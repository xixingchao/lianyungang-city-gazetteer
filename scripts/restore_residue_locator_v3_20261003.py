# -*- coding: utf-8 -*-
r"""回插被"残文撤出"误删的正文 · 前邻尾串定位版（2026-10-03）。

定位法（快且准）：
1. 在老源里找到该段 → 取**紧挨它之前的 18 字**（清洗后）作 prior_tail；
2. 在 v2 清洗流里找 prior_tail 的**最后一次出现**，插在其后（原文偏移由映射还原）；
3. 校验：该段之后应能先遇到 后邻前 18 字（next_head）——若不在其前，改用 next_head 定位；
4. 仍失败则跳过并报告。

用法：
  python restore_residue_locator_v3_20261003.py            # dry-run（含校验结果）
  python restore_residue_locator_v3_20261003.py --apply
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
LOG = ROOT / "output" / "reports" / "progress" / "20261003_残文误伤回插记录.md"
REPORT = ROOT / "output" / "package" / "连云港市志_交付包_20260706_190445" / "reports" / "remaining_reader_residue_removed.md"


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


TITLE_RE = re.compile(r"表\s*\d+\s*[-－—]\s*\d+")


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

    rows = load_rows(REPORT)
    old_files = [f for f in sorted(glob.glob(str(OLD / "**" / "*.md"), recursive=True)) if ".bak" not in f]
    v2_files = sorted(glob.glob(str(V2 / "*.md")))
    v2_raw = {f: io.open(f, encoding="utf-8").read() for f in v2_files}
    v2_clean, v2_map = {}, {}
    for f, t in v2_raw.items():
        c, m = clean_map(t)
        v2_clean[f], v2_map[f] = c, m
    all_clean = "".join(v2_clean.values())

    plan = []
    for r in rows:
        ex = r[3]
        if not is_prose(ex):
            continue
        probe = "".join(ch for ch in ex if "\u4e00" <= ch <= "\u9fff" or ch.isdigit())[:10]
        if len(probe) < 8:
            continue
        ex_clean = "".join(ch for ch in ex if not ch.isspace())
        if ex_clean in all_clean:  # v2 已有（整段在场才跳过）
            continue
        hit = None
        for f in old_files:
            t = io.open(f, encoding="utf-8", errors="replace").read()
            oc_t, omap_t = clean_map(t)
            i = oc_t.find(probe)
            if i >= 0:
                hit = (f, t, oc_t)
                break
        if not hit:
            continue
        ofile, otext, oc = hit
        # 老源里该段在清洗流中的位置
        ci = oc.find(probe)
        para_raw = ex
        # 前邻尾 18 字 / 后邻首 18 字（老源清洗流）
        prior = oc[max(0, ci - 18):ci]
        # 段末在老源里的位置
        end_probe = "".join(ch for ch in ex[-14:] if "\u4e00" <= ch <= "\u9fff" or ch.isdigit())
        ei = oc.find(end_probe, ci) if end_probe else -1
        next_head = oc[(ei + len(end_probe)):(ei + len(end_probe) + 18)] if ei >= 0 else ""
        # 选文件：优先同名
        cand = str(V2 / Path(ofile).name)
        f_candidates = [cand] if cand in v2_clean else list(v2_clean)
        placed = None
        for f in f_candidates:
            vc = v2_clean[f]
            for tag, anchor in (("prior", prior), ("next", next_head)):
                if len(anchor) < 12:
                    continue
                k = vc.rfind(anchor) if tag == "prior" else vc.find(anchor)
                if k < 0:
                    continue
                insert_at = (k + len(anchor)) if tag == "prior" else k
                # 由清洗位映射回原文位
                raw = v2_map[f][insert_at] if insert_at < len(v2_map[f]) else len(v2_raw[f])
                # 校验：插在两条锚之间
                ok = True
                if tag == "prior" and next_head and len(next_head) >= 12:
                    nn = vc.find(next_head, insert_at)
                    if nn < 0:
                        ok = False
                placed = (f, raw, tag, ok)
                break
            if placed:
                break
        if placed:
            plan.append((r, placed, para_raw, prior, next_head))

    ok_n = sum(1 for p in plan if p[1][3])
    print(f"待回插 {len(plan)} 段（校验通过 {ok_n}，仅单锚 {len(plan) - ok_n}）")
    for r, (f, raw, tag, ok), para, prior, next_head in plan[:25]:
        print(f"  [{'両锚✓' if ok else tag}] {r[1][:12]:12} {Path(f).name[:16]:16} | {para[:52]}")
    if not args.apply:
        print("（dry-run）")
        return

    from collections import defaultdict
    per = defaultdict(list)
    for r, (f, raw, tag, ok), para, prior, next_head in plan:
        per[f].append((raw, para, r[1]))
    log = ["# 残文误伤回插记录（2026-10-03，前邻尾串定位）", ""]
    for f, items in per.items():
        t = v2_raw[f]
        for raw, para, ch in sorted(items, key=lambda x: -x[0]):
            t = t[:raw] + "\n\n" + para + "\n\n" + t[raw:]
            log.append(f"- {Path(f).name} | {ch} | {para[:60]}")
        io.open(f, "w", encoding="utf-8", newline="\n").write(t)
        print(f"写回 {Path(f).name}: {len(items)} 段")
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(log) + "\n")
    print("日志:", LOG)


if __name__ == "__main__":
    main()
