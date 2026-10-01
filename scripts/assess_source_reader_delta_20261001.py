# -*- coding: utf-8 -*-
"""
重启批次1评估：重排后源章节 vs 7-06 最终阅读版 的段落级差异

目的：量化"直接改 HTML 的修复未沉回源文件"的缺口（整改计划阶段D）。
口径：段落规范化（去所有空白）后做双向集合比对：
- R→S：阅读版有、源没有 → 需要沉回源的修复/增补
- S→R：源有、阅读版没有 → 阅读版已删除的残文（正常）或被改写
"""
import io
import re
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "workbench" / "body_chapters_reflowed"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"


def norm(s):
    return re.sub(r"[\s，。、；：！？“”‘’（）《》〈〉…—·\-~～%]", "", s)


def load_source_paras():
    paras = []
    for p in sorted(SRC.rglob("*.md")):
        t = io.open(p, encoding="utf-8").read()
        for blk in t.split("\n\n"):
            s = blk.strip()
            if not s or s.startswith("<!--") or s.startswith("#"):
                continue
            paras.append((p.name, s))
    return paras


def load_reader_paras():
    t = io.open(READER, encoding="utf-8", errors="ignore").read()
    body = re.search(r"<body.*?>(.*)</body>", t, re.S).group(1)
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", body, flags=re.S)
    raw = re.findall(r"<p[^>]*>(.*?)</p>|<h[23][^>]*>(.*?)</h[23]>", body, re.S)
    paras = []
    for a, b in raw:
        x = re.sub(r"<[^>]+>", "", a or b)
        x = re.sub(r"\s+", "", x)
        if x:
            paras.append(x)
    return paras


src_paras = load_source_paras()
rd_paras = load_reader_paras()

src_norm = {norm(s): (fn, s) for fn, s in src_paras}
src_norm_keys = set(src_norm)

match_exact = 0
rd_missing = []          # 阅读版有、源没有
for r in rd_paras:
    nr = norm(r)
    if nr in src_norm_keys:
        match_exact += 1
    else:
        rd_missing.append(r)

# 对 rd_missing 做宽松匹配：去标点后前30字符哈希
src_head_index = {}
for fn, s in src_paras:
    ns = norm(s)
    src_head_index.setdefault(ns[:30], []).append(ns)

match_loose = 0
rd_hard_missing = []
for r in rd_missing:
    nr = norm(r)
    cands = src_head_index.get(nr[:30])
    if cands and any(c != nr and (c in nr or nr in c) for c in cands):
        match_loose += 1
    else:
        rd_hard_missing.append(r)

rd_norm_keys = {norm(r) for r in rd_paras}
src_only = [s for fn, s in src_paras if norm(s) not in rd_norm_keys]

out = {
    "reader_paragraphs": len(rd_paras),
    "source_paragraphs": len(src_paras),
    "reader_exact_in_source": match_exact,
    "reader_loose_in_source": match_loose,
    "reader_not_in_source": len(rd_hard_missing),
    "source_not_in_reader": len(src_only),
    "pct_reader_covered": round(100 * (match_exact + match_loose) / max(len(rd_paras), 1), 2),
}
print(json.dumps(out, ensure_ascii=False, indent=1))

io.open(ROOT / "output" / "reports" / "reader_not_in_source_samples.json", "w", encoding="utf-8").write(
    json.dumps(rd_hard_missing[:200], ensure_ascii=False, indent=1))
io.open(ROOT / "output" / "reports" / "source_not_in_reader_samples.json", "w", encoding="utf-8").write(
    json.dumps(src_only[:200], ensure_ascii=False, indent=1))
print("\n--- 阅读版独有段（前8条，=需沉回源的修复） ---")
for x in rd_hard_missing[:8]:
    print("◇", x[:110])
print("\n--- 源独有段（前8条，=阅读版已清除的残文） ---")
for x in src_only[:8]:
    print("◇", x[:110])
