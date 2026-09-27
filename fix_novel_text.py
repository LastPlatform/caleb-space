# -*- coding: utf-8 -*-
"""Apply 5 punctuation fixes to novel.html (09.21 fragment), with on-disk verification.
Needles are the short forms mechanically confirmed count==1 by the scan."""
import sys

P = "novel.html"
REPLS = [
    ("时间是 5:10", "时间是5:10"),
    ("早上 7:30", "早上7:30"),
    ("压的我手", "压得我手"),
    ("迷迷糊糊的睡着", "迷迷糊糊地睡着"),
    ("充满活力的干", "充满活力地干"),
]

data = open(P, "rb").read()
text = data.decode("utf-8")

ok = True
for old, new in REPLS:
    n = text.count(old)
    print("pre  count %-12r = %d" % (old, n))
    if n != 1:
        ok = False
if not ok:
    print("ABORT: needle counts != 1")
    sys.exit(1)

for old, new in REPLS:
    text = text.replace(old, new)

open(P, "wb").write(text.encode("utf-8"))

# re-read from disk and verify
t2 = open(P, "rb").read().decode("utf-8")
all_ok = True
for old, new in REPLS:
    a = new in t2
    b = old not in t2
    status = "OK" if (a and b) else "FAIL"
    if not (a and b):
        all_ok = False
    print("post %-16r in=%s  old_gone=%s  %s" % (new, a, b, status))

lines = t2.splitlines()
print("total lines:", len(lines))
for ln in (249, 261, 266, 267, 269):
    print("L%d: %s" % (ln, lines[ln - 1][:80]))
print("RESULT:", "ALL APPLIED" if all_ok else "SOME FAILED")
