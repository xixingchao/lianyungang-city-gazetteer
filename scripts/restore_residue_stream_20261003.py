# -*- coding: utf-8 -*-
r"""回插被"残文撤出"误删的正文 · 流对齐版（2026-10-03）。

原理（批次2 的反向操作）：把老源文件（7-06 时代、含全量原文）与 v2 同名字段做
**清洗后流对齐**（difflib.SequenceMatcher.get_matching_blocks）：
- 匹配块 = 两边都有的内容；
- 老源在匹配块之间的"缺口" = v2 缺的内容 → 按启发式判断是否正文（有句号、汉字≥25、
  非"续上表/表头/数字串"）→ 是则在对应处插回 v2。

插回位置取"缺口前一个匹配块结束处"在 v2 原始文本中的偏移（清洗流→原文偏移的映射）。

用法：
  python restore_residue_stream_20261003.py            # dry-run（列出缺口）
  python restore_residue_stream_20261003.py --apply
"""
from __future__ import annotations

import argparse
import io
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "workbench" / "body_chapters_v2"
OLD = ROOT / "workbench" / "body_chapters"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
LOG = ROOT / "output" / "reports" / "progress" / "20261003_残文误伤回插记录.md"

# 老源文件名 → v2 文件名（不同名时按同卷归并）
PAIRS = [
    ("上/总述与大事记.md", "总述与大事记.md"),
    ("上/第一卷_自然环境.md", "第一卷_自然环境.md"),
    ("上/第二卷_建置区划.md", "第二卷_建置区划.md"),
    ("上/第三卷_区县概况.md", "第三卷_区县概况.md"),
    ("上/第四卷_人口（part01_部分）.md", "第四卷_人口（part01_部分）.md"),
    ("上/第四卷至第十卷（part02）.md", "第四卷至第十卷（part02）.md"),
    ("上/第十卷至第十六卷（part03）.md", "第十卷至第十六卷（part03）.md"),
    ("中/第十七卷至第二十九卷（中part01）.md", "第十七卷至第二十九卷（中part01）.md"),
    ("中/第三十卷至第四十二卷（中part02）.md", "第三十卷至第四十二卷（中part02）.md"),
    ("下/第四十三卷至第五十一卷（下part01）.md", "第四十三卷至第五十一卷（下part01）.md"),
    ("下/第五十二卷至第六十卷及附录（下part02）.md", "第五十二卷至第六十卷及附录（下part02）.md"),
]


def clean_with_map(s: str) -> tuple[str, list[int]]:
    """去掉注释/标记/空白，返回 (清洗串, 清洗位→原始位 的映射)。"""
    out = []
    pos = []
    i = 0
    n = len(s)
    while i < n:
        if s.startswith("<!--", i):
            j = s.find("-->", i)
            i = (j + 3) if j >= 0 else n
            continue
        ch = s[i]
        if ch in "#*>`|" or ch.isspace():
            i += 1
            continue
        out.append(ch)
        pos.append(i)
        i += 1
    return "".join(out), pos


TITLE_RE = re.compile(r"表\s*\d+\s*[-－—]\s*\d+")


def is_prose(chunk: str) -> bool:
    if "。" not in chunk:
        return False
    if chunk.lstrip("续上表").startswith("续上表") or "注：源OCR" in chunk.replace(" ", ""):
        return False
    cjk = sum(1 for ch in chunk if "\u4e00" <= ch <= "\u9fff")
    digits = sum(1 for ch in chunk if ch.isdigit())
    if cjk < 25 or TITLE_RE.search(chunk):
        return False
    if digits > (cjk + digits) * 0.35:
        return False
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--min-len", type=int, default=25, help="缺口最小清洗长度")
    args = ap.parse_args()

    plans = []
    for old_rel, v2_name in PAIRS:
        op = ROOT / "workbench" / "body_chapters" / old_rel
        vp = V2 / v2_name
        if not op.exists() or not vp.exists():
            print(f"跳过（文件缺失）: {old_rel}")
            continue
        ot = io.open(op, encoding="utf-8", errors="replace").read()
        vt = io.open(vp, encoding="utf-8").read()
        oc, omap = clean_with_map(ot)
        vc, vmap = clean_with_map(vt)
        sm = SequenceMatcher(None, oc, vc, autojunk=False)
        blocks = sm.get_matching_blocks()
        gaps = []
        for k in range(len(blocks) - 1):
            a_end = blocks[k].a + blocks[k].size
            b_end = blocks[k].b + blocks[k].size
            a_next = blocks[k + 1].a
            if a_next - a_end >= args.min_len:
                chunk = oc[a_end:a_next]
                if is_prose(chunk):
                    # 插回位置：v2 清洗流的 b_end → v2 原始偏移
                    if b_end < len(vmap):
                        raw_pos = vmap[b_end]
                    else:
                        raw_pos = len(vt)
                    # 原文形态的缺口（尽量从老源原始文本取，保留标点）
                    raw_a0 = omap[a_end] if a_end < len(omap) else len(ot)
                    raw_a1 = omap[a_next - 1] + 1 if a_next - 1 < len(omap) else len(ot)
                    raw_chunk = ot[raw_a0:raw_a1]
                    raw_chunk = re.sub(r"<!--.*?-->", "", raw_chunk, flags=re.S)
                    raw_chunk = re.sub(r"[ \t]*\n[ \t]*", "", raw_chunk).strip()
                    # 去掉可能的行内锚/标题符
                    raw_chunk = re.sub(r"^[#>|*]+", "", raw_chunk).strip()
                    if len(raw_chunk) >= args.min_len:
                        gaps.append((a_end, raw_pos, raw_chunk))
        if gaps:
            plans.append((v2_name, vp, vt, gaps))
            print(f"{v2_name}: 缺口 {len(gaps)} 处，例：{gaps[0][2][:60]}")

    print(f"\n合计待回插 {sum(len(p[3]) for p in plans)} 段，涉及 {len(plans)} 个文件")
    if not args.apply:
        print("（dry-run）")
        return

    log = ["# 残文误伤回插记录（2026-10-03，流对齐版）", ""]
    for v2_name, vp, vt, gaps in plans:
        t = vt
        for a_end, raw_pos, chunk in sorted(gaps, key=lambda x: -x[1]):
            t = t[:raw_pos] + "\n\n" + chunk + "\n\n" + t[raw_pos:]
            log.append(f"- {v2_name} | {chunk[:60]}")
        io.open(vp, "w", encoding="utf-8", newline="\n").write(t)
        print(f"v2 写回 {v2_name}: {len(gaps)} 段")
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(log) + "\n")
    print("日志:", LOG)


if __name__ == "__main__":
    main()
