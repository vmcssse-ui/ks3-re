"""Check an authored unit JSON against SCHEMA.md, then against the real page fit."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dx import PAGE_BOX

ICONS = set(os.path.splitext(f)[0] for f in os.listdir(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")))
TASK_ICONS = {"bell", "key", "grid", "book-open", "star", "alert-triangle", "zap", "clock"}
LIM = dict(title=30, big_question=90, aim=66, bell=80, keyword=26, caption=55,
           learn_row=42, attrib=60, task=110, stretch_q=90, wordbank=18,
           statement=78, arg=92, how=105, qf=52, gloss=80)

def check(path):
    U = json.load(open(path, encoding="utf8"))
    e = []
    def lim(v, n, what, where):
        if len(v) > n: e.append("%s: %s is %d chars (max %d): %r" % (where, what, len(v), n, v[:60]))
    if U.get("icon") not in ICONS or U.get("icon") in TASK_ICONS:
        e.append("unit icon %r not allowed" % U.get("icon"))
    lim(U["big_question"], LIM["big_question"], "unit big_question", "unit")
    if len(U["glossary"]) != 16: e.append("glossary has %d entries, need 16" % len(U["glossary"]))
    for g in U["glossary"]:
        lim(g["d"], LIM["gloss"], "glossary definition", "glossary %r" % g["w"])
    for L in U["lessons"]:
        w = "L%s" % L["n"]
        if L.get("icon") not in ICONS or L.get("icon") in TASK_ICONS:
            e.append("%s: icon %r not allowed" % (w, L.get("icon")))
        lim(L["title"], LIM["title"], "title", w)
        lim(L["big_question"], LIM["big_question"], "big_question", w)
        if len(L["aims"]) != 3: e.append("%s: need 3 aims" % w)
        for a in L["aims"]: lim(a, LIM["aim"], "aim", w)
        if len(L["bell"]["questions"]) != 3: e.append("%s: need 3 bell questions" % w)
        for q in L["bell"]["questions"]: lim(q, LIM["bell"], "bell question", w)
        if len(L["keywords"]) != 4: e.append("%s: need 4 keywords" % w)
        for k in L["keywords"]: lim(k, LIM["keyword"], "keyword", w)
        lim(L["learn"]["caption"], LIM["caption"], "learn caption", w)
        if len(L["learn"]["rows"]) != 5: e.append("%s: need 5 learn rows" % w)
        for r in L["learn"]["rows"]: lim(r, LIM["learn_row"], "learn row", w)
        ql = len(L["source"]["quote"])
        if not (80 <= ql <= 185): e.append("%s: quote is %d chars (want 90-180)" % (w, ql))
        lim(L["source"]["attrib"], LIM["attrib"], "attrib", w)
        lim(L["source"]["task"], LIM["task"], "source task", w)
        lim(L["stretch"]["question"], LIM["stretch_q"], "stretch question", w)
        if len(L["stretch"]["wordbank"]) != 5: e.append("%s: need 5 word-bank items" % w)
        for x in L["stretch"]["wordbank"]: lim(x, LIM["wordbank"], "word bank item", w)
        if len(L["stretch"]["starters"]) != 4: e.append("%s: need 4 starters" % w)
        lim(L["debate"]["statement"], LIM["statement"], "debate statement", w)
        for side in ("agree", "disagree"):
            if len(L["debate"][side]) != 2: e.append("%s: need 2 %s arguments" % (w, side))
            for a in L["debate"][side]: lim(a, LIM["arg"], "%s argument" % side, w)
        lim(L["debate"]["how_to_win"], LIM["how"], "how_to_win", w)
        if len(L["quickfire"]) != 6: e.append("%s: need 6 quick-fire questions" % w)
        for q in L["quickfire"]: lim(q["q"], LIM["qf"], "quick-fire question", w)
        for s in json.dumps(L, ensure_ascii=False):
            pass
    for bad in ("‘", "’", "“", "”"):
        if bad in json.dumps(U, ensure_ascii=False):
            e.append("smart quote %r found - use plain ASCII quotes" % bad)
    return U, e

if __name__ == "__main__":
    U, e = check(sys.argv[1])
    for x in e: print("ERR", x)
    if not e:
        from build import build
        import tempfile
        fits = build(sys.argv[1], tempfile.mktemp(suffix=".docx"))
        over = [f for f in fits if f[1] > PAGE_BOX or f[2] > PAGE_BOX]
        for n, a, b in fits:
            print("lesson %-2d A %5d (%+5d)  B %5d (%+5d)%s"
                  % (n, a, a - PAGE_BOX, b, b - PAGE_BOX,
                     "  <-- OVERFLOW" if a > PAGE_BOX or b > PAGE_BOX else ""))
        print("OK" if not over else "OVERFLOWING PAGES: %d" % len(over))
    else:
        print("%d schema errors" % len(e))
        sys.exit(1)
