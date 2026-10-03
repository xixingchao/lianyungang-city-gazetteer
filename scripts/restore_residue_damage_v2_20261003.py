# -*- coding: utf-8 -*-
r"""回插被"残文撤出"误删的正文档落 · v2 版（2026-10-03，严格前后邻定位）。

与 v1 的区别：定位用**紧邻的整段**（老源里该段的上一段/下一段），而不是 60 字碎片；
并要求 前邻 出现在 v2 且 后邻 出现在其之后，才判定"两邻夹住"，否则只按单邻插并标注。

用法：
  python restore_residue_damage_v2_20261003.py               # dry-run
  python restore_residue_damage_v2_20261003.py --apply
"""
from __future__ import annotations

import argparse
import glob
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "workbench" / "body_chapters_v2"
OLD = ROOT / "workbench" / "body_chapters"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
LOG = ROOT / "output" / "reports" / "progress" / "20261003_残文误伤回插记录.md"


def load_rows(report: Path) -> list[list[str]]:
    lines = io.open(report, encoding="utf-8").read().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("## 撤出清单"))
    rows = []
    for l in lines[start + 2:]:
        if l.startswith("|"):
            cells = [c.strip() for c in l.strip("|").split("|")]
            if len(cells) >= 4 and cells[0].isdigit():
                rows.append(cells)
    return rows


def clean(s: str) -> str:
    s = re.sub(r"<!--.*?-->", "", s)
    s = re.sub(r"[#*>`|]", "", s)
    return re.sub(r"\s+", "", s)


def probe_words(para: str, n: int = 12) -> list[str]:
    s = "".join(ch for ch in para if "\u4e00" <= ch <= "\u9fff" or ch.isdigit())
    out = []
    for off in (0, max(0, len(s) // 3), max(0, 2 * len(s) // 3), max(0, len(s) - n)):
        seg = s[off:off + n]
        if len(seg) >= 8:
            out.append(seg)
    return list(dict.fromkeys(out))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=str(ROOT / "output" / "package" / "连云港市志_交付包_20260706_190445" / "reports" / "remaining_reader_residue_removed.md"))
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    rows = load_rows(Path(args.report))
    v2_files = sorted(glob.glob(str(V2 / "*.md")))
    v2_text = {f: io.open(f, encoding="utf-8").read() for f in v2_files}
    all_v2 = "".join(v2_text.values())
    all_v2_clean = clean(all_v2)

    old_files = [f for f in sorted(glob.glob(str(OLD / "**" / "*.md"), recursive=True)) if ".bak" not in f]

    ins = []  # (v2 file, anchor_text, side, para, 章节, 定位)
    for r in rows:
        ex = r[3]
        if "。" not in ex or ex.startswith("续上表") or ex.startswith("注：源 OCR"):
            continue
        cjk = sum(1 for ch in ex if "\u4e00" <= ch <= "\u9fff")
        digits = sum(1 for ch in ex if ch.isdigit())
        if cjk < 25:
            continue
        if re.search(r"表\s*\d+\s*[-－—]\s*\d+", ex) or digits > (cjk + digits) * 0.35:
            continue
        if any(p in all_v2_clean for p in probe_words(clean(ex), 12)):
            continue
        # 老源定位
        hit = None
        for f in old_files:
            t = io.open(f, encoding="utf-8", errors="replace").read()
            for p in probe_words(ex, 10):
                i = t.find(p)
                if i >= 0:
                    hit = (f, t, i)
                    break
            if hit:
                break
        if not hit:
            continue
        ofile, otext, oi = hit
        # 紧邻整段
        paras = [p for p in re.split(r"\n\s*\n", otext)]
        # 找包含该段的段索引
        idx = None
        for k, p in enumerate(paras):
            if clean(ex)[:20] and clean(ex)[:20] in clean(p):
                idx = k
                break
        if idx is None:
            continue
        prev_p = clean(paras[idx - 1])[:30] if idx > 0 else ""
        next_p = clean(paras[idx + 1])[:30] if idx + 1 < len(paras) else ""
        v2file = str(V2 / Path(ofile).name)
        if v2file not in v2_text:
            v2file = max(v2_text, key=lambda f: len(v2_text[f]))
        vt_clean = clean(v2_text[v2file])
        ip = vt_clean.find(prev_p) if len(prev_p) >= 12 else -1
        inx = vt_clean.find(next_p) if len(next_p) >= 12 else -1
        if ip >= 0 and inx > ip:
            side, anchor, why = "between", prev_p, "两邻夹住"
        elif ip >= 0:
            side, anchor, why = "after", prev_p, "仅前邻"
        elif inx >= 0:
            side, anchor, why = "before", next_p, "仅后邻"
        else:
            continue
        ins.append((v2file, anchor, side, clean(ex), r[1], why, prev_p, next_p))

    print(f"可插入 {len(ins)} 段")
    for x in ins[:20]:
        print(f'  [{x[5]}] {x[4][:12]:12} {Path(x[0]).name[:18]:18} | {x[3][:44]}')
    if not args.apply:
        print("（dry-run）")
        return

    from collections import defaultdict
    per = defaultdict(list)
    for v2file, anchor, side, para, ch, why, prev_p, next_p in ins:
        per[v2file].append((anchor, side, para, ch, why))
    log = ["# 残文误伤回插记录（2026-10-03）", "", f"回插 {len(ins)} 段（严格前后邻定位）", "",
           "| 章节 | 定位 | 段首 |", "| --- | --- | --- |"]
    for v2file, items in per.items():
        t = v2_text[v2file]
        # 以 clean 文本定位回原始位置：逐段处理，从后往前替代
        for anchor, side, para, ch, why in items:
            # 用锚段的前若干字在原文里定位
            k = t.find(anchor[:16])
            if k < 0:
                print("落笔失败(锚未命中):", para[:30])
                continue
            if side == "after":
                end = t.find("\n", k)
                end = end if end >= 0 else k
                t = t[:end] + "\n\n" + para + t[end:]
            elif side == "before":
                start = t.rfind("\n\n", 0, k)
                start = start + 2 if start >= 0 else k
                t = t[:start] + para + "\n\n" + t[start:]
            else:  # between
                end = t.find("\n", k)
                end = end if end >= 0 else k
                t = t[:end] + "\n\n" + para + t[end:]
            log.append(f"| {ch[:12]} | {why} | {para[:40]} |")
        io.open(v2file, "w", encoding="utf-8", newline="\n").write(t)
        print(f"v2 写回 {Path(v2file).name}: {len(items)} 段")
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(log) + "\n")
    print("日志:", LOG)


if __name__ == "__main__":
    main()
