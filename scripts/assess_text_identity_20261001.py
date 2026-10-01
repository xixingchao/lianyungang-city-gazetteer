# -*- coding: utf-8 -*-
"""
重启批次1评估2：源文本 vs 阅读版文本 的字符级一致性（与分段无关）

方法：两边全文规范化（去空白）后取 50 字符 shingle 集合，算双向覆盖率。
覆盖率≈1 → 内容一致（差异只在分段）；覆盖率明显<1 → 存在真实改写/增删。
再对差异 shingle 定位到具体文字片段，输出样例。
"""
import io
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "workbench" / "body_chapters_reflowed"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
K = 50


def norm(s):
    return re.sub(r"[\s，。、；：！？“”‘’（）《》〈〉…·\-~～]", "", s)


def shingles(txt):
    # 全位置取样 + 哈希，避免定步长窗口因单字符增删整体错位
    return {hash(txt[i:i + K]) for i in range(len(txt) - K + 1)}


# 源：去掉注释和标题
src_parts = []
for p in sorted(SRC.rglob("*.md")):
    t = io.open(p, encoding="utf-8").read()
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"^#.*$", "", t, flags=re.M)
    src_parts.append(t)
src_txt = norm("".join(src_parts))

# 阅读版：取 <p>/<h2>/<h3> 文本
t = io.open(READER, encoding="utf-8", errors="ignore").read()
body = re.search(r"<body.*?>(.*)</body>", t, re.S).group(1)
body = re.sub(r"<script.*?</script>|<style.*?</style>", "", body, flags=re.S)
rd_txt = norm("".join(
    re.sub(r"<[^>]+>", "", a or b)
    for a, b in re.findall(r"<p[^>]*>(.*?)</p>|<h[23][^>]*>(.*?)</h[23]>", body, re.S)))

S, R = shingles(src_txt), shingles(rd_txt)
inter = S & R
stats = {
    "src_chars": len(src_txt),
    "reader_chars": len(rd_txt),
    "src_shingles": len(S),
    "reader_shingles": len(R),
    "src_covered_by_reader": round(100 * len(inter) / max(len(S), 1), 2),
    "reader_covered_by_src": round(100 * len(inter) / max(len(R), 1), 2),
}
print(json.dumps(stats, ensure_ascii=False, indent=1))

# 提取真实差异文字：在对方全文上滑动，找连续未被覆盖的片段
def diff_runs(txt, other_shingles, min_len=25, max_runs=200):
    runs = []
    i = 0
    n = len(txt)
    while i < n and len(runs) < max_runs:
        if hash(txt[i:i + K]) in other_shingles:
            i += 1
            continue
        j = i
        while j < n and hash(txt[j:j + K]) not in other_shingles:
            j += 1
        frag = txt[i:j + K // 2]
        if len(frag) >= min_len:
            runs.append(frag)
        i = j + 1
    return runs


rd_only = diff_runs(rd_txt, S)
src_only_runs = diff_runs(src_txt, R)
print("\n--- 阅读版独有片段（前15，=表格嵌回/修复） ---")
for x in rd_only[:15]:
    print("◇", x[:100])
print("\n--- 源独有片段（前15，=已清除残文） ---")
for x in src_only_runs[:15]:
    print("◇", x[:100])
io.open(ROOT / "output" / "reports" / "text_identity_diff_samples.json", "w",
        encoding="utf-8").write(json.dumps(
            {"reader_only": rd_only[:100], "source_only": src_only_runs[:100]},
            ensure_ascii=False, indent=1))
