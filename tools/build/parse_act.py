"""Parse the PDF of one Act or Legal Notice as published (the Government Gazette supplement on legislation.mt).

Same typesetting family as the consolidated laws (parse_pdf.py: bold section numbers, a margin column with each
section's heading and cross references), with three differences handled here:
- each page has a Gazette page number at the top ("A 140", "B 728") and the last page a printer's footer
  ("Ippubblikat mid-Dipartiment tal-Informazzjoni ... Published by ...", "Prezz/Price", "VERŻJONI ELETTRONIKA");
- the older PDFs (before about 2000) are scans whose text is an OCR layer: no bold, so a section also starts at a
  plain "N." at the left margin when N is the next section number; the OCR text is kept as it is;
- paragraphs: a row also ends a paragraph when it stops well short of the column's right edge (justified text).

Output: parse_pdf's shape plus 'text_layer': 'native' | 'ocr' | 'none', and 'commencement': phrases that state when
the law comes into force.
"""
import re

import pymupdf

import parse_pdf as P

FOOTER = re.compile(r'(Ippubblikat|Published by the Department of Information|Mitbug|Printed at the Government|'
                    r'Prezz\b|VER[ŻZ]JONI ELETTRONIKA|ELECTRONIC VERSION|^_{8,}|^-{8,}$)', re.I)
PAGE_NO = re.compile(r'^\s*[A-E]\s*\d{1,5}\s*$|^\s*\d{1,5}\s*$')
RIGHT: dict[int, float] = {}
_merge = P.merge_rows
_read = P.read_lines


def read_lines(path):
    """parse_pdf's lines without the printer's footer (which the margin column would otherwise take as a note), and
    with small type outside the margin column (tables, forms and schedules set in 7-8pt) kept as body text."""
    out = []
    for l in _read(path):
        if FOOTER.search(l.text.strip()):
            continue
        if not l.margin and l.size < 8.9:
            l.size = 8.9
        out.append(l)
    return out


def merge_rows(lines):
    lines = [l for l in lines if not FOOTER.search(l.text.strip())]
    # A lone "(2)" or "3." sits a little lower or higher than the words it starts: give it their row.
    for l in lines:
        lone = l.text.strip()
        if P.ENUM.fullmatch(lone) or re.fullmatch(r'\d{1,4}[A-Z]{0,3}\.', lone):
            near = [o for o in lines if o is not l and o.page == l.page and o.x > l.x and abs(o.y - l.y) <= 5
                    and not o.margin]
            if near:
                l.y = min(near, key=lambda o: (abs(o.y - l.y), o.x)).y
    rows = _merge(lines)
    # The Gazette page number ("B 2483", or "B" and "2483" on rows of their own) is the first or last row of its
    # page. Only there is a row of bare numbers dropped: inside a page it is a table row (lottery cards, tariffs).
    drop: set[int] = set()
    pages: dict[int, list[int]] = {}
    for i, r in enumerate(rows):
        pages.setdefault(r.page, []).append(i)
    for idx in pages.values():
        for seq in (idx, idx[::-1]):
            for i in seq[:2]:
                if PAGE_NO.match(rows[i].text) or re.fullmatch(r'\s*[A-E]\s*', rows[i].text):
                    drop.add(i)
                else:
                    break
    rows = [r for i, r in enumerate(rows) if i not in drop]
    RIGHT.clear()
    by_page: dict[int, list[float]] = {}
    for r in rows:
        by_page.setdefault(r.page, []).append(r.x1)
    for p, xs in by_page.items():
        xs.sort()
        RIGHT[p] = xs[int(len(xs) * 0.9)] if xs else 0
    return rows


def paragraphs(rows):
    out: list[str] = []
    prev = None
    for r in rows:
        t = P.clean(r.text)
        if not t or FOOTER.search(t) or PAGE_NO.match(t):
            continue
        short = prev is not None and prev.x1 < RIGHT.get(prev.page, 1e9) - 40 and not prev.centred
        new = (prev is None or bool(P.ENUM.match(t)) or r.centred or prev.centred
               or (short and re.search(r'[.:;"”]\s*$', prev.text.strip()) is not None)
               or (r.rel > 6 and abs(r.rel - prev.tx) > 6 and short and r.page == prev.page)
               or (r.page == prev.page and r.y - prev.y > 16))
        if new or not out:
            out.append(t)
        else:
            last = out[-1]
            out[-1] = last + t if last.endswith('-') and t[:1].islower() else last + ' ' + t
        prev = r
    return out


def text_layer(path: str) -> str:
    """'none' (a scan without text), 'ocr' (a scan with a text layer over the image) or 'native'."""
    doc = pymupdf.open(path)
    # Page numbers, the printer's footer and the L.N.'s own number are typeset text even on an image-only PDF.
    chars = sum(len(t.strip()) for page in doc for t in page.get_text('text').split('\n')
                if not (PAGE_NO.match(t) or re.fullmatch(r'\s*[A-E]\s*', t) or FOOTER.search(t.strip())
                        or re.fullmatch(r'\s*(?:L\.\s*N\.|Act)\s+[\w.]+\s+(?:of|tal-)\s*\d{4}\s*', t)))
    if chars < 40:
        return 'none'
    page = doc[0]
    area = page.rect.width * page.rect.height
    for info in page.get_image_info():
        x0, y0, x1, y1 = info['bbox']
        if (x1 - x0) * (y1 - y0) > 0.6 * area:
            return 'ocr'
    return 'native'


DATE = (r'(\d{1,2})(?:st|nd|rd|th)?\s+(?:day\s+of\s+)?(January|February|March|April|May|June|July|August|September|'
        r'October|November|December),?\s+(\d{4})')
MONTHS = {m: i for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                      'September', 'October', 'November', 'December'], 1)}


def iso(m) -> str | None:
    d, mon, y = int(m.group(1)), MONTHS[m.group(2)], int(m.group(3))
    if 1 <= d <= 31 and 1800 < y < 2100:
        return f'{y:04d}-{mon:02d}-{d:02d}'
    return None


def commencement(text: str) -> list[dict]:
    """Statements of when the law comes into force, from the whole text with line breaks removed: a date, or
    'by notice' (on a date to be set by notice). Dates that come later in a list ("as follows: (a) ... from the
    3rd January, 2004") are taken when they follow within 400 characters."""
    out = []
    t = re.sub(r'\s+', ' ', text)
    for m in re.finditer(r'(shall\s+(?:be\s+deemed\s+to\s+have\s+)?(?:come|came)\s+into\s+(?:force|operation)|'
                         r'comes?\s+into\s+force|shall\s+have\s+effect)(.{0,400})', t, re.I):
        tail = m.group(2)
        deemed = 'deemed' in m.group(1).lower()
        d = re.search(DATE, tail[:80])
        if d and iso(d):
            out.append({'date': iso(d), 'deemed': deemed, 'text': (m.group(1) + tail[:d.end()]).strip()})
        elif re.match(r'\s*on\s+(?:such\s+(?:date|day)|a\s+date\s+to\s+be)', tail, re.I):
            out.append({'date': None, 'by_notice': True, 'text': (m.group(0)[:200]).strip()})
        elif re.match(r'\s*(?:as\s+follows|in\s+accordance)', tail, re.I):
            for d in re.finditer(DATE, tail):
                if iso(d):
                    out.append({'date': iso(d), 'deemed': deemed, 'text': (m.group(1) + tail[:d.end()])[-200:].strip()})
    return out


def assent(text: str) -> str | None:
    """The date of the President's assent, printed under "I assent." on an Act."""
    m = re.search(r'I\s+assent', text)
    if not m:
        return None
    d = re.search(DATE, re.sub(r'\s+', ' ', text[m.end():m.end() + 300]))
    return iso(d) if d else None


def own_sections(units: list[dict]) -> list[dict]:
    """An amending law's own sections run 1, 2, 3...; a bold number out of that order ("34." after 2, or "1." again)
    is a provision it inserts into the law it amends, quoted in its text. Such a unit is put back into the section
    before it, number and margin heading included, so the text stays whole. Up to four skipped numbers are allowed
    (sections whose number was not bold)."""
    out: list[dict] = []
    last = 0
    for u in units:
        m = re.fullmatch(r'(\d+)', u['id']) if u['kind'] == 'article' else None
        n = int(m.group(1)) if m else None
        if u['kind'] != 'article' or not out or (n is not None and last < n <= last + 5):
            out.append(u)
            if n is not None:
                last = n
            continue
        prev = out[-1]
        lines = list(u['lines'])
        head = [h for h in u['heading'] if h]
        num = u['id'].split('~')[0]
        lines = [f"{num}. {lines[0]}" if lines else f'{num}.'] + lines[1:]
        prev['lines'] = prev['lines'] + head + lines
        prev['refs'] = prev['refs'] + u['refs']
        prev['notes'] = prev['notes'] + u['notes']
    return out


def parse(path: str) -> dict:
    layer = text_layer(path)
    if layer == 'none':
        return {'text_layer': 'none', 'preamble': [], 'units': [], 'commencement': []}
    P.merge_rows, P.paragraphs, P.read_lines = merge_rows, paragraphs, read_lines
    orig_article = P.ARTICLE
    try:
        if layer == 'ocr':
            d = _parse_ocr(path)
        else:
            d = P.parse(path)
    finally:
        P.merge_rows, P.paragraphs, P.ARTICLE, P.read_lines = _merge, P_paragraphs, orig_article, _read
    d['units'] = own_sections(d['units'])
    raw = '\n'.join(page.get_text('text') for page in pymupdf.open(path))
    d['text_layer'] = layer
    d['commencement'] = commencement(raw)
    d['assent'] = assent(raw)
    flat = re.sub(r'\s+', ' ', raw)
    g = re.search(r'(?:Gazzetta|Gazette).{0,120}?' + DATE, flat[:3000], re.I)
    d['gazette_date'] = iso(re.search(DATE, g.group(0))) if g else None
    return d


P_paragraphs = P.paragraphs


def _ocr_attempt(path: str, by_position: bool) -> dict:
    """Promote "N." rows that continue the numbering to bold, then parse as usual. With `by_position`, the margin
    column is taken from where a line sits on the page (OCR type sizes are unreliable); without, nothing is margin."""
    orig = P.read_lines

    def read_lines(p):
        lines = orig(p)
        doc = pymupdf.open(p)
        width = {i: pg.rect.width for i, pg in enumerate(doc)}
        for l in lines:
            l.margin = by_position and (l.x < width[l.page] * 0.19 or l.x > width[l.page] * 0.70)
            l.size = 8 if l.margin else max(l.size, 10)
        expect = 1
        left: dict[int, float] = {}
        for l in lines:
            if not l.margin:
                left[l.page] = min(left.get(l.page, 1e9), l.x)
        for l in sorted(lines, key=lambda l: (l.page, l.y, l.x)):
            t = l.text.strip()
            t2 = re.sub(r'^[lI]\.', '1.', t)
            m = re.match(r'^(\d{1,3})\.', t2)
            if m and not l.margin and int(m.group(1)) == expect and l.x - left.get(l.page, 0) < 60:
                l.text, l.bold = t2, True
                expect += 1
        return lines
    P.read_lines = read_lines
    try:
        return P.parse(path)
    finally:
        P.read_lines = orig


def _chars(d: dict) -> int:
    return sum(len(x) for x in d['preamble']) + sum(len(x) for u in d['units'] for x in u['lines'] + u['heading'])


def _good(d: dict, total: int) -> bool:
    ids = [u['id'] for u in d['units'] if u['kind'] == 'article']
    return bool(ids) and ids == [str(i) for i in range(1, len(ids) + 1)] and _chars(d) >= 0.85 * total


def _parse_ocr(path: str) -> dict:
    """OCR layers: try the margin column by position, then no margin at all; if neither gives sections numbered
    1..N that keep the text, the whole text is one unit ('text') rather than a wrong split."""
    total = len(re.sub(r'\s+', '', ''.join(pg.get_text('text') for pg in pymupdf.open(path))))
    for by_position in (True, False):
        d = _ocr_attempt(path, by_position)
        if _good(d, total):
            d['split'] = 'margin' if by_position else 'plain'
            return d
    rows = P.merge_rows(P.read_lines(path))
    return {'preamble': [], 'units': [{'id': 'text', 'kind': 'text', 'heading': [], 'lines': P.paragraphs(rows),
                                       'notes': [], 'refs': []}], 'split': 'none'}


if __name__ == '__main__':
    import json
    import sys
    d = parse(sys.argv[1])
    print(json.dumps(d, ensure_ascii=False, indent=1)[:int(sys.argv[2]) if len(sys.argv) > 2 else None])
