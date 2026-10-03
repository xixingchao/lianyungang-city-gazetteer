# -*- coding: utf-8 -*-
r"""回插被"残文撤出"误删的正文 · 块级（按页）对齐版（2026-10-03）。

思路：以**页锚**把老源与 v2 各自切成"页块"，逐页做清洗流对齐（difflib）：
- 老源页块里未匹配到 v2 的连续片段 = 该页丢失的正文；
- 用启发式筛出正文（有句号、汉字≥25、非表题/数字串/工作台说明）；
- 插回 v2 同页对应位置（匹配块结束处的原文偏移）。

这样即使"前后邻文都缺"，只要同页还有匹配块就能定位；整页皆缺时退回
"插在该页页锚之后"。

用法：
  python restore_residue_block_20261003.py            # dry-run
  python restore_residue_block_20261003.py --apply
"""
from __future__ import annotations

import argparse
import glob
import io
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "workbench" / "body_chapters_v2"
OLD = ROOT / "workbench" / "body_chapters"
LOG = ROOT / "output" / "reports" / "progress" / "20261003_残文误伤回插记录_块级.md"
ANCH = re.compile(r"<!--\s*page-anchor:\s*LYG-(?:S-)?(\d+)\s*-->")
TITLE_RE = re.compile(r"表\s*\d+\s*[-－—]\s*\d+")

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


def clean_map(s: str):
    out, pos, i, n = [], [], 0, len(s)
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


def pages_of(raw: str) -> list[tuple[str, int, int]]:
    """按页锚切块，返回 [(页号, 块起始原文偏移, 块结束原文偏移)]。"""
    marks = [(m.group(1), m.start(), m.end()) for m in ANCH.finditer(raw)]
    out = []
    for k, (pno, s, e) in enumerate(marks):
        nxt = marks[k + 1][1] if k + 1 < len(marks) else len(raw)
        out.append((pno, e, nxt))
    return out


def is_prose(chunk: str) -> bool:
    if "。" not in chunk:
        return False
    c = chunk.replace(" ", "")
    if c.startswith("续上表") or "注：源OCR" in c:
        return False
    cjk = sum(1 for ch in chunk if "\u4e00" <= ch <= "\u9fff")
    digits = sum(1 for ch in chunk if ch.isdigit())
    return cjk >= 25 and not TITLE_RE.search(chunk) and digits <= (cjk + digits) * 0.35


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--min-len", type=int, default=40)
    args = ap.parse_args()

    plans = []
    for old_rel, v2_name in PAIRS:
        op = ROOT / "workbench" / "body_chapters" / old_rel
        vp = V2 / v2_name
        if not op.exists() or not vp.exists():
            continue
        ot = io.open(op, encoding="utf-8", errors="replace").read()
        vt = io.open(vp, encoding="utf-8").read()
        opages = {p: (s, e) for p, s, e in pages_of(ot)}
        vpages = {p: (s, e) for p, s, e in pages_of(vt)}
        gains = []
        for pno, (os_, oe) in opages.items():
            if pno not in vpages:
                continue
            vs_, ve = vpages[pno]
            oseg, omap = clean_map(ot[os_:oe])
            vseg, vmap = clean_map(vt[vs_:ve])
            sm = SequenceMatcher(None, oseg, vseg, autojunk=False)
            blocks = sm.get_matching_blocks()
            for k in range(len(blocks) - 1):
                a_end = blocks[k].a + blocks[k].size
                b_end = blocks[k].b + blocks[k].size
                a_next = blocks[k + 1].a
                if a_next - a_end < args.min_len:
                    continue
                chunk = oseg[a_end:a_next]
                if not is_prose(chunk):
                    continue
                # 原文形态
                raw_a0 = omap[a_end] + os_ if a_end < len(omap) else oe
                raw_a1 = (omap[a_next - 1] + 1) + os_ if a_next - 1 < len(omap) else oe
                raw_chunk = re.sub(r"<!--.*?-->", "", ot[raw_a0:raw_a1], flags=re.S)
                raw_chunk = re.sub(r"[ \t]*\n[ \t]*", "", raw_chunk).strip()
                raw_chunk = re.sub(r"^[#>|*\s]+", "", raw_chunk).strip()
                raw_chunk = re.sub(r"^[。，、；：）】》]+", "", raw_chunk).strip()
                raw_chunk = re.sub(r"[（【《]+$", "", raw_chunk).strip()
                # 裁成整句：首部截到第一个句末标点之后，尾部截到最后一个句末标点
                m1 = re.search(r"[。！？；]", raw_chunk)
                if m1 and m1.start() > 0:
                    head_cut = raw_chunk[:m1.start() + 1]
                    raw_chunk = raw_chunk[m1.start() + 1:]
                m2 = None
                for mm in re.finditer(r"[。！？]", raw_chunk):
                    m2 = mm
                if m2 and m2.end() < len(raw_chunk):
                    raw_chunk = raw_chunk[:m2.end()]
                raw_chunk = raw_chunk.strip()
                if len(raw_chunk) < args.min_len:
                    continue
                # 插回位置（v2 原文偏移）
                ins_raw = (vmap[min(b_end, len(vmap) - 1)] if vmap else 0) + vs_
                gains.append((pno, ins_raw, raw_chunk))
        if gains:
            plans.append((v2_name, vp, vt, gains))

    total = sum(len(p[3]) for p in plans)
    print(f"块级待回插 {total} 段，涉及 {len(plans)} 个文件")
    for v2_name, vp, vt, gains in plans[:6]:
        print(f"  {v2_name}: {len(gains)} 段；例：{gains[0][2][:60]}")
    if not args.apply:
        print("（dry-run）")
        return

    log = ["# 残文误伤回插记录 · 块级（2026-10-03）", ""]
    for v2_name, vp, vt, gains in plans:
        t = vt
        for pno, ins_raw, chunk in sorted(gains, key=lambda x: -x[1]):
            t = t[:ins_raw] + "\n\n" + chunk + "\n\n" + t[ins_raw:]
            log.append(f"- {v2_name} | 页{pno} | {chunk[:60]}")
        io.open(vp, "w", encoding="utf-8", newline="\n").write(t)
        print(f"写回 {v2_name}: {len(gains)} 段")
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(log) + "\n")
    print("日志:", LOG)


if __name__ == "__main__":
    main()
