"""Year 7 RE Learning Journey — two A4 pages for pupils to glue into their books.

Page 1 is the year ahead: six units, their weeks, their big question, what you
will know, the key words and a red/amber/green self-check to come back to.
Page 2 is the record: the department's own assessment grid, how to get better,
and a target.

Black and white, Arial, the same house grammar as the Year 7 booklets. Both
pages are fixed-height, non-splitting containers, so the file is exactly two
pages however LibreOffice or Word renders it.
"""
import os, sys, zipfile
from dx import *
from build import Doc, DOCTYPE, SECT, STYLES, CT, ROOTRELS, page, esc

W_ = CONTENT_W                      # 10318
BODY_W = TEXT_W

VISION = ("VISION:  to understand different world views and become a critical "
          "thinker")

UNITS = [
    dict(n=1, name="Beliefs", weeks="Weeks 1–8", icon="help-circle",
         bq="What do people believe, and how do they show those beliefs?",
         know=["What RE is and why we study it",
               "The difference between a belief, a fact and an opinion",
               "What theists, atheists and agnostics think about God",
               "How artefacts and symbols show what someone believes"],
         words="Belief · Fact · Opinion · Theism · Atheist · Agnostic · "
               "Artefact · Symbol"),
    dict(n=2, name="Hinduism", weeks="Weeks 9–14", icon="sun",
         bq="What do Hindus believe about God, life after death and nature?",
         know=["The story of Rama and Sita, and why Diwali is celebrated",
               "What happens inside a mandir, and what puja is",
               "What Hindus believe about the atman, samsara and moksha",
               "Why karma makes Hindus care for the natural world"],
         words="Diwali · Diva · Aum · Mandir · Murti · Puja · Atman · "
               "Samsara · Moksha · Karma"),
    dict(n=3, name="Buddhism", weeks="Weeks 15–21", icon="feather",
         bq="How do the Buddha's teachings help Buddhists escape suffering?",
         know=["How Siddhartha Gautama became the Buddha",
               "Why Wesak is the most important Buddhist festival",
               "What Buddhists do in a vihara",
               "The Four Noble Truths and the Eightfold Path"],
         words="Siddhartha Gautama · Buddha · Four Sights · Wesak · Vihara · "
               "Dukkha · Nirvana · The Middle Way"),
    dict(n=4, name="Sikhism", weeks="Weeks 22–28", icon="shield",
         bq="What did Guru Nanak teach, and how do Sikhs live it out today?",
         know=["What Guru Nanak taught about God and about equality",
               "The 5Ks, and how the Khalsa began at Vaisakhi",
               "Why the gurdwara serves free food to everyone",
               "What Sikhs believe about the soul and caring for the world"],
         words="Guru Nanak · Equality · Sewa · Khalsa · Vaisakhi · The 5Ks · "
               "Gurdwara · Langar · Waheguru"),
    dict(n=5, name="Heroes of Faith", weeks="Weeks 29–32", icon="award",
         bq="What makes someone a hero of faith?",
         know=["How Gandhi used ahimsa against racism in South Africa",
               "What apartheid was, and what it cost Nelson Mandela",
               "Why Martin Luther King spoke against segregation",
               "How Malala Yousafzai fought for girls to be educated"],
         words="Hero · Ahimsa · Non-violence · Racism · Apartheid · "
               "Segregation · Justice · Courage"),
    dict(n=6, name="Film and Faith", weeks="Weeks 33–36", icon="film",
         bq="How can a film tell a religious story without naming a religion?",
         know=["How Narnia retells a Christian belief through symbols",
               "What three film prayers show about why people pray",
               "Why stories keep warning us about temptation",
               "Why so many film heroes come back from the dead"],
         words="Symbol · Symbolism · Sin · Sacrifice · Forgiveness · "
               "Temptation · Resurrection · Prayer"),
]

# The department's own assessment grid, kept label for label.
RECORD = [
    ("BELIEFS",        ["Baseline (keywords)", "Baseline (questions)",
                        "Summative (keywords)", "Summative (questions)"]),
    ("HINDUISM",       ["Project (Art)", "Project (questions)",
                        "Summative (keywords)", "Summative (questions)"]),
    ("BUDDHISM",       ["Formative (keywords)", "Formative (questions)",
                        "Summative (keywords)", "Summative (questions)"]),
    ("SIKHISM",        ["Formative (keywords)", "Formative (questions)",
                        "Summative (keywords)", "Summative (questions)"]),
    ("HEROES",         ["Unit (keywords)", "Unit (questions)",
                        "Revision (keywords)", "Revision (content)"]),
    ("FILM & FAITH",   ["Unit (keywords)", "Year 8 project", "", ""]),
]

BETTER = [
    ("Learn the key words.", "Cover the meaning, write it from memory, then "
     "check. Two minutes a night beats an hour the day before a test."),
    ("Answer in full sentences.", "A one-word answer can never show what you "
     "know. Start with the question's own words."),
    ("Give a reason, then explain it.", "Say what you think, say why, then say "
     "what someone who disagreed would say back."),
    ("Use the right name for things.", "Mandir, vihara, gurdwara. Getting the "
     "word right is a mark of respect as well as a mark in a test."),
]


# ------------------------------------------------------------------ page one
def page_one(D):
    out, h = [], 0

    # masthead ---------------------------------------------------------------
    logo = drawing(D.icon("logo"), 1463040, D.nid(), ratio=97 / 427.0)
    left = tc(3100, p(logo, line=560), "center")
    right = tc(W_ - 3100, (
        p(run("RELIGIOUS EDUCATION", sz=17, b=True, caps=True, sp=30), line=230)
        + p(run("My Year 7 Learning Journey", sz=44, b=True), line=520)), "center")
    out.append(tbl([tr([left, right], 780)], borders=False)); h += 780
    out.append(p("", line=60, bdr=RULE_HEAVY)); h += 60 + BPAD_HEAVY

    # name strip -------------------------------------------------------------
    cells = []
    for i, lab in enumerate(("NAME", "CLASS", "TEACHER")):
        body = p(run(lab, sz=15, b=True, caps=True, sp=14), line=200)
        body += p("", line=300, bdr=RULE_THIN)
        cells.append(tc(3439 if i < 2 else 3440, body))
    out.append(tbl([tr(cells, 560)], borders=False)); h += 560

    # vision -----------------------------------------------------------------
    out.append(p(run(VISION, sz=19, b=True, caps=True, sp=16),
                 line=260, before=60, bdr=BOX, ind=(90, 90), jc="center"))
    h += 60 + 260 + BPAD_BOX
    x, dh = spacer(60); out.append(x); h += dh

    # the six units ----------------------------------------------------------
    hdr = tr([tc(1560, p(run("WHEN", sz=15, b=True, caps=True, sp=12), line=230)),
              tc(2450, p(run("UNIT", sz=15, b=True, caps=True, sp=12), line=230)),
              tc(4708, p(run("WHAT I WILL KNOW", sz=15, b=True, caps=True, sp=12), line=230)),
              tc(1600, p(run("HOW WELL?", sz=15, b=True, caps=True, sp=12), line=230,
                         jc="center"))], 300)
    rows = [hdr]
    ROW_H = 1990
    for U in UNITS:
        c1 = p(run(U["weeks"].replace("Weeks ", "WEEKS "), sz=16, b=True, caps=True, sp=10),
               line=220)
        c1 += p(drawing(D.icon(U["icon"]), 320000, D.nid()), line=560, before=120)

        c2 = p(run("UNIT %d" % U["n"], sz=14, b=True, caps=True, sp=16), line=190)
        c2 += p(run(U["name"], sz=26, b=True), line=300, after=40)
        c2 += p(run(U["words"], sz=13, i=True), line=175)

        c3 = p(run(U["bq"], sz=17, b=True, i=True), line=225, after=50)
        for k in U["know"]:
            c3 += p(run("•  " + k, sz=16), line=205)

        c4 = ""
        for lab in ("RED", "AMBER", "GREEN"):
            c4 += p(run(lab, sz=12, b=True, caps=True, sp=12), line=170,
                    before=60 if c4 else 30, jc="center")
            c4 += p("", line=230, bdr=BOX, ind=(430, 430))
        rows.append(tr([tc(1560, c1), tc(2450, c2), tc(4708, c3), tc(1600, c4)], ROW_H))
    out.append(tbl(rows)); h += 300 + ROW_H * len(UNITS)

    # tail -------------------------------------------------------------------
    tail = ("WEEK 37  END OF YEAR EXAM  ·  everything above  "
            "|  WEEK 38  EQUALITY WEEK  ·  Alan Turing")
    out.append(p(run(tail, sz=15, b=True, caps=True, sp=12),
                 line=240, before=90, bdr=BOX, ind=(90, 90), jc="center"))
    h += 90 + 240 + BPAD_BOX
    out.append(p(run("Colour a box each time you finish a unit — red if you are "
                     "still unsure, amber if you are getting there, green if you "
                     "could teach it to someone else.",
                     sz=15, i=True), line=215, before=70, jc="center"))
    h += 70 + 215
    return out, h


# ------------------------------------------------------------------ page two
def page_two(D):
    out, h = [], 0

    c = drawing(D.icon("trending-up"), 150000, D.nid())
    c += run("  My progress in RE", sz=24, b=True, caps=True, sp=18)
    out.append(p(c, line=340, after=60, bdr=RULE_HEAD, tabs=10198))
    h += 340 + 60 + BPAD_HEAD
    out.append(p(run("Write your score in the box each time. Your teacher will "
                     "tell you what the test is out of.", sz=17, i=True),
                 line=230, after=80))
    h += 230 + 80

    # the record grid --------------------------------------------------------
    LAB_W, CELL_W = 1918, 2100
    hdr = tr([tc(LAB_W, p(run("UNIT", sz=15, b=True, caps=True, sp=12), line=230))]
             + [tc(CELL_W, p(run("ASSESSMENT %d" % k, sz=15, b=True, caps=True, sp=12),
                             line=230)) for k in (1, 2, 3, 4)], 300)
    rows = [hdr]
    ROW_H = 1290
    for name, labels in RECORD:
        cells = [tc(LAB_W, p(run(name, sz=19, b=True, caps=True, sp=10), line=250),
                    "center")]
        for lab in labels:
            if not lab:
                cells.append(tc(CELL_W, p("", line=200)))
                continue
            body = p(run(lab, sz=14, b=True), line=195, after=40)
            body += p(run("SCORE", sz=11, b=True, caps=True, sp=12), line=170)
            body += p("", line=330, bdr=RULE_THIN, ind=(0, 900))
            body += p(run("DATE", sz=11, b=True, caps=True, sp=12), line=170)
            body += p("", line=250, bdr=RULE_THIN, ind=(0, 900))
            cells.append(tc(CELL_W, body))
        rows.append(tr(cells, ROW_H))

    eoy = [tc(LAB_W, p(run("END OF YEAR", sz=17, b=True, caps=True, sp=10), line=230)
              + p(run("Week 37", sz=13, i=True), line=200), "center")]
    for lab in ("Keywords", "Questions", "Total", "My best unit was"):
        body = p(run(lab, sz=14, b=True), line=195, after=40)
        body += p("", line=380, bdr=RULE_THIN, ind=(0, 700 if lab != "My best unit was" else 0))
        eoy.append(tc(CELL_W, body))
    rows.append(tr(eoy, 960))
    out.append(tbl(rows)); h += 300 + ROW_H * len(RECORD) + 960
    x, dh = spacer(60); out.append(x); h += dh

    # how to get better ------------------------------------------------------
    c = drawing(D.icon("target"), 150000, D.nid())
    c += run("  Four ways to get better at RE", sz=21, b=True, caps=True, sp=16)
    out.append(p(c, line=300, before=150, after=60, bdr=RULE_HEAD, tabs=10198))
    h += 150 + 300 + 60 + BPAD_HEAD
    cells = []
    for k in range(2):
        body = ""
        for title, text in BETTER[k * 2:k * 2 + 2]:
            body += p(run(title, sz=18, b=True), line=245, before=40 if body else 0)
            body += p(run(text, sz=15), line=210, after=30)
        cells.append(tc(5159, body))
    out.append(tbl([tr(cells, 1900)])); h += 1900

    # target -----------------------------------------------------------------
    c = drawing(D.icon("edit-3"), 150000, D.nid())
    c += run("  My target for RE this year", sz=21, b=True, caps=True, sp=16)
    out.append(p(c, line=300, before=170, after=60, bdr=RULE_HEAD, tabs=10198))
    h += 170 + 300 + 60 + BPAD_HEAD
    out.append(p(run("One thing you want to be better at by next July.",
                     sz=15, i=True), line=210, after=30)); h += 210 + 30
    rl, rh = ruled(2); out.extend(rl); h += rh + 2 * BPAD_RULE

    c = drawing(D.icon("message-circle"), 150000, D.nid())
    c += run("  What my teacher says", sz=21, b=True, caps=True, sp=16)
    out.append(p(c, line=300, before=170, after=60, bdr=RULE_HEAD, tabs=10198))
    h += 170 + 300 + 60 + BPAD_HEAD
    rl, rh = ruled(3); out.extend(rl); h += rh + 3 * BPAD_RULE
    return out, h


def fit(chunks, h, name):
    slack = PAGE_BOX - h
    if slack < 0:
        print("  !! %s overflows by %d twips" % (name, -slack))
    return chunks, h, slack


def build(outpath):
    D = Doc()
    a, ha, sa = fit(*page_one(D), "page 1")
    b, hb, sb = fit(*page_two(D), "page 2")
    body = page(a) + p("", line=1) + page(b)
    doc = DOCTYPE + body + p("", line=1) + SECT + "</w:body></w:document>"

    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/styles" Target="styles.xml"/>'
            '<Relationship Id="rIdH" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/header" Target="header1.xml"/>'
            '<Relationship Id="rIdF" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/footer" Target="footer1.xml"/>')
    for n in D.media:
        rels += ('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/'
                 '2006/relationships/image" Target="media/%s.png"/>' % (D.rels[n], n))
    rels += "</Relationships>"

    hdr = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           '<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="120" '
           'w:lineRule="exact"/></w:pPr></w:p></w:hdr>')
    ftr = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           '<w:p><w:pPr><w:tabs><w:tab w:val="right" w:pos="10318"/></w:tabs>'
           '<w:spacing w:before="0" w:after="0" w:line="200" w:lineRule="exact"/></w:pPr>'
           '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>'
           '<w:color w:val="595959"/><w:sz w:val="15"/><w:szCs w:val="15"/></w:rPr>'
           '<w:t xml:space="preserve">Harlington School  ·  Religious Education  ·  '
           'Year 7 Learning Journey  ·  2026–27</w:t></w:r>'
           '<w:r><w:tab/></w:r>'
           '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>'
           '<w:color w:val="595959"/><w:sz w:val="15"/><w:szCs w:val="15"/></w:rPr>'
           '<w:t xml:space="preserve">Stick me in the front of your book</w:t></w:r>'
           '</w:p></w:ftr>')

    with zipfile.ZipFile(outpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT)
        z.writestr("_rels/.rels", ROOTRELS)
        z.writestr("word/document.xml", doc)
        z.writestr("word/_rels/document.xml.rels", rels)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/header1.xml", hdr)
        z.writestr("word/footer1.xml", ftr)
        for n in D.media:
            z.write("media/%s.png" % n, "word/media/%s.png" % n)
    print("page 1  %5d (%+5d)   page 2  %5d (%+5d)   box %d"
          % (ha, ha - PAGE_BOX, hb, hb - PAGE_BOX, PAGE_BOX))
    return sa, sb


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "out/Y7_Learning_Journey.docx")
