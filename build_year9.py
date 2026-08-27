# -*- coding: utf-8 -*-
"""Year 9 week-by-week page.

Resources live on the school SharePoint; every button is an absolute
path-style URL with ?web=1 so decks open in PowerPoint Online rather than
downloading. URL-encode with quote(part, safe="()'") — parentheses and
apostrophes stay literal, '+' must become %2B (it appears in
"(5) MARRIAGE AND THE SACRED + D TYPE").
"""
import html, os
from urllib.parse import quote

E = lambda s: html.escape(str(s), quote=True)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "year9.html")

SP_BASE = "https://hs365.sharepoint.com"
SP_ROOT = "/sites/HS_Subjects_RE/Year 11/Philosophy/KS3 Ai/KS3/YEAR 9"


def sp(rel, folder=False):
    parts = (SP_ROOT + "/" + rel).split("/")
    path = "/".join(quote(p, safe="()'").replace("+", "%2B") for p in parts)
    if folder:
        return (f"{SP_BASE}/sites/HS_Subjects_RE/Year%2011/Forms/AllItems.aspx"
                f"?id={quote(SP_ROOT + '/' + rel, safe='')}")
    return f"{SP_BASE}{path}?web=1"


# --------------------------------------------------------------- the units
U1 = "1. HUMANISM AND SOCIETY"
U2 = "2. CHRISTIANITY AND SOCIETY"
U3 = "3. HUMANISM AND THE LAW"
U4 = "4. ISLAM AND THE LAW"
U5 = "5. ISLAM AND FORGIVENESS"
UE = "END OF YEAR TEST"

UNITS = [
    dict(key="u1", n=1, name="Humanism and Society", folder=U1,
         blurb="Marriage as a civil right, sexual relationships, family planning "
               "and equality — Humanist and Christian views side by side.",
         booklet=f"{U1}/Y9_Unit1_Humanism_and_Society_Booklet.docx",
         resources=[("Unit cover (Publisher)", "RESOURCES/Y9 1 - Humanism and Society (1).pub")]),
    dict(key="u2", n=2, name="Christianity and Society", folder=U2,
         blurb="Assistance for families, divorce and remarriage, equality at home, "
               "and gender prejudice and discrimination.",
         booklet=f"{U2}/Y9_Unit2_Christianity_and_Society_Booklet.docx",
         resources=[("Bell work — definitions", f"{U2}/RESOURCES/(1) BELL WORK - DEFINITIONS - ASH.docx"),
                    ("Bell work — wordsearch", f"{U2}/RESOURCES/(2) BELL WORK - WORDSEARCH - ASH.docx"),
                    ("b-type method deck", f"{U2}/RESOURCES/Y9 b-type.pptx"),
                    ("Focus sheet", f"{U2}/RESOURCES/New Unit - Focus sheet.pptx"),
                    ("Feedback sheet (staff)", f"{U2}/RESOURCES/CHRISTIANITY AND SOCIETY FEEDBACK SHEET ASH ONLY.docx"),
                    ("Unit booklet (Publisher)", f"{U2}/RESOURCES/Y9 1 - Christianity and Society (1).pub"),
                    ("Cover (Publisher)", f"{U2}/RESOURCES/Y9 1 - Cover.pub")]),
    dict(key="u3", n=3, name="Humanism and the Law", folder=U3,
         blurb="Crime, human rights, attitudes to punishment, restorative justice, "
               "and moral and natural evil.",
         booklet=f"{U3}/Y9_Unit3_Humanism_and_the_Law_Booklet.docx",
         resources=[("Key words deck", f"{U3}/RESOURCES/Key words.pptx"),
                    ("D-type practice", f"{U3}/RESOURCES/D-type practice.pptx"),
                    ("D-type — Humanism and the Law", f"{U3}/RESOURCES/Yr 9 Humanism and the Law D type.pptx"),
                    ("Unit booklet (Publisher)", f"{U3}/RESOURCES/Y9 2 - Humanism and Law.pub")]),
    dict(key="u4", n=4, name="Islam and the Law", folder=U4,
         blurb="Islam and justice, Islam and crime, the Qur'an and the hadd, and "
               "the aims of punishment.",
         booklet=f"{U4}/Y9_Unit4_Islam_and_the_Law_Booklet.docx",
         resources=[("Unit booklet (Publisher)", f"{U4}/RESOURCES/Y9 4 - Islam and Law.pub"),
                    ("Easter task (Publisher)", f"{U4}/RESOURCES/Easter task.pub")]),
    dict(key="u5", n=5, name="Islam and Forgiveness", folder=U5,
         blurb="Treatment of criminals, capital punishment, forgiveness, and the "
               "question of God.",
         booklet=f"{U5}/Y9_Unit5_Islam_and_Forgiveness_Booklet.docx",
         resources=[]),
    dict(key="eoy", n=6, name="End of Year Test", folder=UE,
         blurb="Two High 5 revision lessons, the definition sheets, the paper "
               "itself and the DIT that follows it.",
         booklet=None,
         resources=[]),
]

# --------------------------------------------------------------- the weeks
# kind: lesson · formative · summative · revision · exam · dit
# res:  (label, type, relative path)   type ∈ deck · doc · paper
def W(n, unit, title, kind, res, note=None):
    return dict(n=n, unit=unit, title=title, kind=kind, res=res, note=note)


WEEKS = [
    # ---- Unit 1 -----------------------------------------------------------
    W(1, "u1", "Marriage — Civil Rights", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(1) MARRIAGE - CIVIL RIGHTS/(1) MARRIAGE - ASH.pptx"),
        ("Expectations deck", "deck", f"{U1}/(1) MARRIAGE - CIVIL RIGHTS/(1) EXPECTATIONS PPT - ASH.pptx"),
    ], "First lesson of the year — the expectations deck runs before the content."),
    W(2, "u1", "Sexual Relationships", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(2) SEXUAL RELATIONSHIPS/(2) SEXUAL RELATIONSHIPS - ASH.pptx"),
        ("Bell work — crossword", "doc", f"{U1}/(2) SEXUAL RELATIONSHIPS/(2) BELL WORK - CROSSWORD - ASH.docx"),
    ]),
    W(3, "u1", "Family Planning", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(3) FAMILY PLANNING/(3) FAMILY PLANNING - ASH.pptx"),
        ("Worksheet — contraception statistics", "doc", f"{U1}/(3) FAMILY PLANNING/(3) WORKSHEET - ARTIFICAL CONTRACEPTION STATISTICS - ASH.docx"),
    ]),
    W(4, "u1", "Formative assessment", "formative", [
        ("Formative paper", "paper", f"{U1}/(3A) FORMATIVE/(3A) FORMATIVE - ASH.docx"),
        ("DIT sheet", "doc", f"{U1}/(3A) FORMATIVE/(3A) DIT - FORMATIVE - ASH.docx"),
    ]),
    W(5, "u1", "Equality", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(4) EQUALITY/(4) EQUALITY - ASH.pptx"),
    ]),
    W(6, "u1", "Marriage and the Sacred + D type", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(5) MARRIAGE AND THE SACRED + D TYPE/(5) MARRIAGE AND THE SACRED + D TYPE - ASH.pptx"),
        ("D-type structure deck", "deck", f"{U1}/(5) MARRIAGE AND THE SACRED + D TYPE/(5) D TYPE STRUCTURE - ASH.pptx"),
    ], "The D-type structure deck is the one to reuse before every 12-mark question."),
    W(7, "u1", "Sexual Relationships in Christianity", "lesson", [
        ("Lesson deck", "deck", f"{U1}/(6) SEXUAL RELATIONSHIPS IN CHRISTIANITY/(6) SEXUAL RELATIONSHIPS IN CHRISTIANITY - ASH.pptx"),
        ("Information sheet", "doc", f"{U1}/(6) SEXUAL RELATIONSHIPS IN CHRISTIANITY/(6) SEXUAL RELATIONSHIPS INFORMATION - ASH.docx"),
        ("Worksheet", "doc", f"{U1}/(6) SEXUAL RELATIONSHIPS IN CHRISTIANITY/(6) WORKSHEET - ASH.docx"),
    ]),
    W(8, "u1", "Summative + families lesson", "summative", [
        ("Lesson deck", "deck", f"{U1}/(7) SUMMATIVE + FAMILIES LESSON HW/(7) SUMMATIVE + FAMILIES LESSON HW - ASH.pptx"),
    ], "The summative paper for this unit is not in the folder — only the lesson "
       "deck that runs it."),

    # ---- Unit 2 -----------------------------------------------------------
    W(9, "u2", "Assistance for Families", "lesson", [
        ("Lesson deck", "deck", f"{U2}/(1) ASSISTANCE FOR FAMILIES/(1) ASSISTANCE FOR FAMILIES - ASH.pptx"),
    ]),
    W(10, "u2", "Family Planning", "lesson", [
        ("Lesson deck", "deck", f"{U2}/(2) FAMILY PLANNING/(2) FAMILY PLANNING - ASH.pptx"),
    ]),
    W(11, "u2", "Formative assessment", "formative", [
        ("Formative paper", "paper", f"{U2}/(2A) FORMATIVE/(2A) FORMATIVE - ASH.docx"),
        ("DIT deck", "deck", f"{U2}/(2A) FORMATIVE/(2A) DIT - FORMATIVE - ASH.pptx"),
        ("Homework — human rights poster", "deck", f"{U2}/(2A) FORMATIVE/(2A) HW - FORMATIVE - HUMAN RIGHTS POSTER - ASH.pptx"),
    ]),
    W(12, "u2", "Divorce and Remarriage", "lesson", [
        ("Lesson deck", "deck", f"{U2}/(3) DIVORCE AND REMARRIAGE/(3) DIVORCE AND REMARRIAGE - ASH.pptx"),
    ]),
    W(13, "u2", "Equality of Men and Women in the Home", "lesson", [
        ("Lesson deck", "deck", f"{U2}/(4) EQUALITY OF MEN AND WOMEN IN THE HOME/(4) EQUALITY OF MEN AND WOMEN - ASH.pptx"),
        ("Worksheet — equality at home", "doc", f"{U2}/(4) EQUALITY OF MEN AND WOMEN IN THE HOME/(4) WORKSHEET - EQUALITY AT HOME - ASH.docx"),
    ]),
    W(14, "u2", "Gender Prejudice and Discrimination", "lesson", [
        ("Lesson deck", "deck", f"{U2}/(5) GENDER PREJUDICE AND DISCRIMINATION/(5) GENDER PREJUDICE AND DISCRIMINATION - ASH.pptx"),
    ]),
    W(15, "u2", "Summative 1 and 2 + justice lesson", "summative", [
        ("Summative paper 1", "paper", f"{U2}/(6) SUMMATIVE + JUSTICE LESSON HW/(6) SUMMATIVE - 1 - ASH.docx"),
        ("Summative paper 2", "paper", f"{U2}/(6) SUMMATIVE + JUSTICE LESSON HW/(6) SUMMATIVE - 2 - ASH.docx"),
        ("DIT deck — summative 1", "deck", f"{U2}/(6) SUMMATIVE + JUSTICE LESSON HW/(6) DIT - SUMMATIVE 1 - ASH.pptx"),
        ("DIT deck — summative 2", "deck", f"{U2}/(6) SUMMATIVE + JUSTICE LESSON HW/(6) DIT - SUMMATIVE 2 - ASH.pptx"),
        ("Justice lesson deck", "deck", f"{U2}/(6) SUMMATIVE + JUSTICE LESSON HW/(6) JUSTICE - ASH.pptx"),
    ], "Two papers here — these are Summative Assessments 1 and 2 in the Student Companion."),

    # ---- Unit 3 -----------------------------------------------------------
    W(16, "u3", "Crime", "lesson", [
        ("Lesson deck", "deck", f"{U3}/(1) CRIME/(1) CRIME - ASH.pptx"),
        ("Justice deck", "deck", f"{U3}/(1) CRIME/(6) JUSTICE - ASH.pptx"),
        ("Bell work — definitions", "doc", f"{U3}/(1) CRIME/(1) BELL WORK - DEFINITIONS - ASH.docx"),
    ]),
    W(17, "u3", "Attitudes to Human Rights", "lesson", [
        ("Lesson deck", "deck", f"{U3}/(2) ATTITUDES TO HUMAN RIGHTS/(2) HUMAN RIGHTS - ASH.pptx"),
        ("Worksheet — human rights", "doc", f"{U3}/(2) ATTITUDES TO HUMAN RIGHTS/(2) WORKSHEET - HUMAN RIGHTS - ASH.docx"),
    ]),
    W(18, "u3", "Attitudes to Punishment", "lesson", [
        ("Lesson deck", "deck", f"{U3}/(3) ATTITUDES TO PUNISHMENT/(3) ATTITUDES TO PUNISHMENT - ASH.pptx"),
    ]),
    W(19, "u3", "Formative assessment", "formative", [
        ("Formative paper", "paper", f"{U3}/(3A) FORMATIVE/(3A) FORMATIVE - ASH.docx"),
        ("DIT deck", "deck", f"{U3}/(3A) FORMATIVE/(3A) DIT - FORMATIVE - ASH.pptx"),
    ]),
    W(20, "u3", "Restorative Justice", "lesson", [
        ("Lesson deck", "deck", f"{U3}/(4) RESTORATATIVE JUSTICE/(4) RESTORATATIVE JUSTICE - ASH.pptx"),
        ("Bell work — definitions", "doc", f"{U3}/(4) RESTORATATIVE JUSTICE/(4) BELL WORK - DEFINITIONS - ASH.docx"),
    ]),
    W(21, "u3", "Moral and Natural Evil", "lesson", [
        ("Lesson deck", "deck", f"{U3}/(5) MORAL AND NATURAL EVIL/(5) MORAL AND NATURAL EVIL - ASH.pptx"),
    ]),
    W(22, "u3", "Summative assessment", "summative", [
        ("Summative paper", "paper", f"{U3}/(6) SUMMATIVE/(6) SUMMATIVE - ASH.docx"),
        ("Lesson deck + homework", "deck", f"{U3}/(6) SUMMATIVE/(6) SUMMATIVE + HW - ASH.pptx"),
        ("DIT deck", "deck", f"{U3}/(6) SUMMATIVE/DIT - SUMMATIVE - ASH.pptx"),
    ], "This is Summative Assessment 3 in the Student Companion."),

    # ---- Unit 4 -----------------------------------------------------------
    W(23, "u4", "Islam and Justice", "lesson", [
        ("Lesson deck", "deck", f"{U4}/(1) ISLAM AND JUSTICE/(1) ISLAM AND JUSTICE - ASH.pptx"),
        ("Bell work", "doc", f"{U4}/(1) ISLAM AND JUSTICE/(1) BELL WORK - ASH.docx"),
    ]),
    W(24, "u4", "Islam and Crime", "lesson", [
        ("Lesson deck", "deck", f"{U4}/(2) ISLAM AND CRIME/(2) ISLAM AND CRIME - ASH.pptx"),
    ]),
    W(25, "u4", "The Qur'an and the Hadd", "lesson", [
        ("Lesson deck", "deck", f"{U4}/(3) THE QURAN AND THE HADD/(3) THE QURAN AND THE HADD - ASH.pptx"),
    ]),
    W(26, "u4", "Attitudes to Punishment", "lesson", [
        ("Lesson deck", "deck", f"{U4}/(4) ATTITUDES TO PUNISHMENT/(4) ATTITUDES TO PUNISHMENT - ASH.pptx"),
    ]),
    W(27, "u4", "Formative assessment", "formative", [
        ("Formative paper", "paper", f"{U4}/(4A) FORMATIVE/(4A) FORMATIVE - ASH.docx"),
    ]),
    W(28, "u4", "Aims of Punishment", "lesson", [
        ("Lesson deck", "deck", f"{U4}/(5) AIMS OF PUNISHMENT/(5) AIMS OF PUNISHMENT - ASH.pptx"),
        ("Bell work", "doc", f"{U4}/(5) AIMS OF PUNISHMENT/(5) BELL WORK - ASH.docx"),
    ]),
    W(29, "u4", "Summative assessment", "summative", [
        ("Summative paper", "paper", f"{U4}/(6) SUMMATIVE/(6) SUMMATIVE - ASH.docx"),
        ("Summative questions", "paper", f"{U4}/(6) SUMMATIVE/Year 9 - Summative Questions.docx"),
        ("Lesson deck + homework", "deck", f"{U4}/(6) SUMMATIVE/(6) SUMMATIVE + HW - ASH.pptx"),
        ("DIT deck", "deck", f"{U4}/(6) SUMMATIVE/YR 9 DIT.pptx"),
    ], "This is the Unit Assessment — Islam and Law in the Student Companion."),

    # ---- Unit 5 -----------------------------------------------------------
    W(30, "u5", "Treatment of Criminals", "lesson", [
        ("Lesson deck", "deck", f"{U5}/(1) TREATMENT OF CRIMINALS/(1) TREATMENT OF CRIMINALS - ASH.pptx"),
    ]),
    W(31, "u5", "Capital Punishment", "lesson", [
        ("Lesson deck", "deck", f"{U5}/(2) CAPITAL PUNISHMENT/(2) CAPITAL PUNISHMENT - ASH.pptx"),
    ]),
    W(32, "u5", "Forgiveness", "lesson", [
        ("Lesson deck", "deck", f"{U5}/(3) FORGIVENESS/(3) FORGIVENESS - ASH.pptx"),
    ]),
    W(33, "u5", "The Question of God", "lesson", [
        ("Lesson deck", "deck", f"{U5}/(4) THE QUESTION OF GOD/(4) THE QUESTION OF GOD - ASH.pptx"),
    ]),

    # ---- End of year ------------------------------------------------------
    W(34, "eoy", "High 5 — Marriage and the Family", "revision", [
        ("Revision deck", "deck", f"{UE}/HIGH 5 - MARRIAGE AND THE FAMILY - ASH.pptx"),
        ("Definition sheet", "doc", f"{UE}/MARRIAGE AND FAMILY DEFINITION SHEET - ASH.docx"),
    ]),
    W(35, "eoy", "High 5 — Crime and Punishment", "revision", [
        ("Revision deck", "deck", f"{UE}/HIGH 5 - CRIME AND PUNISHMENT - ASH.pptx"),
        ("Definition sheet", "doc", f"{UE}/CRIME AND PUNISHMENT DEFINITION SHEET - ASH.docx"),
    ]),
    W(36, "eoy", "End of Year Test", "exam", [
        ("The paper", "paper", f"{UE}/YEAR 9 - EOY TEST.docx"),
    ], "Two sections: relationships, then Islam and law. The Companion treats "
       "them as two separate reviews."),
    W(37, "eoy", "End of Year DIT", "dit", [
        ("DIT deck", "deck", f"{UE}/DIT - End of Year Exam.pptx"),
    ]),
]

COMPANION = "Y9 Student Companion.docx"
LEARNING_JOURNEY = "RESOURCES/YEAR 9 LEARNING JOURNEY.docx"
COMPANION_WEB = "https://claude.ai/code/artifact/1f4463ac-d0e5-4d2d-8ad9-4765191b821c"

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
  --paper:#FBF9FC; --card:#FFFFFF; --ink:#1A1520; --ink-2:#4C4256;
  --ink-3:#786C84; --rule:#E4DCEA; --rule-2:#F0EAF3;
  --plum:#3E1163; --plum-2:#6B4A85; --plum-wash:#F4EEF8; --on-plum:#FFFFFF;
  --brass:#8A5C0B; --brass-wash:#FBF3E2;
  --teal:#0B3D36; --teal-wash:#E7F0EE;
  --shadow:0 1px 2px rgba(26,21,32,.05), 0 8px 24px -16px rgba(26,21,32,.28);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#141019; --card:#1C1724; --ink:#EFE9F2; --ink-2:#B9AFC4;
    --ink-3:#8A7F96; --rule:#312839; --rule-2:#241D2C;
    --plum:#C6A4E2; --plum-2:#9E7FBC; --plum-wash:#241A31; --on-plum:#17101F;
    --brass:#E2B45A; --brass-wash:#2A2113;
    --teal:#7FC8B8; --teal-wash:#12241F;
    --shadow:0 1px 2px rgba(0,0,0,.5), 0 10px 30px -18px rgba(0,0,0,.8);
  }
}
:root[data-theme="dark"]{
  --paper:#141019; --card:#1C1724; --ink:#EFE9F2; --ink-2:#B9AFC4;
  --ink-3:#8A7F96; --rule:#312839; --rule-2:#241D2C;
  --plum:#C6A4E2; --plum-2:#9E7FBC; --plum-wash:#241A31; --on-plum:#17101F;
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
a{color:var(--plum)}
.wrap{max-width:1140px; margin:0 auto; padding:0 24px}

.mast{background:var(--plum); color:var(--on-plum); padding:52px 0 40px}
.mast .eyebrow{font-size:12px; letter-spacing:.18em; text-transform:uppercase;
  font-weight:700; opacity:.72}
.mast h1{font-size:clamp(36px,6vw,60px); line-height:1.02; margin:10px 0 0}
.mast p{margin:14px 0 0; max-width:64ch; opacity:.88; font-size:17px}
.mast .top{display:flex; flex-wrap:wrap; gap:10px; margin-top:22px}
.mast .top a{display:inline-flex; align-items:center; gap:8px; text-decoration:none;
  background:rgba(255,255,255,.14); color:var(--on-plum); border:1px solid rgba(255,255,255,.28);
  border-radius:2px; padding:9px 14px; font-size:13.5px; font-weight:600}
.mast .top a:hover{background:rgba(255,255,255,.24)}

nav.jump{position:sticky; top:0; z-index:30; background:var(--paper);
  border-bottom:1px solid var(--rule)}
nav.jump .inner{display:flex; align-items:center; gap:14px; flex-wrap:wrap; padding:10px 0}
nav.jump ul{display:flex; gap:2px; list-style:none; margin:0; padding:0;
  overflow-x:auto; flex:1 1 380px}
nav.jump a{display:block; white-space:nowrap; padding:9px 12px; font-size:13px;
  font-weight:600; color:var(--ink-2); text-decoration:none; border-bottom:2px solid transparent}
nav.jump a:hover{color:var(--plum); border-bottom-color:var(--plum)}
nav.jump a:focus-visible,button:focus-visible{outline:2px solid var(--plum); outline-offset:2px}
.filters{display:flex; gap:6px}
.filters button{all:unset; cursor:pointer; font-size:12px; font-weight:700;
  letter-spacing:.06em; text-transform:uppercase; color:var(--ink-3);
  border:1px solid var(--rule); border-radius:2px; padding:6px 11px}
.filters button[aria-pressed="true"]{background:var(--ink); color:var(--paper);
  border-color:var(--ink)}

.unit{margin:46px 0 0; padding-top:24px; border-top:3px solid var(--plum)}
.unit .lab{font-size:11px; letter-spacing:.16em; text-transform:uppercase;
  font-weight:700; color:var(--plum-2)}
.unit h2{font-size:30px; margin:6px 0 0}
.unit p.blurb{color:var(--ink-2); max-width:72ch; margin:8px 0 0; font-size:15px}
.unitres{display:flex; flex-wrap:wrap; gap:8px; margin-top:14px}

.week{background:var(--card); border:1px solid var(--rule); border-radius:3px;
  box-shadow:var(--shadow); margin:14px 0; display:grid;
  grid-template-columns:86px 1fr; overflow:hidden; scroll-margin-top:76px}
@media(max-width:660px){.week{grid-template-columns:1fr}}
.week .num{background:var(--plum-wash); border-right:1px solid var(--rule);
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:2px; padding:16px 8px}
@media(max-width:660px){.week .num{flex-direction:row; gap:10px; border-right:0;
  border-bottom:1px solid var(--rule); justify-content:flex-start; padding:10px 16px}}
.week .num b{font-family:Newsreader,Georgia,serif; font-size:30px; line-height:1;
  font-variant-numeric:tabular-nums; color:var(--plum)}
.week .num span{font-size:9.5px; letter-spacing:.14em; text-transform:uppercase;
  font-weight:700; color:var(--plum-2)}
.week .main{padding:16px 20px 18px}
.week .head{display:flex; align-items:baseline; gap:12px; flex-wrap:wrap}
.week h3{font-size:20px}
.week .note{color:var(--ink-2); font-size:14px; margin:8px 0 0; max-width:74ch}
.res{display:flex; flex-wrap:wrap; gap:8px; margin-top:13px}

.btn{display:inline-flex; align-items:center; gap:7px; text-decoration:none;
  border:1px solid var(--rule); border-radius:2px; padding:8px 12px;
  font-size:13px; font-weight:600; color:var(--ink-2); background:var(--card)}
.btn:hover{border-color:var(--plum); color:var(--plum); background:var(--plum-wash)}
.btn i{font-style:normal; font-size:11px; color:var(--ink-3)}
.btn:hover i{color:var(--plum)}
.btn.ghost{border-style:dashed}

.chip{font-size:10px; letter-spacing:.13em; text-transform:uppercase; font-weight:700;
  padding:4px 9px; border-radius:2px; white-space:nowrap}
.k-lesson{background:var(--rule-2); color:var(--ink-3)}
.k-form{background:var(--brass-wash); color:var(--brass)}
.k-summ{background:var(--ink); color:var(--paper)}
.k-rev{background:var(--teal-wash); color:var(--teal)}
.k-exam{background:var(--plum); color:var(--on-plum)}
.k-dit{background:var(--plum-wash); color:var(--plum)}

.anchor{margin-left:auto; display:inline-flex; gap:6px; align-items:center}
.anchor a, .anchor button{all:unset; cursor:pointer; font-size:11px; font-weight:700;
  letter-spacing:.08em; color:var(--ink-3); font-variant-numeric:tabular-nums;
  border:1px solid var(--rule); border-radius:2px; padding:4px 8px}
.anchor a:hover, .anchor button:hover{color:var(--plum); border-color:var(--plum)}

.notice{background:var(--brass-wash); border-left:3px solid var(--brass);
  padding:14px 18px; margin:26px 0 0; font-size:14.5px; color:var(--ink-2);
  border-radius:0 2px 2px 0}
footer.note{margin:60px 0 80px; padding-top:24px; border-top:1px solid var(--rule);
  color:var(--ink-3); font-size:13.5px; max-width:76ch}
footer.note b{color:var(--ink-2)}
.hidden{display:none !important}
@media (prefers-reduced-motion:reduce){*{animation:none!important; transition:none!important}}
"""

JS = """
(function(){
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


def btn(label, url, icon="", ghost=False):
    i = f'<i>{E(icon)}</i>' if icon else ""
    cls = "btn ghost" if ghost else "btn"
    return (f'<a class="{cls}" href="{E(url)}" target="_blank" rel="noopener">'
            f'{i}<span>{E(label)}</span></a>')


def render():
    unit_by_key = {u["key"]: u for u in UNITS}
    nav = "".join(f'<li><a href="#{u["key"]}">{u["n"]}. {E(u["name"])}</a></li>'
                  for u in UNITS)

    body = []
    for u in UNITS:
        ur = []
        if u["booklet"]:
            ur.append(btn("Unit booklet", sp(u["booklet"]), "▤"))
        ur.append(btn("Unit folder", sp(u["folder"], folder=True), "❐"))
        for lab, rel in u["resources"]:
            ur.append(btn(lab, sp(rel), "▤"))
        weeks = [w for w in WEEKS if w["unit"] == u["key"]]
        span = f'Weeks {weeks[0]["n"]}–{weeks[-1]["n"]}' if weeks else ""
        body.append(f"""
<section class="unit" id="{u['key']}">
  <div class="lab">Unit {u['n']} · {span} · {len(weeks)} lessons</div>
  <h2>{E(u['name'])}</h2>
  <p class="blurb">{E(u['blurb'])}</p>
  <div class="unitres">{''.join(ur)}</div>
</section>""")
        for w in weeks:
            klabel, kcls = KINDS[w["kind"]]
            res = "".join(btn(lab, sp(rel), ICON.get(t, "")) for lab, t, rel in w["res"])
            note = f'<p class="note">{E(w["note"])}</p>' if w["note"] else ""
            body.append(f"""
<article class="week" id="w{w['n']}" data-unit="{u['key']}" data-kind="{w['kind']}">
  <div class="num"><b>{w['n']}</b><span>Week</span></div>
  <div class="main">
    <div class="head">
      <h3>{E(w['title'])}</h3>
      <span class="chip {kcls}">{E(klabel)}</span>
      <span class="anchor">
        <a href="#w{w['n']}" title="Link to week {w['n']}">#w{w['n']}</a>
        <button type="button" data-copy="w{w['n']}">copy link</button>
      </span>
    </div>
    {note}
    <div class="res">{res}</div>
  </div>
</article>""")

    doc = f"""<title>Year 9 Weekly</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400&family=Public+Sans:ital,wght@0,400..800;1,400&display=swap">
<style>{CSS}</style>

<header class="mast">
  <div class="wrap">
    <div class="eyebrow">Harlington School · Religious Studies · Year 9</div>
    <h1>Year 9, week by week</h1>
    <p>Every lesson of the year in order, with its deck, worksheets and papers
       one click away. Decks open in PowerPoint Online — you need to be signed
       in to your school account.</p>
    <div class="top">
      {btn("Student Companion (Word)", sp(COMPANION), "▤")}
      {btn("Student Companion (web)", COMPANION_WEB, "◧")}
      {btn("Learning Journey", sp(LEARNING_JOURNEY), "▤")}
      {btn("All Year 9 files", sp("", folder=True), "❐")}
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
  </div>
</nav>

<main class="wrap">
  <div class="notice"><b>Every week has its own link.</b> Click <b>#w12</b> on any
    week to jump to it, or <b>copy link</b> to send that week to a class — the
    address ends <code>year9.html#w12</code>.</div>
  {''.join(body)}
  <footer class="note">
    <p><b>Where the files live.</b> Every button points at the RE SharePoint,
      <code>Year 11 / Philosophy / KS3 Ai / KS3 / YEAR 9</code>. Move or rename
      that folder and the links break together — rebuild the page rather than
      editing it by hand.</p>
    <p>Unit 6, Question of God, is not on this page: its two lesson folders
      hold no decks yet. Week 33 keeps the Question of God lesson that sits in
      Unit 5.</p>
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
