# -*- coding: utf-8 -*-
"""Update love fragments in novel.html: revise 09.27, add 09.28x2/09.29/09.30.
Safety: count==1 anchor assertions BEFORE any write, .bak backup, post-write
re-read from disk with per-needle verdicts, ASCII-only stdout.
Also: removes stale debug scripts, updates MEMORY.md love-section line."""
import hashlib
import os
import shutil
import sys

ok = True


def chk(label, cond):
    global ok
    ok = ok and bool(cond)
    print("%-42s %s" % (label, "OK" if cond else "FAIL"))


# ---- 0. cleanup stale debug scripts (mine, superseded) ----
for f in ["fix_novel_text.py", "fix_novel_punct.py", "fix_punct_v2.py",
          "discover_punct_ctx.py", "verify_novel_final.py"]:
    if os.path.exists(f):
        os.remove(f)
        print("removed temp:", f)

P = "novel.html"
data = open(P, "rb").read()
print("sha256 before:", hashlib.sha256(data).hexdigest()[:16])
text = data.decode("utf-8")

# ---- 1. pre-check anchors (each must be exactly 1) ----
A1 = "从我们确认关系，到她说分手，才两个星期。"
A2 = "我不想放弃，单方面的说分手，太过分了。"
A3 = "只是我期望改变她，让她呆久一点，最后能够留下来最好。</p>"
A4 = "      </div><!-- /#love-content -->"
chk("entries == 4 before", text.count("love-entry-date") == 4)
chk("anchor1 (09.27 关系句) x1", text.count(A1) == 1)
chk("anchor2 (单方面的说分手) x1", text.count(A2) == 1)
chk("anchor3 (09.27 段尾) x1", text.count(A3) == 1)
chk("anchor4 (love-content 闭合) x1", text.count(A4) == 1)
chk("09.30 absent before", "09.30" not in text)
chk("戒断反应 absent before", "戒断反应" not in text)
if not ok:
    print("ABORT: pre-check failed, nothing written")
    sys.exit(1)


# ---- 2. build new entries ----
def entry(date, num, paras):
    out = ('        <div class="love-entry">\n'
           '          <div class="love-entry-head">\n'
           '            <span class="love-entry-date">%s</span>\n'
           '            <span class="love-entry-title" data-zh="片段 %d" data-en="Fragment %d">片段 %d</span>\n'
           '          </div>\n'
           '          <div class="prose">\n' % (date, num, num, num))
    for kind, txt in paras:
        if kind == "b":
            out += '            <blockquote class="blockquote-think">%s</blockquote>\n' % txt
        else:
            out += '            <p>%s</p>\n' % txt
    out += '          </div>\n        </div>'
    return out


E5 = entry("09.28", 5, [
    ("p", "感觉就像戒毒后的戒断反应，我六点就醒了，根本没办法睡懒觉。"),
    ("p", "想要和她发消息，但是不行。"),
    ("p", "这是我答应她的边界感。"),
])
E6 = entry("09.28", 6, [
    ("p", "已经是18:00，我今天休息，在寝室呆了一天。"),
    ("p", "我还是在想她，我想到了那天晚上，她脱掉衣服的样子，她的身体非常匀称，腰很细，屁股很丰满，胸部正好是一个拳头的大小，手握上去正正好好。"),
    ("p", "我过去只在电影里面看到过，真上手的时候，其实我挺害怕，怕弄疼了我的恋人。"),
])
E7 = entry("09.29", 7, [
    ("p", "23:20又是干了一天活，整个人都没什么激情。"),
    ("p", "我想去贴贴她，但是不行。"),
    ("p", "我期待着她晚上会出现，但是没有。"),
    ("p", "我听了一晚上的《中环至半山》，有一句话我反反复复听“你说你爱我，该怎么爱我”"),
    ("p", "我不知道怎么才算爱。"),
    ("p", "她喜欢我吗？她爱我吗？"),
    ("p", "她把分享的东西都送回来了，这是不愿意和我再有一分一毫的瓜葛了吗？"),
    ("p", "唉。"),
    ("p", "不想了，不然今晚又睡不着了。"),
])
E8 = entry("09.30", 8, [
    ("p", "今早上班时，她把我之前送给她的安洁莉娜丢到了我的桌子上。"),
    ("p", "瞬间窒息"),
    ("p", "为什么？我想要质问她，但还是停住了。心里满满的都是苦涩。"),
    ("p", "我在上班之前，我还在想进行怎么主动打开对话，先问问她回家的票买到了没有，然后问一问十一的计划。"),
    ("p", "但我一时说不出话。"),
    ("p", "我还是问了，但我弄不懂她的回答。"),
    ("p", "我又把早上预想的话说了出来，没聊几句就结束了。她回家的票没买到，国庆上班。"),
    ("p", "我的思绪回到了过去，她给我看安洁莉娜的动画，然后问我喜不喜欢这种类型的。我当时就在想，是的，你和安洁莉娜一样可爱。"),
    ("p", "后来送这个安洁莉娜的娃娃也是，希望她能和安洁莉娜一样，开开心心的。这个娃娃也是纪念我们的相遇。"),
    ("p", "而现在这个娃娃又回到了我手上。"),
    ("p", "她是对我彻底失望了吗？"),
    ("p", "其实我已经买好了10.5的电影票，本想问问能不能一起去看看电影。"),
    ("p", "这个话已经说不出口了。"),
    ("p", "23:06我还是问了问，看看电影，不出意料地拒绝了。"),
    ("p", "她，全盘拒绝了我"),
    ("p", "没有任何机会"),
    ("p", "我最后写了一段话，但是没发出去："),
    ("b", "我记得我和你讲过，人生中的决定分为两种，一种是以后会后悔的决定，以及，绝不会后悔的决定。喜欢上你，我绝不后悔，你知道这个，就够了。"),
    ("b", "我不接受你的道歉，因为你也没做错什么。"),
    ("b", "人生这本故事书，很漫长，里面的每个故事也终究都会走向结尾，但如何前往故事的最后一页，也分两种方式：一种，就是像你这样，充满悲观和歉意地踏上旅行；而另一种，就是告别昨日，告别自己的歉意，载着祝愿和美好，向以往一样无忧无虑、尽情启程。"),
    ("b", "这样就好"),
])

# ---- 3. apply edits ----
# 3a. 09.27 revisions
text = text.replace(A1, "从我们确认关系，更进一步，到她说分手，才两个星期。")
text = text.replace(A2, "我不想放弃，单方面地说分手，太过分了。")
# 3b. 09.27 three new closing paragraphs
new_tail = (A3
            + "\n            <p>我真的好想永远和她在一起呀。</p>"
            + "\n            <p>我喜欢她的主动，我喜欢她的勇气，她的这些行为对我来说太珍贵了，她可以是我面对未来不确定性的理由。</p>"
            + "\n            <p>活下去不难，而想过好生活很难，比我想象的难得多。</p>")
text = text.replace(A3, new_tail)
# 3c. four new entries before love-content close
insert = E5 + "\n\n" + E6 + "\n\n" + E7 + "\n\n" + E8 + "\n\n"
text = text.replace(A4, insert + A4)

# ---- 4. backup + write ----
shutil.copyfile(P, P + ".bak")
open(P, "wb").write(text.encode("utf-8"))

# ---- 5. post-write verification (re-read from disk) ----
t2 = open(P, "rb").read().decode("utf-8")
print("sha256 after :", hashlib.sha256(t2.encode("utf-8")).hexdigest()[:16])
chk("entries == 8 after", t2.count("love-entry-date") == 8)
for d, c in [("09.20", 1), ("09.21", 1), ("09.22", 1), ("09.27", 1),
             ("09.28", 2), ("09.29", 1), ("09.30", 1)]:
    chk("date %s x%d" % (d, c), t2.count('love-entry-date">%s<' % d) == c)
chk("09.27 更进一步", t2.count("从我们确认关系，更进一步，到她说分手") == 1)
chk("09.27 old 关系句 gone", A1 not in t2)
chk("单方面地说分手 x1", t2.count("单方面地说分手") == 1)
chk("old 单方面的说分手 gone", "单方面的说分手" not in t2)
chk("09.27 永远在一起", t2.count("我真的好想永远和她在一起呀") == 1)
chk("09.27 珍贵/理由", t2.count("她可以是我面对未来不确定性的理由") == 1)
chk("09.27 活下去不难", t2.count("活下去不难，而想过好生活很难") == 1)
chk("片段5 戒断反应", t2.count("感觉就像戒毒后的戒断反应") == 1)
chk("片段5 边界感", t2.count("这是我答应她的边界感") == 1)
chk("片段6 寝室一天", t2.count("在寝室呆了一天") == 1)
chk("片段6 手握上去", t2.count("手握上去正正好好") == 1)
chk("片段7 中环至半山", t2.count("《中环至半山》") == 1)
chk("片段7 该怎么爱我", t2.count("你说你爱我，该怎么爱我") == 1)
chk("片段8 安洁莉娜 x4", t2.count("安洁莉娜") == 4)
chk("片段8 瞬间窒息", t2.count("瞬间窒息") == 1)
chk("片段8 电影票", t2.count("10.5的电影票") == 1)
chk("片段8 全盘拒绝", t2.count("全盘拒绝了我") == 1)
chk("片段8 绝不后悔", t2.count("我绝不后悔") == 1)
chk("片段8 载着祝愿", t2.count("载着祝愿和美好") == 1)
chk("片段8 这样就好", t2.count("这样就好") == 1)
chk("片段 8 标题 x1", t2.count("片段 8") == 1)
chk("blockquote-think == 7", t2.count("blockquote-think") == 7)
chk("regress 蜂蜜花茶 x1", t2.count("蜂蜜花茶") == 1)
chk("regress 葡萄柚 x1", t2.count("葡萄柚") == 1)
chk("regress MV都看了一遍 x1", t2.count("MV都看了一遍") == 1)
chk("regress Aleen x1", t2.count("Aleen") == 1)
chk("love-content 闭合仍在", t2.count("<!-- /#love-content -->") == 1)
chk("total lines print", True)
print("total lines:", len(t2.splitlines()))

if ok:
    os.remove(P + ".bak")
    print("backup removed (verification passed)")
else:
    print("backup kept at", P + ".bak")

# ---- 6. MEMORY.md line update (best effort) ----
M = os.path.join(".workbuddy", "memory", "MEMORY.md")
try:
    mt = open(M, encoding="utf-8").read()
    lines = mt.splitlines()
    hits = [i for i, l in enumerate(lines) if "恋爱」分栏" in l]
    if len(hits) == 1:
        i = hits[0]
        lines[i] = ("- 小说板块「恋爱」分栏（独立密码 `Aleen`；每次进入都需重新验证；"
                    "2026-10-02 更新为 8 段片段：09.20 / 09.21 / 09.22 / 09.27 / 09.28×2 / 09.29 / 09.30）")
        open(M, "w", encoding="utf-8", newline="").write("\n".join(lines) + "\n")
        print("MEMORY.md: love-section line updated")
    else:
        print("MEMORY.md: love-section line hits=%d, skipped" % len(hits))
except Exception as e:
    print("MEMORY.md update skipped:", type(e).__name__)

print("RESULT:", "ALL APPLIED" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
