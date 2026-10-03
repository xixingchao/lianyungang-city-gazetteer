# -*- coding: utf-8 -*-
r"""回插被"残文撤出"误删的正文 · v4（跨缺失段外扩找锚，按序整段插入）（2026-10-03）。

v3 的锚只找"紧邻段"，遇到成片缺失就失效；v1 的碎片锚会定位到同段另一处。
v4 规则：
1. 以撤出清单里的**段落文本**为单位，按其在老源中的先后顺序处理；
2. 为每段找锚：从它在老源中的位置**向前**取 18 字窗口，若不在 v2 就继续前移
   （跳过同样缺失的段落），直到命中 v2 —— 命中处即"该段应插入的位置"；
   若向前一直找不到，则向后取窗（插到命中点之前）；
3. 同一次运行内，先处理的段可视作"已存在"（用于后续段的锚判定），保证成片缺失时
   段序不乱；
4. 插前校验：该段自身文本不应已在 v2 中；插后写日志。

用法：
  python restore_residue_v4_20261003.py            # dry-run
  python restore_residue_v4_20261003.py --apply
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
REPORT = ROOT / "output" / "package" / "连云港市志_交付包_20260706_190445" / "reports" / "remaining_reader_residue_removed.md"
LOG = ROOT / "output" / "reports" / "progress" / "20261003_残文误伤回插记录_v4.md"
TITLE_RE = re.compile(r"表\s*\d+\s*[-－—]\s*\d+")


def clean(s: str) -> str:
    s = re.sub(r"<!--.*?-->", "", s)
    s = re.sub(r"[#*>`|]", "", s)
    return re.sub(r"\s+", "", s)


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


def load_rows(path: Path) -> list[list[str]]:
    lines = io.open(path, encoding="utf-8").read().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("## 撤出清单"))
    rows = []
    for l in lines[start + 2:]:
        if l.startswith("|"):
            cells = [c.strip() for c in l.strip("|").split("|")]
            if len(cells) >= 4 and cells[0].isdigit():
                rows.append(cells)
    return rows


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
    args = ap.parse_args()

    rows = [r for r in load_rows(REPORT) if is_prose(r[3])]
    old_files = [f for f in sorted(glob.glob(str(OLD / "**" / "*.md"), recursive=True))
                 if ".bak" not in f and "汇总" not in f and "全书" not in f]
    v2_files = sorted(glob.glob(str(V2 / "*.md")))
    v2_raw = {f: io.open(f, encoding="utf-8").read() for f in v2_files}
    v2_clean = {f: clean(v2_raw[f]) for f in v2_files}
    all_clean = "".join(v2_clean.values())

    # 逐条：在老源定位 + 记录顺序（按老源文件内偏移排序）
    items = []
    for r in rows:
        ex = r[3]
        probe = clean(ex)[:12]
        if len(probe) < 8 or clean(ex) in all_clean:
            continue
        hit = None
        for f in old_files:
            t = io.open(f, encoding="utf-8", errors="replace").read()
            i = clean(t).find(probe)
            if i >= 0:
                hit = (f, t, i)
                break
        if hit:
            items.append((hit[0], hit[2], ex, r))
    items.sort(key=lambda x: (x[0], x[1]))

    # 逐条找锚（外扩；已处理段视为已存在）
    virtual = {f: v2_clean[f] for f in v2_clean}
    plan = []
    for f, pos, ex, r in items:
        t = io.open(f, encoding="utf-8", errors="replace").read()
        tclean = clean(t)
        cpos = tclean.find(clean(ex)[:12])
        # 文件 → v2 同名
        vf = str(V2 / Path(f).name)
        if vf not in virtual:
            vf = max(virtual, key=lambda x: len(virtual[x]))
        anchor = None
        side = None
        for step in (0, 18, 40, 80, 160, 400, 1000, 2500):
            if cpos - step - 18 < 0:
                break
            win = tclean[cpos - step - 18: cpos - step]
            if len(win) < 12:
                continue
            k = virtual[vf].rfind(win)
            if k >= 0:
                anchor, side, at = win, "after", k + len(win)
                break
        if anchor is None:
            for step in (0, 18, 40, 80, 160, 400, 1000, 2500):
                if cpos + 18 + step >= len(tclean):
                    break
                win = tclean[cpos + 18 + step: cpos + 36 + step]
                if len(win) < 12:
                    continue
                k = virtual[vf].find(win)
                if k >= 0:
                    anchor, side, at = win, "before", k
                    break
        if anchor is None:
            continue
        # 插回（虚拟流同步更新，保持后续锚可用）
        para = clean(ex)
        if side == "after":
            virtual[vf] = virtual[vf][:at] + para + virtual[vf][at:]
        else:
            virtual[vf] = virtual[vf][:at] + para + virtual[vf][at:]
        plan.append((vf, anchor, side, ex, r[1]))

    print(f"v4 待回插 {len(plan)} 段")
    for vf, anchor, side, ex, ch in plan[:20]:
        print(f'  [{side}] {ch[:12]:12} {Path(vf).name[:16]:16} | {ex[:52]}')
    if not args.apply:
        print("（dry-run）")
        return

    from collections import defaultdict
    per = defaultdict(list)
    for vf, anchor, side, ex, ch in plan:
        per[vf].append((anchor, side, ex, ch))
    log = ["# 残文误伤回插记录 v4（2026-10-03，外扩找锚）", ""]
    for vf, lst in per.items():
        t = v2_raw[vf]
        for anchor, side, ex, ch in lst:
            k = t.find(anchor[:14])
            if k < 0:
                print("落笔失败(锚未命中原文):", ex[:30])
                continue
            if side == "after":
                at = k + len(anchor)
                nxt = t[at:at + 2]
                sep = "\n\n" if nxt.startswith("\n") else ""
                t = t[:at] + sep + ex + ("\n\n" if sep else "") + t[at:]
            else:
                start = t.rfind("\n\n", 0, k)
                start = start + 2 if start >= 0 else k
                t = t[:start] + ex + "\n\n" + t[start:]
            log.append(f"- {Path(vf).name} | {side} | {ch} | {ex[:60]}")
        io.open(vf, "w", encoding="utf-8", newline="\n").write(t)
        print(f"写回 {Path(vf).name}: {len(lst)} 段")
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(log) + "\n")
    print("日志:", LOG)


if __name__ == "__main__":
    main()
