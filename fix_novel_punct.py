# -*- coding: utf-8 -*-
"""Mechanically verified punctuation fixes for novel.html (09.21 fragment).

Needles confirmed count==1 by on-disk scan at 2026-04-11 20:51:
  时间是 5:10 @261, 早上 7:30 @267, 压的我手 @266,
  迷迷糊糊的睡着 @266, 充满活力的干 @269

Safety: count==1 assertion per needle, .bak backup,
        post-write re-read from disk, per-fix OK/FAIL table.
"""
import shutil
import sys
import hashlib

P = "novel.html"
data = open(P, "rb").read()
print("sha256 before:", hashlib.sha256(data).hexdigest()[:16])
text = data.decode("utf-8")

REPLS = [
    ("时间是 5:10", "时间是5:10"),
    ("早上 7:30", "早上7:30"),
    ("压的我手", "压得我手"),
    ("迷迷糊糊的睡着", "迷迷糊糊地睡着"),
    ("充满活力的干", "充满活力地干"),
]

# Step 1: assert each needle occurs exactly once before touching anything
for old, new in REPLS:
    n = text.count(old)
    assert n == 1, "count!=1 for %r: %d" % (old, n)

# Step 2: backup, apply, write
shutil.copyfile(P, P + ".bak")
for old, new in REPLS:
    text = text.replace(old, new)
open(P, "wb").write(text.encode("utf-8"))

# Step 3: re-read from disk and verify mechanically
t2 = open(P, "rb").read().decode("utf-8")
ok = True
for old, new in REPLS:
    a = t2.count(new) == 1
    b = old not in t2
    ok = ok and a and b
    print("VERIFY %-22r new_in=%s old_gone=%s -> %s"
          % (new, a, b, "OK" if (a and b) else "FAIL"))

# the 09.27 fragment also contains 迷迷糊糊的 — must remain untouched
print("09.27 迷迷糊糊的 intact:", "我还是迷迷糊糊的" in t2)
print("sha256 after :", hashlib.sha256(open(P, "rb").read()).hexdigest()[:16])
print("RESULT:", "ALL APPLIED" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
