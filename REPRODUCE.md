# Reproducing this repository

Everything here comes from legislation.mt and can be rebuilt from it. The same PDFs give the same commit hashes.

## What this build used

- Built on 2026-10-29 from 16381 sitemap entries: 1520 Acts and 14254 Legal Notices with a record, 607 without.
- 15774 law commits (1520 Acts, 14254 Legal Notices) and this documentation commit; 79748 section files.
- The sha256 of every PDF is in `data/actpdf-sha256.tsv`.
- Build scripts (sha256), copied to `tools/build/`:
  - `build.py` 15a5f34a21ab930f6c780908ae6889a71144c9897a139babb309e346c3e85782
  - `build_acts.py` 5d5e5f99f812ec59655b4a8d711bf0fa69b5734ae642ad17b19863332e86db68
  - `docs_acts.py` 01c0027b496425670557de5c5e484fe4511050d3b1e6926be23ac9d6b538a6aa
  - `fetch_acts.py` 3e2e983611baf2a9fbbf5f64c9389a7e01ae27ca12bfc81e65dc8c799a55a79d
  - `fetch_catalogue.py` 9375708ef9afa29f1bc2af9df888da34aca0c84efc9c8fd0c7a9d4f51a8bd208
  - `parse_act.py` c1b8c8a65718bbe9885eb86ff1d1390ec3a2a8a954d89e320bb6e0c99b0eb663
  - `parse_pdf.py` 9cfcc21386b74f35f9730f24b97f26f0c248f01fd89a4367300c08cc7e2edd59

## Steps

Python 3.11+ with `pymupdf`, and `curl` and `git` on the path.

```sh
cd tools/build
python fetch_catalogue.py --workers 16   # the consolidated laws' timelines (dates of related laws)
python fetch_acts.py --workers 16        # .cache/acts/<act|ln>-YYYY-N.json and .cache/actpdf/<snapshot>.pdf
python build_acts.py ../../../malta-acts-rebuilt --today 2026-10-29 --branch main
```

`--today` dates the documentation commit and is required, so a rebuild never depends on the day it is run.

## Fetch rate

legislation.mt's robots.txt (checked 28 October 2026) disallows only the Sogou crawler and sets no Crawl-delay. The 16381 pages and their PDFs were fetched with at most 16 parallel requests (curl, compressed), cached on disk so each document was fetched once. A rebuild from the cache makes no requests. For a fresh full fetch, consider asking the Legislation Unit for bulk access first.

## Decisions

- **Which text:** the English PDF linked from `eli/<act|ln>/YYYY/N/eng`; a PDF that is in fact Maltese (more than a few of ħ ġ ż ċ) is not used.
- **Sections:** a section (regulation, article, rule) starts at a bold number at the start of a line; in an OCR layer, at a plain number that continues the numbering. Margin headings and cross references belong to the section that starts nearest at or above them. Front matter is `title.md`.
- **Normalised away:** whitespace, curly quotes, dashes and soft hyphens; Gazette page numbers, footers and price lines are dropped.
- **Dates:** publication, at noon Malta time (CET, or CEST from the last Sunday of March to the last Sunday of October); before 1970, clamped to 1970-01-01 plus one second per commit, in order.
- **Order:** by publication date; on one date, Acts before Legal Notices, each by year and number.
