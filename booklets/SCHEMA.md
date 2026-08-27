# Year 7 booklet unit JSON — authoring schema

One file per unit: `units/uN.json`. The renderer lays every lesson out as a fixed
two-page spread, so **length limits are hard**: overshoot and the page clips.

```json
{
  "unit": 1,
  "name": "Beliefs",
  "icon": "help-circle",
  "big_question": "unit-level question, <= 90 chars, ends with '?'",
  "glossary": [ {"w": "Key word", "d": "definition, <= 80 chars, lower case start"} ],
  "lessons": [ { ...lesson objects... } ]
}
```

`glossary`: **exactly 16** entries, drawn from the words the unit's decks actually
teach. Order them roughly in teaching order.

## Lesson object

```json
{
  "n": 1,
  "title": "Why study RE?",
  "icon": "globe",
  "big_question": "<= 90 chars, ends with '?'",
  "aims": ["DESCRIBE — ...", "DISCUSS — ...", "EXPLAIN — ..."],
  "bell": {"instruction": "Answer in full sentences.",
           "questions": ["q1", "q2", "q3"]},
  "keywords": ["Word one", "Word two", "Word three", "Word four"],
  "learn": {"caption": "<= 55 chars", "col1": "Idea", "col2": "What it means / example",
            "rows": ["row label 1", "...", "...", "...", "row label 5"]},
  "source": {"quote": "...", "attrib": "— ...", "task": "..."},
  "stretch": {"question": "...", "wordbank": ["w1","w2","w3","w4","w5"],
              "starters": ["Firstly, ...", "This means that",
                           "Secondly, ...", "This means that"]},
  "debate": {"statement": "...", "agree": ["arg 1", "arg 2"],
             "disagree": ["arg 1", "arg 2"], "how_to_win": "..."},
  "quickfire": [ {"tag": "LAST UNIT", "q": "..."} ]
}
```

### Hard limits

| field | limit |
|---|---|
| `title` | **≤ 30 chars** (longer drops to a smaller size and looks wrong) |
| `big_question` | ≤ 90 chars |
| each `aims` entry | ≤ 66 chars **including** the `DESCRIBE — ` prefix |
| each bell question | ≤ 80 chars, exactly **3** questions |
| `keywords` | exactly **4**, each ≤ 26 chars |
| `learn.caption` | ≤ 55 chars |
| `learn.rows` | exactly **5**, each ≤ 42 chars |
| `source.quote` | 90–180 chars, **no** surrounding quote marks (the renderer adds them) |
| `source.attrib` | ≤ 60 chars, starts `— ` |
| `source.task` | ≤ 110 chars |
| `stretch.question` | ≤ 90 chars |
| `stretch.wordbank` | 5 items, each ≤ 18 chars |
| `stretch.starters` | exactly 4, alternating a lead-in and `This means that` |
| `debate.statement` | ≤ 78 chars, no quote marks (the renderer adds them) |
| `debate.agree` / `disagree` | exactly 2 each, each ≤ 92 chars |
| `debate.how_to_win` | ≤ 105 chars |
| `quickfire` | exactly **6**, each `q` ≤ 52 chars |

### Content rules

1. **Everything comes from the unit's own decks.** Read the extracted slide text in
   `y7_raw.json` (`decks[<relative pptx path>]` → list of slides → list of lines).
   Quote the deck's own definitions and examples. Do not invent scripture references:
   if a deck quotes scripture with no chapter and verse, attribute it as
   `— Unit N lesson slides, on <topic>` rather than citing a verse.
2. **Year 7 pitch.** Short sentences. One idea per line. Explain any term the first
   time it appears. No GCSE command words beyond DESCRIBE / DISCUSS / EXPLAIN.
   Reading age around 11: prefer "holy building" to "sacred edifice".
3. `quickfire` tags: questions 1–2 `LAST UNIT` (or `LAST LESSON` in lesson 1 of a
   unit that has no predecessor — then use `THIS LESSON`), 3–4 `LAST LESSON`,
   5–6 `THIS LESSON`. Lesson 1 of unit 1: all six `THIS LESSON`.
4. `debate.agree` / `disagree` are **complete printed arguments** the student reads,
   not prompts. Each is one sentence a Year 7 could say aloud.
5. Assessment lessons (baseline / formative / summative / DIT) keep the same seven
   tasks, but pitched at revision: bell work recalls the unit, `learn.rows` are the
   topics the test covers, stretch rehearses the exam-style answer.
6. `icon`: one name from this list, chosen to suit the lesson —
   activity alert-triangle anchor aperture award bell book-open box camera clock
   cloud codepen coffee compass crosshair droplet edit-3 eye feather file-text film
   flag gift globe grid heart help-circle hexagon home key layers map message-circle
   mic moon music navigation octagon package pen-tool play-circle radio scissors
   send shield smile star sun sunrise target thumbs-up trending-up triangle tv
   umbrella user-check users video volume-2 watch wifi wind zap
   Do not reuse `bell`, `key`, `grid`, `book-open`, `star`, `alert-triangle`, `zap`
   or `clock` as a lesson or unit icon — those are the task icons.
7. Black and white only; no colour, no emoji, no markdown inside any string.
8. Apostrophes and quotes: use plain ASCII `'` and `"` inside strings.
