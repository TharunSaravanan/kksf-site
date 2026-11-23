# Kural Without Borders

*Reading the Thirukkural Through Faith, Philosophy, and History*

A study edition of all 1,330 kurals of the Thirukkural, published by **Kural Koodal**. Every kural has the Tamil text, a transliteration, a plain-English meaning, explanations at elementary and university level, a real-life example, and a set of comparison lenses (Hinduism, Christianity, Islam, Judaism, Buddhism, Jainism, Sikhism, Greek mythology and philosophy), each with numbered sources.

The same content is published four ways from one set of data files:

| Output | Where it lives | Built by |
|---|---|---|
| Website (1,477 static HTML pages) | `thirukkural-project/web/` | `build_web.py` |
| Book (.docx and print PDF) | `thirukkural-project/book/` | `build_book.js`, `finalize_pdf.py` |
| iOS and Android apps | `apps/` | `apps/build_app_data.py` (see `apps/README.md`) |
| Data (JSON) | `thirukkural-project/data/` | `build_data2.py` |

## Folder guide

| Path | What it holds |
|---|---|
| `chapter_NN_data.json` | Working research data for each of the 133 chapters (adhikarams) |
| `history/` | Historical-context research per chapter |
| `jain/`, `sikh/` | Research for the Jainism and Sikhism lenses |
| `meaning_simple/` | Simplified meaning lines, written for middle-school readers |
| `overrides/` | Hand corrections applied on top of the chapter data |
| `thirukkural-project/data/` | Merged data: `kurals.json`, `adhikarams.json`, `sources.json`, `accuracy_log.json` |
| `ACCURACY_REPORT.md` | Per-kural accuracy scores and flags |
| `LOOP_RUNBOOK.md` | How the chapter research loop runs |
| `*_check.py`, `validate_html.py` | Quality checks run before each build |
| `deploy/DEPLOY.md`, `.github/workflows/` | App build and store upload pipeline |

## Rebuilding everything

```
python3 build_data2.py          # merge chapter research into thirukkural-project/data
python3 build_web.py            # regenerate the website
python3 apps/build_app_data.py  # refresh the data bundled in the apps
node build_book.js              # regenerate the book .docx
python3 validate_html.py && python3 removed_check.py
```

## Not in this repository

Earlier book PDF drafts, temporary build folders, backups and rejected research are kept on the author's computer only. The repository holds the current book (`thirukkural_book.docx` and `thirukkural_book.pdf`).

## Contact

kuralkoodal@gmail.com
