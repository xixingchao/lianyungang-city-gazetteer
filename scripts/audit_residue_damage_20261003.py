# -*- coding: utf-8 -*-
r"""残文误伤审计：把残文撤出清单里"像正文且 v2 缺失"的段，到老源文件定位并判断能否回插（2026-10-03）。

输入：
  - 撤出清单：output/package/连云港市志_交付包_20260706_190445/reports/remaining_reader_residue_removed.md
  - 老源文件：workbench/body_chapters/**.md（7-06 时代，含页锚）
  - 现真值：workbench/body_chapters_v2/*.md
输出：
  - C:\Users\52744\_scratch\residue_restore_plan.txt（逐条：能否回插/锚点/前后文）
用法：python audit_residue_damage_20261003.py [--report PATH]
"""
from __future__ import annotations

import argparse
import glob
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "output" / "package" / "连云港市志_交付包_20260706_190445" / "reports" / "remaining_reader_residue_removed.md"
OUT = Path(r"C:\Users\52744\_scratch\residue_restore_plan.txt")
ANCH = re.compile(r"<!--\s*page-anchor:\s*([A-Za-z0-9\-]+)\s*-->")


def load_removals(path: Path) -> list[list[str]]:
    lines = io.open(path, encoding="utf-8").read().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("## 撤出清单"))
    rows = []
    for l in lines[start + 2:]:
        if not l.startswith("|"):
            continue
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) < 4 or not cells[0].isdigit():
            continue
        rows.append(cells)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=str(DEFAULT_REPORT))
    args = ap.parse_args()

    rows = load_removals(Path(args.report))
    v2 = "".join(io.open(f, encoding="utf-8").read()
                 for f in glob.glob(str(ROOT / "workbench" / "body_chapters_v2" / "*.md")))
    old_files = sorted(glob.glob(str(ROOT / "workbench" / "body_chapters" / "**" / "*.md"), recursive=True))
    old_files = [f for f in old_files if ".bak" not in f]

    def probes_of(para: str) -> list[str]:
        """从段中多处取探针（对 OCR 变体更宽容）。"""
        s = "".join(ch for ch in para if "\u4e00" <= ch <= "\u9fff" or ch.isdigit())
        out = []
        for off in (0, max(0, len(s) // 3), max(0, 2 * len(s) // 3), max(0, len(s) - 14)):
            seg = s[off:off + 14]
            if len(seg) >= 8:
                out.append(seg[:8])
                out.append(seg)
        return list(dict.fromkeys(out))

    def find_in_old(para: str):
        """在老源文件里找该段，返回 (文件, 行号, 页锚, 前后文)。多探针提高命中率。"""
        for f in old_files:
            t = io.open(f, encoding="utf-8", errors="replace").read()
            for probe in probes_of(para):
                i = t.find(probe)
                if i < 0:
                    continue
                # 页锚
                m = None
                for mm in ANCH.finditer(t, 0, i):
                    m = mm
                ln = t.count("\n", 0, i) + 1
                return Path(f).name, ln, (m.group(1) if m else "?"), t[max(0, i - 200):i + 400]
        return None

    out = []
    placeable = blockloss = notfound = skipped = 0
    for r in rows:
        ex = r[3]
        if "。" not in ex:
            skipped += 1
            continue
        cjk = sum(1 for ch in ex if "\u4e00" <= ch <= "\u9fff")
        if cjk < 25 or ex.startswith("续上表") or ex.startswith("注：源 OCR"):
            skipped += 1
            continue
        # v2 是否已有
        probe12 = "".join(ch for ch in ex if "\u4e00" <= ch <= "\u9fff")[:12]
        if probe12 and probe12 in v2:
            skipped += 1
            continue
        loc = find_in_old(ex)
        if not loc:
            notfound += 1
            out.append(f"[找不到] {r[0]} {r[1]} | {ex[:90]}")
            continue
        fname, ln, anch, ctx = loc
        # 判断前后邻居是否在 v2（取段前 12 字/段后 12 字）
        before = "".join(ch for ch in ctx[:ctx.find(ex[:12]) if ex[:12] in ctx else 0] if "\u4e00" <= ch <= "\u9fff")[-12:]
        after = ""
        if ex[-12:] in ctx:
            tail = ctx[ctx.find(ex[-12:]) + 12:]
            after = "".join(ch for ch in tail if "\u4e00" <= ch <= "\u9fff")[:12]
        ok_before = bool(before) and before in v2
        ok_after = bool(after) and after in v2
        if ok_before or ok_after:
            placeable += 1
            out.append(f"[可回插] {r[0]} {r[1]} | {fname} L{ln} {anch} | 前邻{'✓' if ok_before else '✗'} 后邻{'✓' if ok_after else '✗'} | {ex[:80]}")
        else:
            blockloss += 1
            out.append(f"[整块缺失] {r[0]} {r[1]} | {fname} L{ln} {anch} | {ex[:80]}")
    out.append("")
    out.append(f"合计：可回插 {placeable}；整块缺失 {blockloss}；老源找不到 {notfound}；跳过 {skipped}")
    OUT.write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out[-30:]))


if __name__ == "__main__":
    main()
