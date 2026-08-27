# KS3 RE — Harlington School

Student-facing week-by-week pages for Key Stage 3 Religious Studies.

| Page | Live |
|---|---|
| Year 9, week by week | https://vmcssse-ui.github.io/ks3-re/year9.html |

`index.html` redirects to `year9.html`.

## How the links work

Every resource button points at the RE SharePoint library:

```
/sites/HS_Subjects_RE/Year 11/Philosophy/KS3 Ai/KS3/YEAR 9/
```

with `?web=1` appended, so decks open in PowerPoint Online rather than
downloading. Viewers must be signed in to the school tenant.

**Move or rename that folder and all 86 file links break together.** Rebuild
the page from `build_year9.py` rather than editing the HTML by hand — the unit
tables, week list and resource paths all live in that one file.

## Rebuilding

```
python3 build_year9.py     # writes year9.html
```
