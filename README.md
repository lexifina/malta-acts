# Malta's Acts and Legal Notices, as published

The text of every Act of Parliament and Legal Notice on [legislation.mt](https://legislation.mt), the official source published by the Legislation Unit, as it was published in the Government Gazette: 1520 Acts and 14254 Legal Notices, from 1964-01-01 to 2026-10-23, in 15774 commits and 79748 section files. There is one commit per law, made by that law, dated the day it was published, at noon Malta time. The English text is used throughout.

These are the amending laws themselves. The consolidated laws they amend, change by change, are in [lexifina/malta-law](https://github.com/lexifina/malta-law), whose commits are credited to these same Acts and Legal Notices (same author names), and whose `data/act-dates.csv` lists them with their dates.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did Act V of 2020 say? | `python tools/in_force_on.py 2026-10-28 act/2020/5` |
| Section 3 of it | `cat acts/act/2020/5/3.md` |
| Everything published by a date | `python tools/in_force_on.py 2020-12-31` |
| Every law amending the Code of Organization and Civil Procedure, by a date | `python tools/in_force_on.py 2026-10-28 --amending cap/12` |
| When does a law say it comes into force? | `git log --author='Act V of 2020' --format=%B` (`Commencement:`, `Commenced-by:`) |
| Every L.N. that brought a law into force | `git log --grep='^Commences: '` |
| The list, with dates and the laws amended | [`data/act-dates.csv`](data/act-dates.csv) |

Each section file starts with its number and margin heading (`# 3. Amendment of article 16 of the principal Act.`), with any Part headings above it as `##` lines, then one line per sub-section, paragraph or proviso, then the margin's cross references (`- See Cap. 330.`). `title.md` has the law's name and the front matter: the President's assent, the long title and the enacting words for an Act; the parent Act and the enabling words for a Legal Notice.

## The dates, and which one we use

**Commits are dated by publication**, the day the law appeared in the Government Gazette (`Published:` trailer): 6792 from the Gazette date printed in its title on legislation.mt, 2643 from the page's publication date (`eli:date_publication`) where that falls in the law's own year, 0 from a consolidated law's timeline, 34 from the Gazette date printed in the PDF and 74 from the date of assent (`Published-from:`). Acts and Legal Notices are numbered in order through the year, so 6229 with no date of their own are dated by the last dated one before them, with the range they must fall in as `Published-between:` (`Published-from: estimated`); 2 with no dated neighbour that year are on 1 January (`Published-from: year`). For older laws, legislation.mt's own publication date is often the day the PDF was uploaded, which is why it is used only when it fits the law's number.

Publication is not commencement. Where the text says when it comes into force, each date is a `Commencement:` trailer (2212 laws); "on such date as the Minister may by notice establish" is `Commencement-by: notice`, and legislation.mt's links to the notices that did so are `Commenced-by:` (on the L.N., `Commences:`). `Status:` is legislation.mt's current status of the law (in force, partially in force, not in force). `Amends:` and `Repeals:` are the laws legislation.mt links it to (3335 laws amend at least one).

**Git cannot store dates before 1970.** Earlier commits are on 1970-01-01, one second apart and in order; the real date is in `Published:`, which `tools/in_force_on.py` reads.

## What the text is

- `Text: native` (10826): the text of the published PDF, split into sections by its typography (bold numbers, the margin column).
- `Text: ocr` (3572): older Gazette PDFs are scans with a text layer from OCR done by the publisher (`Text-source: publisher OCR`); no OCR was run for this repository. It is kept as it is, misreadings and all. Where the sections could not be found reliably, the whole text is one file, `text.md`.
- Title only: `Text: none` (1358) is a scan without text; `maltese` (18) is where the English address serves the Maltese PDF; `no-english` (0), `no-pdf` (0) and `unreadable` (0).

## What it does not show

- 607 entries of legislation.mt's ELI sitemap (mostly Acts before 1980) have no record behind them ("No legislation has been found"); they are listed in [`data/not-found.csv`](data/not-found.csv). 
- The Maltese text. Where the two differ, the Maltese text prevails for most laws; see article 74 of the Constitution of Malta.
- Footnotes, tables drawn as images, and the Gazette's page numbers and printer's lines.

This is a research aid. Only the Government Gazette is authoritative.

## How it is built

`fetch_acts.py` reads every `eli/act` and `eli/ln` entry of legislation.mt's ELI sitemap, then each one's English page, whose ELI metadata gives the publication date, the in-force status, the laws it amends, repeals and commences, and the PDF; then downloads the English PDF. `parse_act.py` reads each PDF into sections and finds the commencement statements; `build_acts.py` writes one commit per law with `git fast-import`, so the same PDFs give the same hashes. No AI model takes part in building or checking it. See [`REPRODUCE.md`](REPRODUCE.md) and [`SOURCES.md`](SOURCES.md).

## Licence

Source: legislation.mt, the Legislation Unit, Government of Malta. The texts were converted to one file per section and arranged as commits; the wording was not changed. The Copyright Act (Cap. 415) excludes "any written law" from literary works, subject to article 12 of the Statute Law Revision Act, 1980. **Check that article before this repository is made public.** Lexifina's own contributions are CC0. See [`LICENSE`](LICENSE).
