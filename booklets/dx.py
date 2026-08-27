"""WordprocessingML generator for the Harlington KS3 student completion booklets.
Rebuilt from the Year 9 house format (Y9_Unit1 ... .docx), Year 7 edition.

Everything is emitted as raw XML strings. Every vertical measure is in twips and
every line rule is exact, so a page's height is computable before it is rendered.
"""
import os, re, zipfile, shutil
from PIL import ImageFont

# ---------------------------------------------------------------- page geometry
PAGE_W, PAGE_H = 11906, 16838
MAR_T = MAR_B = 680
MAR_L = MAR_R = 794
CONTENT_W = PAGE_W - MAR_L - MAR_R          # 10318
PAGE_BOX  = PAGE_H - MAR_T - MAR_B - 60     # 15418 - the fixed page container
CELL_INSET = 90                             # TableNormal default, each side
TEXT_W = CONTENT_W - 2 * CELL_INSET         # 10138 twips of running text

# ---------------------------------------------------------------- font metrics
_FONTS = {}
_FDIR = "/usr/share/fonts/truetype/liberation/"
def _font(pt, bold=False, italic=False):
    key = (round(pt, 1), bold, italic)
    if key not in _FONTS:
        name = "LiberationSans-%s.ttf" % (
            "BoldItalic" if bold and italic else
            "Bold" if bold else "Italic" if italic else "Regular")
        _FONTS[key] = ImageFont.truetype(_FDIR + name, max(4, int(round(pt * 4))))
    return _FONTS[key]

def text_w(s, sz, bold=False, italic=False, letter_spacing=0, caps=False):
    """Width of s in twips. sz is the w:sz half-point value."""
    if not s: return 0
    if caps: s = s.upper()
    pt = sz / 2.0
    f = _font(pt, bold, italic)
    px = f.getlength(s) / 4.0          # rendered at 4x
    return int(px * 20) + letter_spacing * len(s)

def lines(s, sz, width, bold=False, italic=False, letter_spacing=0, caps=False):
    """How many wrapped lines s occupies in a column `width` twips wide."""
    if not s: return 1
    words, n, cur = s.split(), 1, 0
    space = text_w(" ", sz, bold, italic, letter_spacing)
    for w in words:
        ww = text_w(w, sz, bold, italic, letter_spacing, caps)
        if cur and cur + space + ww > width:
            n += 1; cur = ww
        else:
            cur = cur + (space if cur else 0) + ww
    return n

# ---------------------------------------------------------------- xml helpers
def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def rpr(sz=21, b=False, i=False, caps=False, sp=0, color=None):
    x = '<w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>'
    if b: x += "<w:b/>"
    if i: x += "<w:i/>"
    if caps: x += "<w:caps/>"
    if sp: x += '<w:spacing w:val="%d"/>' % sp
    if color: x += '<w:color w:val="%s"/>' % color
    x += '<w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>' % (sz, sz)
    return x

def run(t, **kw):
    return "<w:r>%s<w:t xml:space=\"preserve\">%s</w:t></w:r>" % (rpr(**kw), esc(t))

BOX = ('<w:pBdr><w:top w:val="single" w:sz="8" w:space="2" w:color="000000"/>'
       '<w:left w:val="single" w:sz="8" w:space="4" w:color="000000"/>'
       '<w:bottom w:val="single" w:sz="8" w:space="2" w:color="000000"/>'
       '<w:right w:val="single" w:sz="8" w:space="4" w:color="000000"/></w:pBdr>')
RULE_HEAVY = '<w:pBdr><w:bottom w:val="single" w:sz="18" w:space="1" w:color="000000"/></w:pBdr>'
RULE_HEAD  = '<w:pBdr><w:bottom w:val="single" w:sz="8" w:space="2" w:color="000000"/></w:pBdr>'
RULE_DOT   = '<w:pBdr><w:bottom w:val="dotted" w:sz="6" w:space="1" w:color="000000"/></w:pBdr>'
RULE_THIN  = '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="000000"/></w:pBdr>'

def p(content="", line=240, before=0, after=0, bdr="", ind=None, jc=None, tabs=None):
    pr = "<w:pPr>" + bdr
    if tabs: pr += '<w:tabs><w:tab w:val="right" w:pos="%d"/></w:tabs>' % tabs
    if ind is not None:
        pr += '<w:ind w:left="%d" w:right="%d"/>' % (ind[0], ind[1])
    pr += ('<w:spacing w:before="%d" w:after="%d" w:line="%d" w:lineRule="exact"/>'
           % (before, after, line))
    if jc: pr += '<w:jc w:val="%s"/>' % jc
    pr += "</w:pPr>"
    return "<w:p>%s%s</w:p>" % (pr, content)

def drawing(rid, emu, uid):
    return ('<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
            '<wp:extent cx="%d" cy="%d"/><wp:docPr id="%d" name="icon"/><a:graphic>'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic><pic:nvPicPr><pic:cNvPr id="%d" name="icon"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
            '<pic:prstGeom prst="rect"><a:avLst/></pic:prstGeom></pic:spPr></pic:pic>'
            '</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
            % (emu, emu, uid, uid + 1, rid, emu, emu)).replace("pic:prstGeom", "a:prstGeom")

def tbl(rows, borders=True, width=CONTENT_W):
    b = "single" if borders else "none"
    sz = 8 if borders else 0
    col = "000000" if borders else "auto"
    edges = "".join('<w:%s w:val="%s" w:sz="%d" w:color="%s"/>' % (e, b, sz, col)
                    for e in ("top", "left", "bottom", "right", "insideH", "insideV"))
    return ('<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:tblBorders>%s</w:tblBorders>'
            '<w:tblLayout w:type="fixed"/></w:tblPr>%s</w:tbl>' % (width, edges, "".join(rows)))

def tr(cells, h):
    return ('<w:tr><w:trPr><w:cantSplit/><w:trHeight w:hRule="exact" w:val="%d"/></w:trPr>%s</w:tr>'
            % (h, "".join(cells)))

def tc(w, body, valign="top"):
    return ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/><w:vAlign w:val="%s"/></w:tcPr>%s</w:tc>'
            % (w, valign, body))

# ---------------------------------------------------------------- building blocks
def ruled(n, line=265, ind_l=0):
    """n dotted answer lines; alternate right inset matches the house file."""
    out = []
    for k in range(n):
        out.append(p("", line=line, bdr=RULE_DOT, ind=(ind_l, 6 if k % 2 else 0)))
    return out, n * line

def task_header(icon_rid, uid, label, aim):
    """Returns (xml, height). Icon is inline at 8pt-ish, then label, tab, AIM chip."""
    c = drawing(icon_rid, 127000, uid)
    c += run("  " + label, sz=21, b=True, caps=True, sp=16)
    c += "<w:r><w:tab/></w:r>" + run(aim, sz=15, b=True, caps=True, sp=14)
    return p(c, line=300, before=170, after=60, bdr=RULE_HEAD, tabs=10198), 170 + 300 + 60

def spacer(h=40):
    return p("", line=h), h

# border `w:space` is in points and adds real vertical padding when rendered
BPAD_RULE  = 20     # dotted / thin rule, space="1"
BPAD_HEAD  = 40     # task-header rule, space="2"
BPAD_HEAVY = 20     # heavy masthead rule, space="1"
BPAD_BOX   = 80     # a merged bordered box: 2pt above + 2pt below
