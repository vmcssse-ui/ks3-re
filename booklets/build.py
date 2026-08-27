"""Build one Year 7 unit booklet from its authored JSON."""
import os, json, sys, zipfile, shutil
from dx import *

BODY_W = TEXT_W                    # running text width inside the page container
TASK_ICON = {1: "bell", 2: "key", 3: "grid", 4: "book-open", 5: "star",
             6: "alert-triangle", 7: "zap", 8: "clock"}

class Doc:
    def __init__(self):
        self.rels, self.media, self.n = {}, [], 300
        self.uid = 1000
    def icon(self, name):
        if name not in self.rels:
            self.n += 1
            self.rels[name] = "rId%d" % self.n
            self.media.append(name)
        return self.rels[name]
    def nid(self):
        self.uid += 2
        return self.uid

# ----------------------------------------------------------------- page pieces
def wrapped(text, sz, w, **kw):
    return lines(text, sz, w, **kw)

def page_a(D, U, L):
    """Front page of a lesson spread. Returns (chunks, height, elastics)."""
    out, h = [], 0

    # header band -------------------------------------------------------------
    ic = drawing(D.icon(L["icon"]), 868680 // 2, D.nid())
    left = tc(700, p(ic, line=700, jc="center"), "center")
    eyebrow = p(run("UNIT %d  ·  LESSON %d" % (U["unit"], L["n"]),
                    sz=17, b=True, caps=True, sp=30), line=240)
    title_sz = 40 if wrapped(L["title"], 40, 9618 - 180, bold=True) == 1 else 32
    title = p(run(L["title"], sz=title_sz, b=True), line=int(title_sz * 11), )
    right = tc(9618, eyebrow + title, "center")
    out.append(tbl([tr([left, right], 820)], borders=False)); h += 820

    out.append(p("", line=60, bdr=RULE_HEAVY)); h += 60 + BPAD_HEAVY

    # big question + three aims (one merged box) -------------------------------
    bqw = BODY_W - 180 - 100
    bq = "BIG QUESTION:  " + L["big_question"]
    n = wrapped(bq, 20, bqw, bold=True, caps=True, letter_spacing=14)
    out.append(p(run(bq, sz=20, b=True, caps=True, sp=14),
                 line=250, before=70, bdr=BOX, ind=(90, 90)))
    h += 70 + 250 * n
    for k, a in enumerate(L["aims"], 1):
        t = "AIM %d   %s" % (k, a)
        n = wrapped(t, 17, bqw, bold=True, caps=True, letter_spacing=10)
        out.append(p(run(t, sz=17, b=True, caps=True, sp=10),
                     line=225, bdr=BOX, ind=(90, 90)))
        h += 225 * n
    h += BPAD_BOX
    x, dh = spacer(); out.append(x); h += dh

    # TASK 1 bell work --------------------------------------------------------
    x, dh = task_header(D.icon(TASK_ICON[1]), D.nid(), "TASK 1 · Bell work", "AIM 1")
    out.append(x); h += dh + BPAD_HEAD
    ins = L["bell"].get("instruction", "Answer in full sentences.")
    out.append(p(run(ins, sz=18, i=True), line=230, after=30)); h += 230 * wrapped(ins, 18, BODY_W, italic=True) + 30
    q_slots = []
    for i, q in enumerate(L["bell"]["questions"], 1):
        t = "%d   %s" % (i, q)
        nl = wrapped(t, 21, BODY_W, bold=True)
        out.append(p(run(t, sz=21, b=True), line=235, after=20)); h += 235 * nl + 20
        q_slots.append(len(out))
        rl, rh = ruled(2, ind_l=200); out.extend(rl); h += rh + 2 * BPAD_RULE

    # TASK 2 key words --------------------------------------------------------
    x, dh = task_header(D.icon(TASK_ICON[2]), D.nid(), "TASK 2 · Key words", "AIM 1")
    out.append(x); h += dh + BPAD_HEAD
    ins = "Write what each key word means in your own words."
    out.append(p(run(ins, sz=18, i=True), line=230, after=50)); h += 230 + 50
    kw = L["keywords"][:4]
    while len(kw) < 4: kw.append("")
    rows, KW_H = [], 1110
    for r in (0, 1):
        cells = []
        for c in (0, 1):
            w = kw[r * 2 + c]
            body = p(run(w, sz=21, b=True), line=250)
            body += "".join(p("", line=250, bdr=RULE_DOT, ind=(0, 6 if k % 2 else 0))
                            for k in range(3))
            cells.append(tc(5159, body))
        rows.append((cells, KW_H))
    kw_slot = len(out)
    out.append(tbl([tr(c, hh) for c, hh in rows])); h += 2 * KW_H
    x, dh = spacer(); out.append(x); h += dh

    # TASK 3 learn it ---------------------------------------------------------
    x, dh = task_header(D.icon(TASK_ICON[3]), D.nid(), "TASK 3 · Learn it", "AIM 1")
    out.append(x); h += dh + BPAD_HEAD
    cap = L["learn"]["caption"]
    out.append(p(run(cap, sz=19, b=True, i=True), line=235, after=50))
    h += 235 * wrapped(cap, 19, BODY_W, bold=True, italic=True) + 50
    c1, c2 = L["learn"].get("col1", "Idea"), L["learn"].get("col2", "What it means / example")
    hdr = tr([tc(3508, p(run(c1, sz=19, b=True, caps=True, sp=12), line=240)),
              tc(6810, p(run(c2, sz=19, b=True, caps=True, sp=12), line=240))], 340)
    LR = L["learn"]["rows"]
    LH = 1040
    body_rows = [(r, LH) for r in LR]
    learn_slot = len(out)
    out.append(tbl([hdr] + [tr([tc(3508, p(run(r, sz=20, b=True), line=250)),
                                tc(6810, p("", line=200))], hh) for r, hh in body_rows]))
    h += 340 + LH * len(LR)
    x, dh = spacer(); out.append(x); h += dh

    return out, h, {"q_slots": q_slots, "kw_slot": kw_slot, "kw": kw, "KW_H": KW_H,
                    "learn_slot": learn_slot, "hdr": hdr, "rows": LR, "LH": LH,
                    "bell_n": len(L["bell"]["questions"])}

def page_b(D, U, L):
    out, h = [], 0
    # TASK 4 mark it ----------------------------------------------------------
    x, dh = task_header(D.icon(TASK_ICON[4]), D.nid(), "TASK 4 · Mark it · key source", "AIM 2")
    out.append(x); h += dh + BPAD_HEAD
    q = L["source"]["quote"]
    w = BODY_W - 280 - 100
    out.append(p(run("“" + q + "”", sz=21, i=True), line=250, before=40,
                 bdr=BOX, ind=(140, 140)))
    h += 40 + 250 * wrapped(q, 21, w, italic=True)
    at = L["source"]["attrib"]
    out.append(p(run(at, sz=17, b=True), line=225, bdr=BOX, ind=(140, 140)))
    h += 225 * wrapped(at, 17, w, bold=True) + BPAD_BOX
    tk = L["source"]["task"]
    out.append(p(run(tk, sz=19, b=True), line=235, before=90, after=30))
    h += 90 + 235 * wrapped(tk, 19, BODY_W, bold=True) + 30
    mark_slot = len(out)
    rl, rh = ruled(3); out.extend(rl); h += rh + 3 * BPAD_RULE
    x, dh = spacer(); out.append(x); h += dh

    # TASK 5 stretch ----------------------------------------------------------
    x, dh = task_header(D.icon(TASK_ICON[5]), D.nid(), "TASK 5 · Stretch & challenge", "AIM 3")
    out.append(x); h += dh + BPAD_HEAD
    qq = L["stretch"]["question"]
    out.append(p(run(qq, sz=21, b=True), line=250, after=30))
    h += 250 * wrapped(qq, 21, BODY_W, bold=True) + 30
    wb = "WORD BANK:  " + "  ·  ".join(L["stretch"]["wordbank"])
    out.append(p(run(wb, sz=17, b=True, caps=True, sp=12), line=235, after=60,
                 bdr=BOX, ind=(100, 100)))
    h += 235 * wrapped(wb, 17, BODY_W - 200 - 100, bold=True, caps=True, letter_spacing=12) + 60 + BPAD_BOX
    for st in L["stretch"]["starters"]:
        out.append(p(run(st, sz=19, i=True, color="595959"), line=265, bdr=RULE_DOT))
        out.append(p("", line=265, bdr=RULE_DOT, ind=(0, 6)))
        h += 530 + 2 * BPAD_RULE
    x, dh = spacer(); out.append(x); h += dh

    # TASK 6 the big debate ---------------------------------------------------
    x, dh = task_header(D.icon(TASK_ICON[6]), D.nid(), "TASK 6 · The big debate", "AIM 3")
    out.append(x); h += dh + BPAD_HEAD
    st = "“" + L["debate"]["statement"] + "”"
    out.append(p(run(st, sz=21, b=True, i=True), line=250, bdr=BOX, ind=(120, 120), jc="center"))
    h += 250 * wrapped(st, 21, BODY_W - 240 - 100, bold=True, italic=True) + BPAD_BOX
    x, dh = spacer(); out.append(x); h += dh
    DEB_H = 2085
    dcells = []
    for side, label in (("agree", "I AGREE because…"), ("disagree", "I DISAGREE because…")):
        body = p(run(label, sz=19, b=True, caps=True, sp=10), line=250)
        for arg in L["debate"][side]:
            body += p(run("• " + arg, sz=16, i=True), line=210)
        body += p("", line=60)
        body += "".join(p("", line=255, bdr=RULE_DOT, ind=(0, 6 if k % 2 else 0))
                        for k in range(3))
        dcells.append(tc(5159, body))
    deb_slot = len(out)
    out.append(tbl([tr(dcells, DEB_H)])); h += DEB_H
    htw = "HOW TO WIN:  " + L["debate"]["how_to_win"]
    out.append(p(run(htw, sz=16, b=True, caps=True, sp=10), line=225, before=50))
    h += 50 + 225 * wrapped(htw, 16, BODY_W, bold=True, caps=True, letter_spacing=10)

    # TASK 7 quick fire -------------------------------------------------------
    x, dh = task_header(D.icon(TASK_ICON[7]), D.nid(), "TASK 7 · Quick fire · think back", "AIM 1")
    out.append(x); h += dh + BPAD_HEAD
    qf = L["quickfire"][:6]
    rows, QH = [], [845, 845, 1070]
    for r in range(3):
        cells = []
        for c in range(2):
            item = qf[r * 2 + c]
            body = p(run(item["tag"], sz=14, b=True, caps=True, sp=12), line=190)
            body += p(run("%d. %s" % (r * 2 + c + 1, item["q"]), sz=20, b=True), line=225)
            body += p("", line=250, bdr=RULE_DOT)
            cells.append(tc(5159, body))
        rows.append(tr(cells, QH[r]))
    qf_slot = len(out)
    out.append(tbl(rows)); h += sum(QH)
    x, dh = spacer(); out.append(x); h += dh

    # what I learned ----------------------------------------------------------
    c = drawing(D.icon(TASK_ICON[8]), 127000, D.nid())
    c += run("  What I learned today", sz=21, b=True, caps=True, sp=16)
    out.append(p(c, line=300, before=170, after=60, bdr=RULE_HEAD, tabs=10198))
    h += 530 + BPAD_HEAD
    ins = "Write the three most important things you learned this lesson."
    out.append(p(run(ins, sz=19, i=True), line=235, after=30)); h += 235 + 30
    wil_slot = len(out)
    rl, rh = ruled(3); out.extend(rl); h += rh + 3 * BPAD_RULE
    return out, h, {"mark_slot": mark_slot, "wil_slot": wil_slot,
                    "deb_slot": deb_slot, "cells": dcells, "DEB_H": DEB_H,
                    "qf_slot": qf_slot, "qf_rows": rows, "QH": QH}

# ----------------------------------------------------------------- elastic fit
def _apply(out, repl, ins):
    """repl: {index: xml}. ins: list of (index, xml) inserted BEFORE index."""
    for i, x in repl.items():
        out[i] = x
    for i, x in sorted(ins, key=lambda t: -t[0]):
        out.insert(i, x)
    return out

def fit_a(D, U, L):
    out, h, e = page_a(D, U, L)
    slack = PAGE_BOX - h
    repl, ins = {}, []
    # a third ruled line under every bell question
    cost = 265 * e["bell_n"] + BPAD_RULE * e["bell_n"]
    if slack >= cost:
        for s in e["q_slots"]:
            ins.append((s + 2, ruled(1, ind_l=200)[0][0]))
        h += cost; slack -= cost
    # learn-it rows take the next slice
    n_learn = len(e["rows"])
    if n_learn and slack > 0:
        add = min(170, slack // (n_learn + 2))
        if add > 20:
            LH = e["LH"] + add
            repl[e["learn_slot"]] = tbl(
                [e["hdr"]] + [tr([tc(3508, p(run(r, sz=20, b=True), line=250)),
                                  tc(6810, p("", line=200))], LH) for r in e["rows"]])
            h += add * n_learn; slack -= add * n_learn
    # then the key-word boxes
    if slack > 40:
        add = min(260, slack // 2)
        if add > 20:
            KW, rows = e["KW_H"] + add, []
            for r in (0, 1):
                cells = []
                for c in (0, 1):
                    body = p(run(e["kw"][r * 2 + c], sz=21, b=True), line=250)
                    body += "".join(p("", line=250, bdr=RULE_DOT, ind=(0, 6 if k % 2 else 0))
                                    for k in range(3 if add < 250 else 4))
                    cells.append(tc(5159, body))
                rows.append(tr(cells, KW))
            repl[e["kw_slot"]] = tbl(rows)
            h += 2 * add; slack -= 2 * add
    return _apply(out, repl, ins), h

def fit_b(D, U, L):
    out, h, e = page_b(D, U, L)
    slack = PAGE_BOX - h
    repl, ins = {}, []
    step = 265 + BPAD_RULE
    if slack >= step:                      # a fourth mark-it line
        ins.append((e["mark_slot"] + 3, ruled(1)[0][0])); h += step; slack -= step
    if slack >= step:                      # a fourth what-I-learned line
        ins.append((e["wil_slot"] + 3, ruled(1)[0][0])); h += step; slack -= step
    if slack > 60:                         # deepen the debate boxes
        add = min(430, slack)
        repl[e["deb_slot"]] = tbl([tr(e["cells"], e["DEB_H"] + add)])
        h += add; slack -= add
    if slack > 60:                         # and the quick-fire rows
        add = min(140, slack // 3)
        if add > 15:
            qh = [x + add for x in e["QH"]]
            rows = [r.replace('w:val="%d"' % e["QH"][i], 'w:val="%d"' % qh[i], 1)
                    for i, r in enumerate(e["qf_rows"])]
            repl[e["qf_slot"]] = tbl(rows)
            h += add * 3; slack -= add * 3
    return _apply(out, repl, ins), h

# ----------------------------------------------------------------- cover
def cover(D, U):
    out = []
    out.append(p(run("HARLINGTON SCHOOL  ·  RELIGIOUS EDUCATION  ·  YEAR 7",
                     sz=18, b=True, caps=True, sp=40), line=300, before=511, jc="center"))
    out.append(p("", line=80, bdr=RULE_HEAVY))
    out.append(p(drawing(D.icon(U["icon"]), 868680, D.nid()), line=1000, before=639, jc="center"))
    out.append(p(run("UNIT %d" % U["unit"], sz=26, b=True, caps=True, sp=70),
                 line=340, before=191, jc="center"))
    tsz = 56 if lines(U["name"], 56, TEXT_W, bold=True) == 1 else 44
    out.append(p(run(U["name"], sz=tsz, b=True), line=int(tsz * 11), before=191, jc="center"))
    out.append(p("", line=80, before=447, bdr=RULE_HEAVY))
    out.append(p(run(U["big_question"], sz=24, b=True, i=True), line=300, before=479, jc="center"))
    out.append(p(run("Student completion booklet", sz=20, caps=True, sp=30),
                 line=260, before=351, jc="center"))
    out.append(p("", line=575))
    cells = []
    for i, lab in enumerate(("NAME", "CLASS", "TEACHER")):
        body = p(run(lab, sz=17, b=True, caps=True, sp=14), line=230)
        body += p("", line=340, bdr=RULE_THIN)
        cells.append(tc(3439 if i < 2 else 3440, body))
    out.append(tbl([tr(cells, 640)], borders=False))
    c = drawing(D.icon("check-square" if "check-square" in D.rels else "grid"), 127000, D.nid())
    out.append(p(run("Unit glossary  ·  rate yourself", sz=21, b=True, caps=True, sp=16),
                 line=300, before=170, after=60, bdr=RULE_HEAD, tabs=10198))
    out.append(p(run("Tick R, A or G for each word. Come back to this page at the end of every lesson.",
                     sz=18, i=True), line=230, after=50))
    hdr = tr([tc(3095, p(run("KEY WORD", sz=16, b=True, caps=True, sp=12), line=220)),
              tc(6323, p(run("WHAT IT MEANS", sz=16, b=True, caps=True, sp=12), line=220))] +
             [tc(300, p(run(x, sz=16, b=True), line=220, jc="center")) for x in "RAG"], 280)
    rows = [hdr]
    for g in U["glossary"]:
        n = lines(g["d"], 16, 6323 - 180)
        hh = 320 if n == 1 else 210 * n + 110
        rows.append(tr([tc(3095, p(run(g["w"], sz=18, b=True), line=210)),
                        tc(6323, p(run(g["d"], sz=16), line=210))] +
                       [tc(300, p("", line=200)) for _ in "RAG"], hh))
    out.append(tbl(rows))
    return out

# ----------------------------------------------------------------- package
DOCTYPE = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
           'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
           'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
           'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
           'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><w:body>')

SECT = ('<w:sectPr><w:headerReference w:type="default" r:id="rIdH"/>'
        '<w:footerReference w:type="default" r:id="rIdF"/>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="680" w:right="794" w:bottom="680" w:left="794" '
        'w:header="300" w:footer="300" w:gutter="0"/>'
        '<w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr>')

STYLES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" '
          'w:eastAsia="Arial" w:cs="Arial"/><w:sz w:val="21"/><w:szCs w:val="21"/>'
          '<w:lang w:val="en-GB"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr>'
          '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
          '</w:pPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
          '<w:qFormat/></w:style>'
          '<w:style w:type="table" w:default="1" w:styleId="TableNormal">'
          '<w:name w:val="Normal Table"/><w:tblPr><w:tblCellMar>'
          '<w:top w:w="0" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
          '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="90" w:type="dxa"/>'
          '</w:tblCellMar></w:tblPr></w:style></w:styles>')

def header_xml(U):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="BFBFBF"/>'
            '</w:pBdr><w:spacing w:before="0" w:after="0" w:line="200" w:lineRule="exact"/></w:pPr>'
            '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:caps/>'
            '<w:spacing w:val="12"/><w:color w:val="595959"/><w:sz w:val="16"/>'
            '<w:szCs w:val="16"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p></w:hdr>'
            % esc("Harlington School  ·  Year 7 RE  ·  Unit %d: %s" % (U["unit"], U["name"])))

FOOTER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          '<w:p><w:pPr><w:tabs><w:tab w:val="right" w:pos="10318"/></w:tabs>'
          '<w:spacing w:before="0" w:after="0" w:line="200" w:lineRule="exact"/></w:pPr>'
          '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>'
          '<w:color w:val="595959"/><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr>'
          '<w:t xml:space="preserve">Dr Vitor Carvalho · Head of Philosophy, '
          'Religious Education and EPQ</w:t></w:r><w:r><w:tab/></w:r>'
          '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>'
          '<w:color w:val="595959"/><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr>'
          '<w:t xml:space="preserve">Page </w:t></w:r>'
          '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
          '<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')

CT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
      '<Default Extension="xml" ContentType="application/xml"/>'
      '<Default Extension="png" ContentType="image/png"/>'
      '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
      '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
      '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
      '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
      '</Types>')

ROOTRELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/officeDocument" Target="word/document.xml"/></Relationships>')

def page(chunks):
    """Wrap a page's chunks in the fixed-height, non-splitting page container."""
    return tbl([tr([tc(CONTENT_W, "".join(chunks))], PAGE_BOX)], borders=False)

def build(unit_json, outpath, report=None):
    U = json.load(open(unit_json, encoding="utf8"))
    D = Doc()
    body = "".join(cover(D, U))            # cover is emitted bare (no container)
    fits = []
    for L in U["lessons"]:
        ca, ha = fit_a(D, U, L)
        cb, hb = fit_b(D, U, L)
        fits.append((L["n"], ha, hb))
        body += p("", line=1) + page(ca) + p("", line=1) + page(cb)
    doc = DOCTYPE + body + p("", line=1) + SECT + "</w:body></w:document>"

    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/styles" Target="styles.xml"/>'
            '<Relationship Id="rIdH" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/header" Target="header1.xml"/>'
            '<Relationship Id="rIdF" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/footer" Target="footer1.xml"/>')
    for name in D.media:
        rels += ('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/'
                 '2006/relationships/image" Target="media/%s.png"/>' % (D.rels[name], name))
    rels += "</Relationships>"

    with zipfile.ZipFile(outpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT)
        z.writestr("_rels/.rels", ROOTRELS)
        z.writestr("word/document.xml", doc)
        z.writestr("word/_rels/document.xml.rels", rels)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/header1.xml", header_xml(U))
        z.writestr("word/footer1.xml", FOOTER)
        for name in D.media:
            z.write("media/%s.png" % name, "word/media/%s.png" % name)
    if report is not None:
        report.extend(fits)
    return fits

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    fits = build(src, dst)
    bad = [f for f in fits if f[1] > PAGE_BOX or f[2] > PAGE_BOX]
    for n, a, b in fits:
        flag = "  <-- OVERFLOW" if a > PAGE_BOX or b > PAGE_BOX else ""
        print("lesson %-2d  A %5d (%+5d)   B %5d (%+5d)%s"
              % (n, a, a - PAGE_BOX, b, b - PAGE_BOX, flag))
    print("box =", PAGE_BOX, "| overflowing pages:", len(bad))
