# -*- coding: utf-8 -*-
"""Mechanically discover exact byte context around 5 punctuation sites in
novel.html. NO assumed needles: regex-locate each anchor, print repr of the
true bytes (lines + surrounding chars). Output is the single source of truth
for building replacements; nothing is replaced here."""
import os
import re
import sys

P = "novel.html"
text = open(P, "rb").read().decode("utf-8")
lines = text.splitlines()
print("cwd:", os.getcwd())
print("sha256:", __import__("hashlib").sha256(text.encode("utf-8")).hexdigest()[:16])
print("total lines:", len(lines))

# Anchor regexes: anchor word + flexible window, matches regardless of the
# unknown spacing/punctuation variants around it.
ANCHORS = [
    ("5:10",   r"时间是\s*5:10"),
    ("7:30",   r"早上\s*7:30"),
    ("压",     r"压[得的我]\s*我?手"),
    ("迷糊",   r"迷迷糊糊[的地]\s*睡着"),
    ("干",     r"充满活力[的地]\s*干"),
]
for tag, pat in ANCHORS:
    ms = list(re.finditer(pat, text))
    print("== anchor %r  pattern %r  matches=%d" % (tag, pat, len(ms)))
    for m in ms:
        s, e = m.start(), m.end()
        ctx = text[max(0, s - 20): e + 20]
        ln = text.count("\n", 0, s) + 1
        print("   line %d  span(%d,%d)  needle=%r" % (ln, s, e, m.group(0)))
        print("   ctx   %r" % ctx)
        # per-line repr for the exact line
        print("   line-repr %r" % lines[ln - 1])
