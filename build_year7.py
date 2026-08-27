# -*- coding: utf-8 -*-
"""Year 7 week-by-week page.

Same machinery as build_year9.py, pointed at the YEAR 7 library and dressed in
the Year 7 colour (clear orange). Resources live on the school SharePoint; every
button is an absolute path-style URL with ?web=1 so decks open in PowerPoint
Online rather than downloading. URL-encode with quote(part, safe="()'") so
parentheses and apostrophes stay literal — "(2) 5K's" needs both.

There is no Student Companion at Year 7: booklets and the weekly page only.
"""
import html, os
from urllib.parse import quote
from datetime import date, timedelta

E = lambda s: html.escape(str(s), quote=True)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "year7.html")

SP_BASE = "https://hs365.sharepoint.com"
SP_ROOT = "/sites/HS_Subjects_RE/Year 11/Philosophy/KS3 Ai/KS3/YEAR 7"


def sp(rel, folder=False):
    parts = (SP_ROOT + "/" + rel).split("/")
    path = "/".join(quote(p, safe="()'").replace("+", "%2B") for p in parts)
    if folder:
        return (f"{SP_BASE}/sites/HS_Subjects_RE/Year%2011/Forms/AllItems.aspx"
                f"?id={quote(SP_ROOT + '/' + rel, safe='')}")
    return f"{SP_BASE}{path}?web=1"


# --------------------------------------------------------------- calendar
# Harlington School term dates 2026-27. Teaching weeks run from Monday
# 7 September 2026; the Year 7 induction day (2 Sept) and the 3rd and 4th of
# September fall before week 1.
TERMS = [
    ("Autumn term", date(2026, 9, 7),  date(2026, 12, 18)),
    ("Spring term", date(2027, 1, 4),  date(2027, 3, 25)),
    ("Summer term", date(2027, 4, 12), date(2027, 7, 22)),
]
BREAKS = [
    ("Half term", date(2026, 10, 26), date(2026, 11, 6), "two weeks"),
    ("Christmas holiday", date(2026, 12, 21), date(2027, 1, 1), ""),
    ("Half term", date(2027, 2, 15), date(2027, 2, 19), ""),
    ("Easter holiday", date(2027, 3, 26), date(2027, 4, 9), ""),
    ("Half term", date(2027, 5, 31), date(2027, 6, 4), ""),
]
CLOSED = [(b[1], b[2]) for b in BREAKS]


def teaching_weeks():
    out = []
    for name, start, end in TERMS:
        m = start
        while m <= end:
            if not any(a <= m <= b for a, b in CLOSED):
                out.append((m, min(m + timedelta(days=4), end), name))
            m += timedelta(days=7)
    return out


WEEK_DATES = teaching_weeks()


def dm(d):
    return f"{d.day} {d.strftime('%b')}"


def daterange(a, b):
    if a.month == b.month:
        return f"{a.day}–{b.day} {b.strftime('%B')}"
    return f"{dm(a)} – {dm(b)}"


# --------------------------------------------------------------- the units
U1 = "1. BELIEFS"
U2 = "2. HINDUISM"
U3 = "3. BUDDHISM"
U4 = "4. SIKHISM"
U5 = "5. HEROES OF FAITH"
U6 = "6. FILM AND FAITH"
UE = "END OF YEAR EXAM"
UQ = "EQUALITY WEEK + EOY"

UNITS = [
    dict(key="u1", n=1, name="Beliefs", folder=U1,
         blurb="What RE is and why we study it, then belief against fact and "
               "opinion, the question of God, and the artefacts and symbols "
               "believers use to show what they hold true.",
         booklet=f"{U1}/RESOURCES/Y7_Unit1_Beliefs_Booklet.docx",
         resources=[("Unit cover sheet", f"{U1}/RESOURCES/UNIT 1 - NEW COVER SHEET - ASH.docx"),
                    ("Lesson plans folder", f"{U1}/RESOURCES/ASH - LESSON PLANS")]),
    dict(key="u2", n=2, name="Hinduism", folder=U2,
         blurb="Diwali and the story of Rama and Sita, inside the mandir, and "
               "Hindu beliefs about the soul, rebirth and caring for the "
               "natural world.",
         booklet=f"{U2}/RESOURCES/Y7_Unit2_Hinduism_Booklet.docx",
         resources=[("Unit cover sheet", f"{U2}/RESOURCES/UNIT 2 - COVER SHEET - ASH.docx"),
                    ("Hinduism booklet (older)", f"{U2}/RESOURCES/Y7 - Hinduism booklet.docx"),
                    ("Lesson plans folder", f"{U2}/RESOURCES/ASH - LESSON PLANS")]),
    dict(key="u3", n=3, name="Buddhism", folder=U3,
         blurb="Siddhartha Gautama and the Four Sights, the festival of Wesak, "
               "worship in the vihara, and the Four Noble Truths that answer "
               "the problem of suffering.",
         booklet=f"{U3}/RESOURCES/Y7_Unit3_Buddhism_Booklet.docx",
         resources=[("Unit cover sheet", f"{U3}/RESOURCES/BUDDHISM - UNIT 3 COVER SHEET.docx"),
                    ("Buddhism booklet (older)", f"{U3}/RESOURCES/Y7 - Buddhism booklet.docx"),
                    ("Lesson plans folder", f"{U3}/RESOURCES/ASH - LESSON PLANS")]),
    dict(key="u4", n=4, name="Sikhism", folder=U4,
         blurb="Guru Nanak and the teaching that all people are equal, the Five "
               "Ks, the gurdwara and its langar, and Sikh beliefs about the "
               "soul and stewardship.",
         booklet=f"{U4}/RESOURCES/Y7_Unit4_Sikhism_Booklet.docx",
         resources=[("Unit cover sheet", f"{U4}/RESOURCES/SIKSHIM - UNIT 4 COVER SHEET.docx"),
                    ("Sikhism booklet (older)", f"{U4}/RESOURCES/Y7 - Sikhism booklet.docx"),
                    ("Lesson plans folder", f"{U4}/RESOURCES/ASH - LESSON PLANS")]),
    dict(key="u5", n=5, name="Heroes of Faith", folder=U5,
         blurb="Four people whose beliefs made them act: Gandhi, Nelson "
               "Mandela, Martin Luther King and Malala Yousafzai.",
         booklet=f"{U5}/RESOURCES/Y7_Unit5_Heroes_of_Faith_Booklet.docx",
         resources=[("Unit cover sheet", f"{U5}/RESOURCES/HEROES OF FAITH - COVER SHEET.docx")]),
    dict(key="u6", n=6, name="Film and Faith", folder=U6,
         blurb="Reading religious meaning in film — symbol and sacrifice, "
               "prayer, temptation and resurrection — using the stories "
               "students already know.",
         booklet=f"{U6}/RESOURCES/Y7_Unit6_Film_and_Faith_Booklet.docx",
         resources=[("Unit cover sheet", f"{U6}/RESOURCES/UNIT 6 - FILM AND FAITH - COVER SHEET.docx")]),
    dict(key="eoy", n=7, name="End of Year Exam", folder=UE,
         blurb="Revision across all six units, the paper itself, and the DIT "
               "lesson that follows it.",
         booklet=None, resources=[]),
    dict(key="eq", n=8, name="Equality Week", folder=UQ,
         blurb="The closing week of the year: Alan Turing, and the Prince of "
               "Egypt task.",
         booklet=None, resources=[]),
]

# --------------------------------------------------------------- the weeks
# kind: lesson · formative · summative · revision · exam · dit
# res:  (label, type, relative path)   type ∈ deck · doc · paper
def W(n, unit, title, kind, res, note=None):
    return dict(n=n, unit=unit, title=title, kind=kind, res=res, note=note)


WEEKS = [
    # ---- Unit 1: Beliefs ---------------------------------------------------
    W(1, "u1", "Why study RE?", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(1) WHY STUDY RE/(1) WHY STUDY RE - ASH.pptx"),
        ("Expectations deck", "deck", f"{U1}/(1) WHY STUDY RE/(1) EXPECTATIONS PPT - ASH.pptx"),
        ("Lesson plan", "doc", f"{U1}/RESOURCES/ASH - LESSON PLANS/(1) LESSON PLAN - WHY STUDY RE - ASH.docx"),
    ], note="First RE lesson of Year 7 — seating plan, expectations and the "
            "Learning Journey are all set up here."),
    W(2, "u1", "Baseline test", "formative", [
        ("Baseline test", "paper", f"{U1}/(1A) BASELINE TEST/(1A) - NEW BASELINE TEST - ASH.docx"),
        ("DIT deck", "deck", f"{U1}/(1A) BASELINE TEST/(1A) DIT - BASELINE TEST - ASH.pptx"),
        ("Older baseline test", "paper", f"{U1}/(1A) BASELINE TEST/(1A) OLD BASELINE TEST - ASH.docx"),
    ]),
    W(3, "u1", "What is a belief?", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(2) WHAT IS A BELIEF/(2) WHAT IS A BELIEF - ASH.pptx"),
        ("Worksheet — belief, fact, opinion", "doc", f"{U1}/(2) WHAT IS A BELIEF/(2) WORKSHEET - BELIEF, FACT, OPINION STATEMENTS - ASH.docx"),
        ("Lesson plan", "doc", f"{U1}/RESOURCES/ASH - LESSON PLANS/(2) LESSON PLAN - WHAT IS A BELIEF - ASH.docx"),
    ]),
    W(4, "u1", "Is seeing believing?", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(3) IS SEEING BELIEVING/(3) IS SEEING BELIEVING - ASH.pptx"),
        ("Lesson plan", "doc", f"{U1}/RESOURCES/ASH - LESSON PLANS/(3) LESSON PLAN - IS SEEING BELIEVING - ASH.docx"),
    ]),
    W(5, "u1", "Is there a God?", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(4) IS THERE A GOD/(4) IS THERE A GOD - ASH.pptx"),
        ("Worksheet — religious evidence", "doc", f"{U1}/(4) IS THERE A GOD/(4) WORKSHEET - RELIGIOUS EVIDENCE STATEMENT SHEET - ASH.docx"),
        ("Information — religious evidence", "doc", f"{U1}/(4) IS THERE A GOD/(4) WORKSHEET - RELIGIOUS EVIDENCE INFORMATION - ASH.docx"),
        ("Lesson plan", "doc", f"{U1}/RESOURCES/ASH - LESSON PLANS/(4) LESSON PLAN - IS THERE A GOD - ASH.docx"),
    ]),
    W(6, "u1", "Religious artefacts", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(5) RELIGIOUS ARTEFACTS/(5) RELIGIOUS ARTEFACTS - ASH.pptx"),
        ("Worksheet — artefacts", "doc", f"{U1}/(5) RELIGIOUS ARTEFACTS/(5) WORKSHEET - RELIGIOUS ARTEFACT - ASH.docx"),
        ("Information — artefacts", "doc", f"{U1}/(5) RELIGIOUS ARTEFACTS/(5) WORKSHEET - RELIGIOUS ARTEFACT INFORMATION - ASH.docx"),
        ("Lesson plan", "doc", f"{U1}/RESOURCES/ASH - LESSON PLANS/(5) LESSON PLAN - RELIGIOUS ARTEFACTS - ASH.docx"),
    ]),
    W(7, "u1", "Religious symbols", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(6) RELIGIOUS SYMBOLS/(6) RELIGIOUS SYMBOLS - ASH.pptx"),
        ("Worksheet — symbols", "doc", f"{U1}/(6) RELIGIOUS SYMBOLS/(6) WORKSHEET - RELIGIOUS SYMBOLS - ASH.docx"),
        ("Information sheet", "doc", f"{U1}/(6) RELIGIOUS SYMBOLS/(6) INFORMATION SHEET - ASH.docx"),
        ("Lesson plan", "doc", f"{U1}/RESOURCES/ASH - LESSON PLANS/(6) LESSON PLAN - RELIGIOUS SYMBOLS - ASH.docx"),
    ]),
    W(8, "u1", "Summative assessment", "summative", [
        ("Summative paper", "paper", f"{U1}/(7) SUMMATIVE/(7) NEW SUMMATIVE - ASH.docx"),
        ("Revision questions", "doc", f"{U1}/(7) SUMMATIVE/(7) REVISION QUESTIONS - BELIEFS.docx"),
        ("Lesson deck", "deck", f"{U1}/(7) SUMMATIVE/(7) SUMMATIVE - ASH.pptx"),
        ("DIT deck", "deck", f"{U1}/(7) SUMMATIVE/(7) DIT NEW - SUMMATIVE - ASH.pptx"),
        ("Older summative paper", "paper", f"{U1}/(7) SUMMATIVE/(7) OLD SUMMATIVE - ASH.docx"),
        ("Lesson plan", "doc", f"{U1}/RESOURCES/ASH - LESSON PLANS/(7) SUMMATIVE - LESSON PLAN - ASH.docx"),
    ]),
    # ---- Unit 2: Hinduism --------------------------------------------------
    W(9, "u2", "Diwali", "lesson", [
        ("Lesson deck", "deck", f"{U2}/(2) FESTIVALS - DIWALI/(2) DIWALI - ASH NEW.pptx"),
    ], note="The unit's introduction-to-Hinduism lesson is not on SharePoint, "
            "so the unit opens on Diwali. Brahman and the Trimurti are picked "
            "up in week 13."),
    W(10, "u2", "The Alien Project", "formative", [
        ("Formative assessment", "paper", f"{U2}/(2A) ALIEN PROJECT/Formative Assessment - Alien Project.docx"),
        ("Project deck", "deck", f"{U2}/(2A) ALIEN PROJECT/(2A) ALIEN PROJECT NEW - ASH.pptx"),
        ("Older project deck", "deck", f"{U2}/(2A) ALIEN PROJECT/(2A) ALIEN PROJECT - ASH.pptx"),
    ]),
    W(11, "u2", "The Mandir", "lesson", [
        ("Lesson deck", "deck", f"{U2}/(3) MANDIR/(3) MANDIR - ASH.pptx"),
        ("Worksheet — virtual mandir", "doc", f"{U2}/(3) MANDIR/(3) WORKSHEET - VIRTUAL MANDIR - ASH.docx"),
        ("Information sheet", "doc", f"{U2}/(3) MANDIR/(3) NEW INFO SHEET - ASH.docx"),
        ("Lesson plan", "doc", f"{U2}/RESOURCES/ASH - LESSON PLANS/(3) LESSON PLAN - MANDIR - ASH.docx"),
    ]),
    W(12, "u2", "Belief in the afterlife", "lesson", [
        ("Lesson deck", "deck", f"{U2}/(4) BELIEF IN THE AFTERLIFE/(4) BELIEF IN THE AFTERLIFE - ASH.pptx"),
        ("Lesson plan", "doc", f"{U2}/RESOURCES/ASH - LESSON PLANS/(4) LESSON PLAN - BELIEF IN THE AFTERLIFE - ASH.docx"),
    ]),
    W(13, "u2", "Hinduism and nature", "lesson", [
        ("Lesson deck", "deck", f"{U2}/(5) HINDUISM AND NATURE/(5) HINDUISM AND NATURE - ASH.pptx"),
        ("Lesson plan", "doc", f"{U2}/RESOURCES/ASH - LESSON PLANS/(5) LESSON PLAN - HINDUISM AND NATURE - ASH.docx"),
    ]),
    W(14, "u2", "Summative assessment", "summative", [
        ("Summative paper", "paper", f"{U2}/(6) SUMMATIVE/(6) NEW SUMMATIVE - ASH.docx"),
        ("Revision questions", "doc", f"{U2}/(6) SUMMATIVE/(6) REVISION QUESTIONS - HINDUISM.docx"),
        ("Revision questions 2", "doc", f"{U2}/(6) SUMMATIVE/(6) REVISION QUESTIONS 2 - HINDUISM.docx"),
        ("Lesson deck", "deck", f"{U2}/(6) SUMMATIVE/(6) SUMMATIVE + HW - ASH.pptx"),
        ("DIT deck", "deck", f"{U2}/(6) SUMMATIVE/(6) DIT - SUMMATIVE TEST - ASH.pptx"),
        ("Older summative paper", "paper", f"{U2}/(6) SUMMATIVE/(6) SUMMATIVE TEST - ASH.docx"),
        ("Lesson plan", "doc", f"{U2}/RESOURCES/ASH - LESSON PLANS/(6) LESSON PLAN - SUMMATIVE - ASH.docx"),
    ]),
    # ---- Unit 3: Buddhism --------------------------------------------------
    W(15, "u3", "Siddhartha Gautama", "lesson", [
        ("Lesson deck", "deck", f"{U3}/(1) SIDDHARTHA GAUTAMA/(1) SIDDHARTHA GAUTAMA - ASH.pptx"),
        ("Worksheet — fill in the gaps", "doc", f"{U3}/(1) SIDDHARTHA GAUTAMA/(1) WORKSHEET - FILL IN THE GAPS - ASH.docx"),
        ("Lesson plan", "doc", f"{U3}/RESOURCES/ASH - LESSON PLANS/(1) LESSON PLAN - SIDDHARTHA GAUTAMA - ASH.docx"),
    ]),
    W(16, "u3", "Wesak", "lesson", [
        ("Lesson deck", "deck", f"{U3}/(2) FESTIVAL - WESAK/(2) FESTIVAL OF WESAK - ASH.pptx"),
    ]),
    W(17, "u3", "The Vihara", "lesson", [
        ("Lesson deck", "deck", f"{U3}/(3) VIHARA/(3) VIHARA - ASH.pptx"),
        ("Worksheet — virtual vihara", "doc", f"{U3}/(3) VIHARA/(3) WORKSHEET - VIRTUAL VIHARA - ASH.docx"),
        ("Information — virtual vihara", "doc", f"{U3}/(3) VIHARA/(3) WORKSHEET - VIRTUAL VIHARA INFORMATION - ASH.docx"),
        ("Lesson plan", "doc", f"{U3}/RESOURCES/ASH - LESSON PLANS/(3) LESSON PLAN - VIHARA - ASH.docx"),
    ]),
    W(18, "u3", "Formative assessment", "formative", [
        ("Formative paper", "paper", f"{U3}/(3A) FORMATIVE/(3A) NEW BUDDHISM FORMATIVE - ASH.docx"),
        ("DIT deck", "deck", f"{U3}/(3A) FORMATIVE/(3A) DIT - ASH.pptx"),
        ("Older formative paper", "paper", f"{U3}/(3A) FORMATIVE/(3A) FORMATIVE - BUDDHISM - ASH.docx"),
    ]),
    W(19, "u3", "Belief in the afterlife", "lesson", [
        ("Lesson deck", "deck", f"{U3}/(4) BELIEF IN THE AFTERLIFE/(4) BELIEF IN THE AFTERLIFE - ASH.pptx"),
        ("Worksheet — Eightfold Path", "doc", f"{U3}/(4) BELIEF IN THE AFTERLIFE/(4) WORKSHEET - EIGHTFOLD PATH - ASH.docx"),
        ("Lesson plan", "doc", f"{U3}/RESOURCES/ASH - LESSON PLANS/(4) LESSON PLAN - BELIEF IN THE AFTERLIFE - ASH.docx"),
    ]),
    W(20, "u3", "Buddhism and nature", "lesson", [
        ("Lesson deck", "deck", f"{U3}/(5) BUDDHISM AND NATURE/(5) BUDDHISM AND NATURE - ASH.pptx"),
        ("Lesson plan", "doc", f"{U3}/RESOURCES/ASH - LESSON PLANS/(5) LESSON PLAN - BUDDHISM AND NATURE - ASH.docx"),
    ]),
    W(21, "u3", "Summative assessment", "summative", [
        ("Summative paper", "paper", f"{U3}/(6) SUMMATIVE/(6) NEW SUMMATIVE - ASH.docx"),
        ("Revision questions", "doc", f"{U3}/(6) SUMMATIVE/(6) REVISION QUESTIONS - BUDDHISM.docx"),
        ("Lesson deck", "deck", f"{U3}/(6) SUMMATIVE/(6) SUMMATIVE + HW - ASH.pptx"),
        ("DIT deck", "deck", f"{U3}/(6) SUMMATIVE/(6) DIT - SUMMATIVE BUDDHISM - ASH.pptx"),
        ("Older summative paper", "paper", f"{U3}/(6) SUMMATIVE/(6) SUMMATIVE TEST - BUDDHISM.docx"),
        ("Lesson plan", "doc", f"{U3}/RESOURCES/ASH - LESSON PLANS/(6) LESSON PLAN - SUMMATIVE - ASH.docx"),
    ]),
    # ---- Unit 4: Sikhism ---------------------------------------------------
    W(22, "u4", "Guru Nanak", "lesson", [
        ("Lesson deck", "deck", f"{U4}/(1) GURU NANAK/(1) GURU NANAK - ASH.pptx"),
        ("Bell work — wordsearch", "doc", f"{U4}/(1) GURU NANAK/(1) BELL WORK - WORDSEARCH - ASH.docx"),
        ("Homework — the 10 Gurus", "deck", f"{U4}/(1) GURU NANAK/(1) HW - 10 GURUS INFORMATION - ASH.pptx"),
        ("Homework worksheet", "doc", f"{U4}/(1) GURU NANAK/(1) HW - 10 GURUS WORKSHEET - ASH.docx"),
        ("Lesson plan", "doc", f"{U4}/RESOURCES/ASH - LESSON PLANS/(1) LESSON PLAN - GURU NANAK - ASH.docx"),
    ]),
    W(23, "u4", "The Five Ks", "lesson", [
        ("Lesson deck", "deck", f"{U4}/(2) 5K's/(2) THE 5K'S - ASH.pptx"),
        ("Worksheet — Vaisakhi and the 5Ks", "doc", f"{U4}/(2) 5K's/(2) WORKSHEET - VAISAKHI AND 5K'S GAP FILL - ASH.docx"),
    ]),
    W(24, "u4", "The Gurdwara", "lesson", [
        ("Lesson deck", "deck", f"{U4}/(3) GURDWARA/(3) GURDWARA - ASH.pptx"),
        ("Worksheet — virtual gurdwara", "doc", f"{U4}/(3) GURDWARA/(3) WORKSHEET - VIRTUAL GURDWARA - ASH.docx"),
        ("Information — virtual gurdwara", "doc", f"{U4}/(3) GURDWARA/(3) VIRTUAL GURDWARA - INFORMATION - ASH.docx"),
    ]),
    W(25, "u4", "Formative assessment", "formative", [
        ("Formative paper", "paper", f"{U4}/(3A) FORMATIVE/(3) FORMATIVE - SIKHISM.docx"),
        ("DIT deck", "deck", f"{U4}/(3A) FORMATIVE/(3A) DIT - FORMATIVE - ASH.pptx"),
    ]),
    W(26, "u4", "Belief in the afterlife", "lesson", [
        ("Lesson deck", "deck", f"{U4}/(4) BELIEF IN THE AFTERLIFE/(4) BELIEF IN THE AFTERLIFE - ASH.pptx"),
    ]),
    W(27, "u4", "Sikhism and nature", "lesson", [
        ("Lesson deck", "deck", f"{U4}/(5) SIKHISM AND NATURE/(5) SIKHISM AND NATURE - ASH.pptx"),
    ]),
    W(28, "u4", "Summative assessment", "summative", [
        ("Summative paper", "paper", f"{U4}/(6) SUMMATIVE/(6) SUMMATIVE - SIKHISM - ASH.docx"),
        ("Revision questions", "doc", f"{U4}/(6) SUMMATIVE/(6) REVISION QUESTIONS - SIKHISM.docx"),
        ("Lesson deck", "deck", f"{U4}/(6) SUMMATIVE/(6) SUMMATIVE - ASH.pptx"),
        ("DIT deck", "deck", f"{U4}/(6) SUMMATIVE/(6) DIT - SUMMATIVE - SIKHISM - ASH.pptx"),
    ]),
    # ---- Unit 5: Heroes of Faith -------------------------------------------
    W(29, "u5", "Gandhi", "lesson", [
        ("Lesson deck", "deck", f"{U5}/(1) GANDHI/(1) GANDHI - ASH.pptx"),
        ("Worksheet — comprehension", "doc", f"{U5}/(1) GANDHI/(1) WORKSHEET - GANDHI COMPREHENSION - ASH.docx"),
        ("Worksheet — mind map", "doc", f"{U5}/(1) GANDHI/(1) WORKSHEET - GANDHI MIND MAP - ASH.docx"),
    ]),
    W(30, "u5", "Nelson Mandela", "lesson", [
        ("Lesson deck", "deck", f"{U5}/(2) MANDELA/(2) MANDELA - ASH.pptx"),
        ("Worksheet — questions", "doc", f"{U5}/(2) MANDELA/(2) WORKSHEET - HIS WALK TO FREEDOM QUESTIONS - ASH.docx"),
        ("Information (PDF)", "doc", f"{U5}/(2) MANDELA/(2) WORKSHEET - HIS WALK TO FREEDOM INFORMATION - ASH.pdf"),
    ]),
    W(31, "u5", "Martin Luther King", "lesson", [
        ("Lesson deck", "deck", f"{U5}/(3) MLK/(3) MLK - ASH.pptx"),
        ("Worksheet — gap fill", "doc", f"{U5}/(3) MLK/(3) WORKSHEET - GAP FILL - ASH.docx"),
    ]),
    W(32, "u5", "Malala Yousafzai", "lesson", [
        ("Lesson deck", "deck", f"{U5}/(4) MALALA/(4) MALALA - ASH.pptx"),
        ("Worksheet — questions", "doc", f"{U5}/(4) MALALA/(4) WORKSHEET - MALALA QUESTIONS - ASH.docx"),
        ("Information (PDF)", "doc", f"{U5}/(4) MALALA/(4) WORKSHEET - MALALA INFO - ASH.pdf"),
    ]),
    # ---- Unit 6: Film and Faith --------------------------------------------
    W(33, "u6", "Religious meaning in film", "lesson", [
        ("Lesson deck", "deck", f"{U6}/(1) RELIGIOUS MEANINGS IN FILM - ASH.pptx"),
    ]),
    W(34, "u6", "Prayer in films", "lesson", [
        ("Lesson deck", "deck", f"{U6}/(2) PRAYER IN FILMS - ASH.pptx"),
    ]),
    W(35, "u6", "Temptation in movies", "lesson", [
        ("Lesson deck", "deck", f"{U6}/(3) TEMPTATION IN MOVIES - ASH.pptx"),
    ]),
    W(36, "u6", "Resurrection in movies", "lesson", [
        ("Lesson deck", "deck", f"{U6}/(4) RESURRECTION IN MOVIES - ASH.pptx"),
    ]),
    # ---- End of year -------------------------------------------------------
    W(37, "eoy", "End of Year exam", "exam", [
        ("Exam paper", "paper", f"{UE}/YR 7 - EOY EXAM.docx"),
        ("Revision", "doc", f"{UE}/EOY7 REVISION - ASH.docx"),
        ("DIT deck", "deck", f"{UE}/EOY DIT - ASH.pptx"),
    ], note="Revise first, sit the paper, then run the DIT — the folder holds "
            "all three, so plan whether this needs one week or two."),
    W(38, "eq", "Equality Week", "lesson", [
        ("Alan Turing deck", "deck", f"{UQ}/ALAN TURING.pptx"),
        ("Complete the missing words", "doc", f"{UQ}/COMPLETE THE MISSING WORDS.docx"),
        ("Prince of Egypt task", "doc", f"{UQ}/PRINCE OF EGYPT ASH.docx"),
    ]),
]

SUMMARIES = {
    1: "The first RE lesson of secondary school: what Religious Education is, "
       "and why it is worth studying when 7 of the world's 8 billion people "
       "hold a religious belief. Sets the expectations students will work to "
       "all year.",
    2: "A baseline test taken before any teaching, so progress across Year 7 "
       "can be measured against it. Covers holy books, places of worship, "
       "founders and the words theism, atheism and polytheism, followed by "
       "the DIT lesson.",
    3: "The distinction the whole unit rests on: a belief is accepted as true, "
       "a fact can be proven, an opinion says how someone feels. Students sort "
       "statements into the three and learn why people can hold different "
       "beliefs honestly.",
    4: "Optical illusions open the question of whether the eye can be trusted, "
       "then the lesson turns to theism, atheism and agnosticism, and to the "
       "ways belief is shown in practice — Christian prayer and Jummah prayer.",
    5: "Do people have good reasons for believing in God, or for not believing? "
       "Students weigh evidence, meet the theist, the atheist and the agnostic "
       "as three positions rather than three camps, and argue their own view.",
    6: "Objects that carry belief: rosary beads, the crucifix, the prayer mat "
       "and the compass that points towards Mecca. Students handle the "
       "artefacts, then explain what each one tells you about the believer "
       "who uses it.",
    7: "The cross, Aum, the Dharma Wheel, the Star of David and the crescent "
       "moon and star. Students learn to read a symbol as a compressed belief "
       "— and to see why a sign and a symbol are not the same thing.",
    8: "The unit assessment: belief, fact and opinion, the three positions on "
       "God, prayer, artefacts and symbols. Revision questions first, then the "
       "paper, then the DIT lesson that closes the gaps it finds.",
    9: "Diwali, the festival of lights, told through Rama and Sita's return "
       "from exile and Hanuman's part in it. Students learn why the divas are "
       "lit and what light defeating darkness means to a Hindu family.",
    10: "The formative assessment for the unit: students design a poster "
        "explaining one of the Big Six religions to an alien — its founder, "
        "symbol, holy book, age, size and afterlife belief. Aum is taught "
        "properly here.",
    11: "Inside a Hindu place of worship. The mandir, the murti that houses "
        "the deity, the puja that is offered and the Vedas that are read — "
        "explored through a virtual tour and the accompanying information "
        "sheet.",
    12: "What Hindus believe happens after death: the atman that never dies, "
        "samsara as the cycle of rebirth, and moksha as release from it. "
        "Students trace how the life you live shapes the life that follows.",
    13: "Brahman is in everything, so harming the natural world harms the "
        "divine. Karma is introduced through selfless and selfish acts, and "
        "students argue what a Hindu should do about the environment today.",
    14: "The Hinduism assessment: Diwali, the symbols of the Big Six, the "
        "mandir and puja, atman and samsara and moksha, karma and the "
        "Trimurti. Two sets of revision questions, then the paper and the DIT.",
    15: "A prince who had never seen suffering leaves the palace at 29, sees "
        "the Four Sights, and meditates for 46 days under the Bodhi tree. How "
        "Siddhartha Gautama became the Buddha — the Enlightened One.",
    16: "Wesak, the most important festival in Buddhism, celebrating the "
        "Buddha's birth, enlightenment and death. Students learn the Bathing "
        "of the Buddha and what purifying the heart and mind is meant to "
        "achieve.",
    17: "The vihara as temple, school and community all at once. Puja, "
        "chanting and mantras, and meditation as the discipline of "
        "controlling the mind — taken through a virtual tour of the building.",
    18: "A short formative test halfway through the unit: the Buddha, Wesak "
        "and the vihara, plus karma and reincarnation carried over from "
        "Hinduism. The DIT models how to explain two Buddhist teachings.",
    19: "The Four Noble Truths — that life involves suffering, that desire "
        "causes it, that it can be ended, and that the Eightfold Path is the "
        "way — and what Buddhists mean by escaping samsara into nirvana.",
    20: "Sentient and non-sentient beings, and why the distinction matters to "
        "a Buddhist deciding how to treat animals and the land. The Middle "
        "Way is applied to how much a person really needs to own.",
    21: "The Buddhism assessment: ten key words, the Tripitaka, two ways "
        "Wesak is celebrated, two of the Four Noble Truths, and why "
        "Buddhists want to reach nirvana. Revision, paper, then the DIT.",
    22: "Born in the Punjab in 1469, Guru Nanak refused the Sacred Thread "
        "Ceremony and taught that there is one God and that all people are "
        "equal. Nine Gurus followed him, and homework covers all ten.",
    23: "Kesh, kangha, kara, kachera and kirpan — the five artefacts a "
        "baptised Sikh wears, what each one means, and how the Khalsa began "
        "at Vaisakhi in 1699 under Guru Gobind Singh.",
    24: "The gurdwara, the Guru Granth Sahib treated as a living Guru, and "
        "the langar where everyone sits on the same floor and eats the same "
        "free meal — equality made visible in a building.",
    25: "The formative test on the first half of the unit: Guru Nanak, the "
        "ten Gurus, the Khalsa and Vaisakhi, the 5Ks, the gurdwara and "
        "langar, and the words sewa, karma, mukti and atman.",
    26: "Waheguru, the atma given to every living being, samsara as the cycle "
        "of rebirth and mukti as release from it. Gurmukh and manmukh living "
        "explain how good and bad karma are earned.",
    27: "Sikhism has no creation story, so the teaching starts from "
        "stewardship: the world is held in trust for those who come after. "
        "Students turn that into practical action — recycling, clean energy, "
        "local food.",
    28: "The Sikhism assessment: ten key words, two Sikh beliefs about the "
        "afterlife, two about nature, and an outline of two of the 5Ks. "
        "Students are held to a Point and a Develop in every answer.",
    29: "Gandhi in South Africa, the racism he met there, and ahimsa — the "
        "principle of harming no living thing. His ashram is used to ask what "
        "living your belief actually costs.",
    30: "Apartheid meant 'the state of being apart', and in South Africa it "
        "was written into law. Mandela's belief in equality, the 27 years in "
        "prison it cost him, and what he chose to do afterwards.",
    31: "Segregation in America, where racism comes from, and Martin Luther "
        "King's answer to it. The I Have a Dream speech is read against the "
        "Christian belief that all people are made in the image of God.",
    32: "Born in Mingora in 1997, banned from school in 2008, awarded the "
        "Nobel Peace Prize in 2014. Malala's story is set against what Islam "
        "teaches about the education of men and women.",
    33: "Narnia read as Christian belief in disguise: a wrong choice, a price "
        "that has to be paid, a death in someone else's place and a return "
        "from the dead. Students learn to read a story symbolically.",
    34: "Three film prayers — a coach's, a woman's in the cathedral, a boy's "
        "in an empty church — used to separate personal prayer from corporate "
        "prayer, and to ask what people actually pray for.",
    35: "Temptation as wanting to do what you know is wrong. Adam and Eve are "
        "read as a story about choice and consequence, then the same shape is "
        "found in a children's film students already know.",
    36: "Why so many heroes die and come back. Resurrection as a belief held "
        "by Jews, Christians and Muslims, set beside Harry Potter and "
        "Superman, and the question of what makes the religious version "
        "different.",
    37: "The End of Year exam covering all six units, with the revision "
        "document to prepare and the DIT deck to run afterwards.",
    38: "Equality Week closes the year: Alan Turing's story and what was done "
        "to him, alongside the Prince of Egypt task.",
}

LEARNING_JOURNEY = "RESOURCES/YEAR 7 LEARNING JOURNEY.docx"
EXPECTATIONS = "RESOURCES/EXPECTATIONS PPT.pptx"

KINDS = {
    "lesson":    ("Lesson", "k-lesson"),
    "formative": ("Formative", "k-form"),
    "summative": ("Summative", "k-summ"),
    "revision":  ("Revision", "k-rev"),
    "exam":      ("Exam", "k-exam"),
    "dit":       ("DIT", "k-dit"),
}
ICON = {"deck": "▶", "doc": "▤", "paper": "✎"}

CSS = """
:root{
  --paper:#FDFAF7; --card:#FFFFFF; --ink:#1F1611; --ink-2:#57463B;
  --ink-3:#867467; --rule:#EBDFD5; --rule-2:#F5EDE6;
  --orng:#C2410C; --orng-2:#8A3208; --orng-wash:#FFF1E8; --on-orng:#FFFFFF;
  --brass:#8A5C0B; --brass-wash:#FBF3E2;
  --teal:#0B3D36; --teal-wash:#E7F0EE;
  --shadow:0 1px 2px rgba(31,22,17,.05), 0 8px 24px -16px rgba(31,22,17,.28);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#171210; --card:#221A16; --ink:#F4ECE5; --ink-2:#C6B5A8;
    --ink-3:#96857A; --rule:#3A2C23; --rule-2:#2A2019;
    --orng:#FDA96A; --orng-2:#D98A4E; --orng-wash:#2E1B0E; --on-orng:#2B1206;
    --brass:#E2B45A; --brass-wash:#2A2113;
    --teal:#7FC8B8; --teal-wash:#12241F;
    --shadow:0 1px 2px rgba(0,0,0,.5), 0 10px 30px -18px rgba(0,0,0,.8);
  }
}
:root[data-theme="dark"]{
  --paper:#171210; --card:#221A16; --ink:#F4ECE5; --ink-2:#C6B5A8;
  --ink-3:#96857A; --rule:#3A2C23; --rule-2:#2A2019;
  --orng:#FDA96A; --orng-2:#D98A4E; --orng-wash:#2E1B0E; --on-orng:#2B1206;
  --brass:#E2B45A; --brass-wash:#2A2113;
  --teal:#7FC8B8; --teal-wash:#12241F;
  --shadow:0 1px 2px rgba(0,0,0,.5), 0 10px 30px -18px rgba(0,0,0,.8);
}

*{box-sizing:border-box}
body{margin:0; background:var(--paper); color:var(--ink);
  font-family:"Public Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  font-size:16px; line-height:1.55; -webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:Newsreader,Georgia,"Times New Roman",serif; font-weight:600;
  text-wrap:balance; margin:0; letter-spacing:-.01em}
a{color:var(--orng)}
.wrap{max-width:1140px; margin:0 auto; padding:0 24px}

.mast{background:var(--orng); color:var(--on-orng); padding:52px 0 40px}
.mast .eyebrow{font-size:12px; letter-spacing:.18em; text-transform:uppercase;
  font-weight:700; opacity:.72}
.mast h1{font-size:clamp(36px,6vw,60px); line-height:1.02; margin:10px 0 0}
.mast p{margin:14px 0 0; max-width:64ch; opacity:.88; font-size:17px}
.mast .top{display:flex; flex-wrap:wrap; gap:10px; margin-top:22px}
.mast .top a{display:inline-flex; align-items:center; gap:8px; text-decoration:none;
  background:rgba(255,255,255,.14); color:var(--on-orng); border:1px solid rgba(255,255,255,.28);
  border-radius:2px; padding:9px 14px; font-size:13.5px; font-weight:600}
.mast .top a:hover{background:rgba(255,255,255,.24)}

nav.jump{position:sticky; top:0; z-index:30; background:var(--paper);
  border-bottom:1px solid var(--rule)}
nav.jump .inner{display:flex; align-items:center; gap:14px; flex-wrap:wrap; padding:10px 0}
nav.jump ul{display:flex; gap:2px; list-style:none; margin:0; padding:0;
  flex-wrap:wrap; flex:1 1 380px}
nav.jump a{display:block; white-space:nowrap; padding:9px 12px; font-size:13px;
  font-weight:600; color:var(--ink-2); text-decoration:none; border-bottom:2px solid transparent}
nav.jump a:hover{color:var(--orng); border-bottom-color:var(--orng)}
nav.jump a:focus-visible,button:focus-visible{outline:2px solid var(--orng); outline-offset:2px}
.filters{display:flex; gap:6px}
.filters button{all:unset; cursor:pointer; font-size:12px; font-weight:700;
  letter-spacing:.06em; text-transform:uppercase; color:var(--ink-3);
  border:1px solid var(--rule); border-radius:2px; padding:6px 11px}
.filters button[aria-pressed="true"]{background:var(--ink); color:var(--paper);
  border-color:var(--ink)}

.unit{margin:46px 0 0; padding-top:24px; border-top:3px solid var(--orng)}
.unit .lab{font-size:11px; letter-spacing:.16em; text-transform:uppercase;
  font-weight:700; color:var(--orng-2)}
.unit h2{font-size:30px; margin:6px 0 0}
.unit p.blurb{color:var(--ink-2); max-width:72ch; margin:8px 0 0; font-size:15px}
.unitres{display:flex; flex-wrap:wrap; gap:8px; margin-top:14px}

.week{background:var(--card); border:1px solid var(--rule); border-radius:3px;
  box-shadow:var(--shadow); margin:14px 0; display:grid;
  grid-template-columns:104px 1fr; overflow:hidden; scroll-margin-top:76px}
@media(max-width:660px){.week{grid-template-columns:1fr}}
.week .num{background:var(--orng-wash); border-right:1px solid var(--rule);
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:1px; padding:16px 8px}
@media(max-width:660px){.week .num{flex-direction:row; gap:10px; border-right:0;
  border-bottom:1px solid var(--rule); justify-content:flex-start; padding:10px 16px;
  align-items:baseline}}
.week .num b{font-family:Newsreader,Georgia,serif; font-size:30px; line-height:1;
  font-variant-numeric:tabular-nums; color:var(--orng)}
.week .num span{font-size:9.5px; letter-spacing:.14em; text-transform:uppercase;
  font-weight:700; color:var(--orng-2)}
.week .num em{font-style:normal; font-size:11px; font-weight:700; color:var(--ink-3);
  font-variant-numeric:tabular-nums; margin-top:3px; white-space:nowrap}
.week .when{font-size:12px; font-weight:600; color:var(--ink-3);
  font-variant-numeric:tabular-nums; white-space:nowrap}
.week.now{border-color:var(--orng); box-shadow:0 0 0 2px var(--orng-wash), var(--shadow)}
.week.now .num{background:var(--orng)}
.week.now .num b, .week.now .num span, .week.now .num em{color:var(--on-orng)}
.week.now .head h3::after{content:"this week"; margin-left:10px; font-family:"Public Sans",sans-serif;
  font-size:10px; letter-spacing:.13em; text-transform:uppercase; font-weight:700;
  color:var(--orng); vertical-align:middle}

.gap{display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;
  margin:16px 0; padding:11px 18px; border-radius:3px}
.gap b{font-size:12px; letter-spacing:.1em; text-transform:uppercase}
.gap span{font-size:13px; font-variant-numeric:tabular-nums}
.gap.break{background:var(--rule-2); color:var(--ink-3)}
.gap.break b{color:var(--ink-2)}
.gap.term{background:var(--orng); color:var(--on-orng)}
.gap.term b{color:var(--on-orng)}
.gap.term span{opacity:.85}

.cal{margin:28px 0 0}
.cal .lab{font-size:11px; letter-spacing:.16em; text-transform:uppercase;
  font-weight:700; color:var(--ink-3); margin-bottom:2px}
.termnote{font-size:13px; color:var(--ink-3); margin:12px 0 0; max-width:82ch}
.terms{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin:22px 0 0}
@media(max-width:760px){.terms{grid-template-columns:1fr}}
.term-card{border:1px solid var(--rule); border-radius:3px; padding:14px 16px;
  background:var(--card)}
.term-card b{display:block; font-size:12px; letter-spacing:.1em; text-transform:uppercase;
  color:var(--orng); margin-bottom:6px}
.term-card span{display:block; font-size:13.5px; color:var(--ink-2);
  font-variant-numeric:tabular-nums}
.term-card span+span{color:var(--ink-3); font-size:12.5px; margin-top:3px}
.nowbtn{all:unset; cursor:pointer; font-size:12px; font-weight:700; letter-spacing:.06em;
  text-transform:uppercase; color:var(--on-orng); background:var(--orng);
  border-radius:2px; padding:7px 12px; white-space:nowrap}
.nowbtn:hover{opacity:.88}
.week .main{padding:16px 20px 18px}
.week .head{display:flex; align-items:baseline; gap:12px; flex-wrap:wrap}
.week h3{font-size:20px}
.week .summary{color:var(--ink-2); font-size:15px; margin:9px 0 0; max-width:76ch}
.week .note{color:var(--ink-3); font-size:13.5px; margin:7px 0 0; max-width:76ch}
.week .note b{color:var(--brass); font-size:10px; letter-spacing:.12em;
  text-transform:uppercase; margin-right:6px}
.res{display:flex; flex-wrap:wrap; gap:8px; margin-top:13px}

.btn{display:inline-flex; align-items:center; gap:7px; text-decoration:none;
  border:1px solid var(--rule); border-radius:2px; padding:8px 12px;
  font-size:13px; font-weight:600; color:var(--ink-2); background:var(--card)}
.btn:hover{border-color:var(--orng); color:var(--orng); background:var(--orng-wash)}
.btn i{font-style:normal; font-size:11px; color:var(--ink-3)}
.btn:hover i{color:var(--orng)}
.btn.ghost{border-style:dashed}

.chip{font-size:10px; letter-spacing:.13em; text-transform:uppercase; font-weight:700;
  padding:4px 9px; border-radius:2px; white-space:nowrap}
.k-lesson{background:var(--rule-2); color:var(--ink-3)}
.k-form{background:var(--brass-wash); color:var(--brass)}
.k-summ{background:var(--ink); color:var(--paper)}
.k-rev{background:var(--teal-wash); color:var(--teal)}
.k-exam{background:var(--orng); color:var(--on-orng)}
.k-dit{background:var(--orng-wash); color:var(--orng)}

.anchor{margin-left:auto; display:inline-flex; gap:6px; align-items:center}
.anchor a, .anchor button{all:unset; cursor:pointer; font-size:11px; font-weight:700;
  letter-spacing:.08em; color:var(--ink-3); font-variant-numeric:tabular-nums;
  border:1px solid var(--rule); border-radius:2px; padding:4px 8px}
.anchor a:hover, .anchor button:hover{color:var(--orng); border-color:var(--orng)}

.notice{background:var(--brass-wash); border-left:3px solid var(--brass);
  padding:14px 18px; margin:26px 0 0; font-size:14.5px; color:var(--ink-2);
  border-radius:0 2px 2px 0}
footer.note{margin:60px 0 80px; padding-top:24px; border-top:1px solid var(--rule);
  color:var(--ink-3); font-size:13.5px; max-width:76ch}
footer.note b{color:var(--ink-2)}
.hidden{display:none !important}
@media (prefers-reduced-motion:reduce){*{animation:none!important; transition:none!important}}"""

JS = """
(function(){
  // Mark the current teaching week, and offer a jump to it.
  var today = new Date(); today.setHours(12,0,0,0);
  var weeks = [].slice.call(document.querySelectorAll('.week[data-start]'));
  var current = null, next = null;
  weeks.forEach(function(w){
    var a = new Date(w.dataset.start + 'T00:00:00');
    var b = new Date(w.dataset.end + 'T23:59:59');
    if (today >= a && today <= b) current = w;
    if (!next && today < a) next = w;
  });
  var target = current || next;
  if (current) current.classList.add('now');
  var btn = document.getElementById('jumpnow');
  if (btn && target) {
    btn.textContent = current ? 'This week' : 'Next lesson';
    btn.addEventListener('click', function(){
      target.scrollIntoView({behavior:'smooth', block:'start'});
      history.replaceState(null, '', '#' + target.id);
    });
  } else if (btn) {
    btn.remove();
  }

  var buttons = document.querySelectorAll('.filters button');
  buttons.forEach(function(b){
    b.addEventListener('click', function(){
      var want = b.dataset.filter;
      buttons.forEach(function(x){ x.setAttribute('aria-pressed', x===b ? 'true':'false'); });
      document.querySelectorAll('.week').forEach(function(w){
        var k = w.dataset.kind;
        var show = want === 'all'
          || (want === 'assess' && (k==='formative'||k==='summative'||k==='exam'||k==='dit'))
          || (want === 'lesson' && k==='lesson')
          || (want === 'rev' && k==='revision');
        w.classList.toggle('hidden', !show);
      });
      document.querySelectorAll('.unit').forEach(function(u){
        var id = u.id, any = false;
        document.querySelectorAll('.week[data-unit="'+id+'"]').forEach(function(w){
          if(!w.classList.contains('hidden')) any = true;
        });
        u.classList.toggle('hidden', !any);
      });
    });
  });
  document.querySelectorAll('button[data-copy]').forEach(function(b){
    b.addEventListener('click', function(){
      var url = location.origin + location.pathname + '#' + b.dataset.copy;
      var done = function(){ var t=b.textContent; b.textContent='copied';
        setTimeout(function(){ b.textContent=t; }, 1400); };
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(url).then(done, done);
      } else {
        var ta=document.createElement('textarea'); ta.value=url; document.body.appendChild(ta);
        ta.select(); try{document.execCommand('copy');}catch(e){} ta.remove(); done();
      }
    });
  });
})();
"""


def gap_after(n):
    """Break and term markers that fall after lesson week n."""
    if n > len(WEEK_DATES) or n >= len(WEEK_DATES):
        return ""
    end = WEEK_DATES[n - 1][1]
    nxt, _ne, nterm = WEEK_DATES[n]
    out = []
    for name, b0, b1, extra in BREAKS:
        if end < b0 and b1 < nxt:
            tail = f"  ·  {extra}" if extra else ""
            out.append(
                f'<div class="gap break"><b>{E(name)}</b>'
                f'<span>{E(daterange(b0, b1))}{tail}</span></div>')
    if nterm != WEEK_DATES[n - 1][2]:
        out.append(
            f'<div class="gap term"><b>{E(nterm)} begins</b>'
            f'<span>Monday {E(dm(nxt))} {nxt.year}</span></div>')
    return "".join(out)


def btn(label, url, icon="", ghost=False):
    i = f'<i>{E(icon)}</i>' if icon else ""
    cls = "btn ghost" if ghost else "btn"
    return (f'<a class="{cls}" href="{E(url)}" target="_blank" rel="noopener">'
            f'{i}<span>{E(label)}</span></a>')


def render():
    NAVNAME = {"eoy": "EOY exam", "eq": "Equality Week"}
    nav = "".join(
        f'<li><a href="#{u["key"]}">{u["n"]}. {E(NAVNAME.get(u["key"], u["name"]))}</a></li>'
        for u in UNITS)
    body = []
    for u in UNITS:
        ur = []
        if u["booklet"]:
            ur.append(btn("Unit booklet", sp(u["booklet"]), "▤"))
        ur.append(btn("Unit folder", sp(u["folder"], folder=True), "❐"))
        for lab, rel in u["resources"]:
            ur.append(btn(lab, sp(rel, folder=rel.endswith("LESSON PLANS")),
                          "❐" if rel.endswith("LESSON PLANS") else "▤"))
        weeks = [w for w in WEEKS if w["unit"] == u["key"]]
        span = (f'Week {weeks[0]["n"]}' if len(weeks) == 1
                else f'Weeks {weeks[0]["n"]}–{weeks[-1]["n"]}') if weeks else ""
        label = "lesson" if len(weeks) == 1 else "lessons"
        body.append(f"""
<section class="unit" id="{u['key']}">
  <div class="lab">Unit {u['n']} · {span} · {len(weeks)} {label}</div>
  <h2>{E(u['name'])}</h2>
  <p class="blurb">{E(u['blurb'])}</p>
  <div class="unitres">{''.join(ur)}</div>
</section>""")
        for w in weeks:
            wstart, wend, _wterm = WEEK_DATES[w["n"] - 1]
            klabel, kcls = KINDS[w["kind"]]
            res = "".join(btn(lab, sp(rel), ICON.get(t, "")) for lab, t, rel in w["res"])
            summ = SUMMARIES.get(w["n"], "")
            summ = f'<p class="summary">{E(summ)}</p>' if summ else ""
            note = f'<p class="note"><b>Note</b> {E(w["note"])}</p>' if w["note"] else ""
            body.append(f"""
<article class="week" id="w{w['n']}" data-unit="{u['key']}" data-kind="{w['kind']}"
         data-start="{wstart.isoformat()}" data-end="{wend.isoformat()}">
  <div class="num"><span>Week</span><b>{w['n']}</b><em>{E(dm(wstart))}</em></div>
  <div class="main">
    <div class="head">
      <h3>{E(w['title'])}</h3>
      <span class="chip {kcls}">{E(klabel)}</span>
      <span class="when">{E(daterange(wstart, wend))}</span>
      <span class="anchor">
        <a href="#w{w['n']}" title="Link to week {w['n']}">#w{w['n']}</a>
        <button type="button" data-copy="w{w['n']}">copy link</button>
      </span>
    </div>
    {summ}{note}
    <div class="res">{res}</div>
  </div>
</article>""")
            body.append(gap_after(w["n"]))

    tspan = {}
    for tname, _ts, _te in TERMS:
        ws = [j + 1 for j, (_m, _e, t) in enumerate(WEEK_DATES) if t == tname]
        tspan[tname] = (ws[0], ws[-1])
    termcards = "".join(
        f'<div class="term-card"><b>{E(tname)}</b>'
        f'<span>{E(dm(ts))} {ts.year} – {E(dm(te))} {te.year}</span>'
        f'<span>Weeks {tspan[tname][0]}–{tspan[tname][1]}</span></div>'
        for tname, ts, te in TERMS)
    spare = len(WEEK_DATES) - len(WEEKS)
    termnote = (
        "Week 1 is the week beginning Monday 7 September 2026 — the Year 7 "
        "induction day on 2 September and the first two days of term fall "
        f"before it. The year holds {len(WEEK_DATES)} teaching weeks and this "
        f"scheme has {len(WEEKS)} lessons"
        + (", one per week with none spare." if spare == 0 else
           f", which leaves {spare} spare at the end for catch-up."))

    doc = f"""<title>Year 7 Weekly</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400&family=Public+Sans:ital,wght@0,400..800;1,400&display=swap">
<style>{CSS}</style>

<header class="mast">
  <div class="wrap">
    <div class="eyebrow">Harlington School · Religious Education · Year 7</div>
    <h1>Year 7, week by week</h1>
    <p>Every lesson of the year in order, with its deck, worksheets and papers
       one click away. Decks open in PowerPoint Online — you need to be signed
       in to your school account.</p>
    <div class="top">
      {btn("Learning Journey", sp(LEARNING_JOURNEY), "▤")}
      {btn("Expectations deck", sp(EXPECTATIONS), "▶")}
      {btn("All Year 7 files", sp("", folder=True), "❐")}
    </div>
  </div>
</header>

<nav class="jump" aria-label="Units and filters">
  <div class="wrap inner">
    <ul>{nav}</ul>
    <div class="filters" role="group" aria-label="Filter weeks">
      <button type="button" data-filter="all" aria-pressed="true">All</button>
      <button type="button" data-filter="lesson" aria-pressed="false">Lessons</button>
      <button type="button" data-filter="assess" aria-pressed="false">Assessments</button>
      <button type="button" data-filter="rev" aria-pressed="false">Revision</button>
    </div>
    <button type="button" id="jumpnow" class="nowbtn">This week</button>
  </div>
</nav>

<main class="wrap">
  <div class="notice"><b>Every week has its own link.</b> Click <b>#w12</b> on any
    week to jump to it, or <b>copy link</b> to send that week to a class — the
    address ends <code>year7.html#w12</code>.</div>
  <section class="cal">
    <div class="lab">Term dates 2026–27</div>
    <div class="terms">{termcards}</div>
    <p class="termnote">{termnote}</p>
  </section>
  {''.join(body)}
  <footer class="note">
    <p><b>Where the files live.</b> Every button points at the RE SharePoint,
      <code>Year 11 / Philosophy / KS3 Ai / KS3 / YEAR 7</code>. Move or rename
      that folder and the links break together — rebuild the page rather than
      editing it by hand.</p>
    <p><b>Unit booklets</b> sit in each unit's own RESOURCES folder. There is no
      Student Companion at Year 7 — the booklets carry the year on their own.</p>
    <p><b>Gaps in the library.</b> Unit 2 has no introduction-to-Hinduism lesson,
      so the unit opens on Diwali; Unit 5 and Unit 6 have no assessment folder.</p>
  </footer>
</main>
<script>{JS}</script>
"""
    open(OUT, "w").write(doc)
    n_links = doc.count('class="btn')
    print(f"wrote {OUT}  ·  {len(WEEKS)} weeks  ·  {n_links} resource buttons")
    return doc


if __name__ == "__main__":
    render()
