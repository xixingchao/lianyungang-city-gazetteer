# -*- coding: utf-8 -*-
"""重启批次1(3)：全量差异游程分析——430K 源独有 / 200K 阅读版独有 到底是什么"""
import io
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "workbench" / "body_chapters_reflowed"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
K = 30


def norm(s):
    return re.sub(r"[\s，。、；：！？“”‘’（）《》〈〉…·\-~～%‰]", "", s)


def load_src():
    parts = []
    for p in sorted(SRC.rglob("*.md")):
        t = io.open(p, encoding="utf-8").read()
        t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        t = re.sub(r"^#.*$", "", t, flags=re.M)
        parts.append(t)
    return norm("".join(parts))


def load_rd():
    t = io.open(READER, encoding="utf-8", errors="ignore").read()
    body = re.search(r"<body.*?>(.*)</body>", t, re.S).group(1)
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", body, flags=re.S)
    return norm("".join(
        re.sub(r"<[^>]+>", "", a or b)
        for a, b in re.findall(r"<p[^>]*>(.*?)</p>|<h[23][^>]*>(.*?)</h[23]>", body, re.S)))


def shingles(txt):
    return {hash(txt[i:i + K]) for i in range(len(txt) - K + 1)}


def runs_uncovered(txt, other, min_len=20):
    out = []
    i, n = 0, len(txt)
    while i < n:
        if hash(txt[i:i + K]) in other:
            i += 1
            continue
        j = i
        while j < n and hash(txt[j:j + K]) not in other:
            j += 1
        frag = txt[i:j + K]
        if len(frag) >= min_len:
            out.append(frag)
        i = j + K // 2
    return out


def digit_ratio(s):
    d = sum(1 for c in s if c.isdigit())
    return d / max(len(s), 1)


src, rd = load_src(), load_rd()
S, R = shingles(src), shingles(rd)

src_runs = runs_uncovered(src, R)
rd_runs = runs_uncovered(rd, S)

src_chars_uncovered = sum(len(x) for x in src_runs)
rd_chars_uncovered = sum(len(x) for x in rd_runs)
print(json.dumps({
    "src_chars": len(src), "rd_chars": len(rd),
    "src_uncovered_chars": src_chars_uncovered, "rd_uncovered_chars": rd_chars_uncovered,
    "src_runs": len(src_runs), "rd_runs": len(rd_runs),
    "src_uncovered_digit_heavy(>30%)": sum(1 for x in src_runs if digit_ratio(x) > 0.3),
    "rd_uncovered_digit_heavy(>30%)": sum(1 for x in rd_runs if digit_ratio(x) > 0.3),
}, ensure_ascii=False, indent=1))

print("\n--- 源独有：最长的 12 段 ---")
for x in sorted(src_runs, key=len, reverse=True)[:12]:
    print(f"[{len(x)}字 数比{digit_ratio(x):.0%}]", x[:90])
print("\n--- 阅读版独有：最长的 12 段 ---")
for x in sorted(rd_runs, key=len, reverse=True)[:12]:
    print(f"[{len(x)}字 数比{digit_ratio(x):.0%}]", x[:90])

io.open(ROOT / "output" / "reports" / "delta_runs_full.json", "w", encoding="utf-8").write(
    json.dumps({"source_only": src_runs, "reader_only": rd_runs}, ensure_ascii=False, indent=1))
