# Year 7 booklet generator

Six student completion booklets, two pages per lesson, built from the Year 9
house format. `python3 build.py units/u1.json out.docx` renders one; the page
container is a fixed-height, non-splitting table row, so every page's height is
computed before it is rendered and the answer lines grow to fill the slack.

- `SCHEMA.md` — the authoring contract and the hard length limits
- `units/uN.json` — the authored content, one file per unit
- `dx.py` — WordprocessingML primitives and the Liberation Sans line-wrap model
- `build.py` — page A / page B / cover builders, the elastic fit and the package
- `validate.py` — schema check, then a real render-height check per page
- `icons.py` — fetches the feather icon set into `media/`
- `journey.py` — the two-page stick-in Learning Journey (`python3 journey.py out.docx`)

Content extracted from the ASH lesson decks by a zip+regex pass over the
SharePoint library (repeated dock boilerplate stripped by line frequency).
