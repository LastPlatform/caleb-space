# -*- coding: utf-8 -*-
"""Mechanically verified punctuation fixes for novel.html (09.21 fragment).

Needles are the SHORT forms mechanically confirmed count==1 on disk by the
2026-04-11 scan:
  '时间是 5:10'   @261
  '早上 7:30'     @267
  '压的我手'       @266
  '迷迷糊糊的睡着'  @266
  '充满活力的干'    @269

Safety: count==1 assertion per needle, .bak backup, post-write re-read from
disk with per-needle OK/FAIL verdict, context repr printed before replacing,
.bak removed only after full verification passes."""
import hashlib
import os
import shutil
import sys

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

# --- Step 1: mechanical pre-check -----------------------------------------
# Each needle must occur exactly once; print true byte context (repr).
ok = True
for old, new in REPLS:
    n = text.count(old)
    if n != 1:
        print("PRE-FAIL count!=1 for %r: %d" % (old, n))
        ok = False
        continue
    i = text.index(old)
    ctx = text[max(0, i - 14): i + len(old) + 14]
    print("CTX %r @%d -> %r" % (old, i, ctx))

if not ok:
    print("ABORT: pre-check failed, nothing written")
    sys.exit(1)

# --- Step 2: backup, apply, write ------------------------------------------
shutil.copyfile(P, P + ".bak")
for old, new in REPLS:
    text = text.replace(old, new)
open(P, "wb").write(text.encode("utf-8"))

# --- Step 3: re-read from disk, verify mechanically ------------------------
t2 = open(P, "rb").read().decode("utf-8")
all_ok = True
for old, new in REPLS:
    a = t2.count(new) == 1
    b = old not in t2
    status = "OK" if (a and b) else "FAIL"
    if not (a and b):
        all_ok = False
    print("VERIFY %-24r new_count1=%s old_gone=%s -> %s" % (new, a, b, status))

# 09.27 fragment also contains 迷迷糊糊的 — must remain untouched
print("09.27 迷迷糊糊的 intact:", "我还是迷迷糊糊的" in t2)
print("total lines:", len(t2.splitlines()))
print("sha256 after:", hashlib.sha256(t2.encode("utf-8")).hexdigest()[:16])

if all_ok:
    os.remove(P + ".bak")
    print("backup removed (verification passed)")
else:
    print("backup kept at", P + ".bak")

print("RESULT:", "ALL APPLIED" if all_ok else "SOME FAILED")
sys.exit(0 if all_ok else 1)
