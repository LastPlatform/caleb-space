# -*- coding: utf-8 -*-
"""Final mechanical verification of novel.html love-fragment update.
ASCII-only stdout (counts + line numbers + repr of ASCII needles) so the
shell shim cannot mangle the verdict. Chinese needles live only inside this
UTF-8 file, never passed through the shell."""
import re
import sys

P = "novel.html"
t = open(P, "rb").read().decode("utf-8")
ok = True


def chk(label, cond):
    global ok
    ok = ok and cond
    print("%-34s %s" % (label, "OK" if cond else "FAIL"))


# 1. structure
chk("love-entry count == 4", t.count('love-entry-date') == 4)
for d in ("09.20", "09.21", "09.22", "09.27"):
    chk("date %s present" % d, ('love-entry-date">%s<' % d) in t)
chk("blockquote-think count == 3", t.count('blockquote-think') == 3)
chk("panel-fiction open/close", t.count('id="panel-fiction"') == 1 and t.count("<!-- /#panel-fiction -->") == 1)
chk("panel-love open/close", t.count('id="panel-love"') == 1 and t.count("<!-- /#panel-love -->") == 1)
chk("love-gate present", t.count('id="love-gate"') == 1)
chk("love-content close present", t.count("<!-- /#love-content -->") == 1)
chk("section novel-gate gone", 'novel-gate' not in t)
chk("Aleen password present", "Aleen" in t)

# 2. punctuation fixes: new forms exactly once, old forms absent
FIXES = [
    ("5:10 no-space", "时间是5:10", "时间是 5:10"),
    ("7:30 no-space", "早上7:30", "早上 7:30"),
    ("压得我手", "压得我手", "压的我手"),
    ("迷迷糊糊地睡着", "迷迷糊糊地睡着", "迷迷糊糊的睡着"),
    ("充满活力地干", "充满活力地干", "充满活力的干"),
    ("MV都看了一遍", "MV都看了一遍", "MV 都看了一遍"),
]
for label, new, old in FIXES:
    a = t.count(new) == 1
    b = old not in t
    chk("%s: new x1, old gone" % label, a and b)

# 3. key content needles (count==1 each)
NEEDLES = [
    ("09.20 长发开头", "我看到房间地毯上的那一缕长发"),
    ("09.21 门锁声音", "却听到了门锁的声音"),
    ("09.22 Bowlby定义", "这个是来自Bowlby的定义"),
    ("09.22 我爱着她", "我爱着她。"),
    ("09.27 中秋节开头", "中秋节这几天，发生了好多事"),
    ("09.27 葡萄柚蜡烛", "我点燃了那个葡萄柚香味的香薰蜡烛"),
    ("09.27 常驻武汉", "而我接下来会有好几年常驻武汉"),
    ("09.27 留下来最好", "最后能够留下来最好"),
]
for label, needle in NEEDLES:
    chk("%s x1" % label, t.count(needle) == 1)

# 4. 09.27 tail intact
chk("09.27 final sentence", t.count("只是我期望改变她，让她呆久一点，最后能够留下来最好。") == 1)

print("total lines:", len(t.splitlines()))
print("RESULT:", "ALL VERIFIED" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
