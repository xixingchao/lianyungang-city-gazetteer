# -*- coding: utf-8 -*-
r"""回插被"残文撤出"误删的正文档落（2026-10-03）。

策略（按优先级）：
 A 邻文对齐：取老源里该段**前/后各若干字**的上下文，去 v2 里找最长公共块（≥12 字），
   插在该块之后（用后邻则插在之前）。
 B 页锚对齐：A 失败时，用该段所在页锚（LYG-XXXX）在 v2 里定位同页，再在"同页段落集合"里
   用最长公共块定位；仍失败则退回"插在该页锚后的第一段之前"。
写回：body_chapters_v2/<对应文件> 与 output/final_reader/连云港市志_全书.html（同步）。
用法：
  python restore_residue_damage_20261003.py            # dry-run，列出每条的插入点
  python restore_residue_damage_20261003.py --apply    # 落笔
  python restore_residue_damage_20261003.py --limit 18 --apply   # 只做前 N 条
"""
from __future__ import annotations

import argparse
import glob
import io
import re
import shutil
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "workbench" / "body_chapters_v2"
OLD = ROOT / "workbench" / "body_chapters"
READER = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
LOG = ROOT / "output" / "reports" / "progress" / "20261003_残文误伤回插记录.md"
ANCH = re.compile(r"<!--\s*page-anchor:\s*LYG-(?:S-)?(\d+)\s*-->")


def load_rows(report: Path) -> list[list[str]]:
    lines = io.open(report, encoding="utf-8").read().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("## 撤出清单"))
    rows = []
    for l in lines[start + 2:]:
        if not l.startswith("|"):
            continue
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) >= 4 and cells[0].isdigit():
            rows.append(cells)
    return rows


def clean(s: str) -> str:
    s = re.sub(r"<!--.*?-->", "", s)
    s = re.sub(r"[#*>`|]", "", s)
    return re.sub(r"\s+", "", s)


def probe_words(para: str, n: int = 12) -> list[str]:
    """探针：段中连续 n 个汉字（多处取样）。"""
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
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    rows = load_rows(Path(args.report))
    v2_files = sorted(glob.glob(str(V2 / "*.md")))
    v2_text = {f: io.open(f, encoding="utf-8").read() for f in v2_files}
    all_v2 = "".join(v2_text.values())
    old_files = [f for f in sorted(glob.glob(str(OLD / "**" / "*.md"), recursive=True)) if ".bak" not in f]

    # 1) 找出"像正文且 v2 缺失"的条目，并定位到老源
    targets = []
    for r in rows:
        ex = r[3]
        if "。" not in ex or ex.startswith("续上表") or ex.startswith("注：源 OCR"):
            continue
        cjk = sum(1 for ch in ex if "\u4e00" <= ch <= "\u9fff")
        digits = sum(1 for ch in ex if ch.isdigit())
        if cjk < 25:
            continue
        # 排除表格残文：含"表X-Y"式表题、或数字占比过高（>35%）
        if re.search(r"表\s*\d+\s*[-－—]\s*\d+", ex) or digits > (cjk + digits) * 0.35:
            continue
        if any(p in all_v2 for p in probe_words(ex, 12)):
            continue
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
        if hit:
            targets.append((r, hit))
    print(f"待回插候选（像正文 + v2 缺失 + 老源可定位）：{len(targets)}")
    if args.limit:
        targets = targets[: args.limit]

    # 2) 逐条算插入点
    plan = []
    for r, (ofile, otext, oi) in targets:
        ex = clean(r[3])
        cand = str(V2 / Path(ofile).name)
        if cand in v2_text:
            v2file = cand
        else:                                      # 老源文件名与 v2 不一致时按内容找
            v2file = max(v2_text, key=lambda f: len(v2_text[f]))
        v2t = v2_text[v2file]
        before = clean(otext[max(0, oi - 220):oi])[-60:]
        after = clean(otext[oi + len(r[3]):oi + len(r[3]) + 220])[:60]
        # A 邻文对齐
        sm = SequenceMatcher(None, before, v2t, autojunk=False)
        m = sm.find_longest_match(0, len(before), 0, len(v2t))
        if m.size >= 12:
            pos = m.b + m.size
            anchor_used = f"前邻({m.size}字)"
        else:
            sm2 = SequenceMatcher(None, after, v2t, autojunk=False)
            m2 = sm2.find_longest_match(0, len(after), 0, len(v2t))
            if m2.size >= 12:
                pos = m2.b
                anchor_used = f"后邻({m2.size}字)"
            else:
                # B 页锚对齐
                mm = None
                for x in ANCH.finditer(otext, 0, oi):
                    mm = x
                if mm:
                    key = f"<!-- page-anchor: LYG-{mm.group(1)} -->"
                    k = v2t.find(key)
                    if k < 0:
                        k = v2t.find(key.replace("LYG-", "LYG-S-"))
                    if k >= 0:
                        pos = v2t.find("\n\n", k)
                        pos = pos + 2 if pos >= 0 else k + len(key)
                        anchor_used = f"页锚{mm.group(1)}"
                    else:
                        plan.append((r, v2file, None, "页锚不在 v2", ex[:60]))
                        continue
                else:
                    plan.append((r, v2file, None, "无锚无邻", ex[:60]))
                    continue
        plan.append((r, v2file, pos, anchor_used, ex[:60]))

    ok = [p for p in plan if p[2] is not None]
    print(f"可落笔：{len(ok)}；不可落笔：{len(plan) - len(ok)}")
    for r, f, pos, why, head in plan[: int(args.limit) if args.limit else 25]:
        print(f'  [{why}] {r[1][:12]:12} {Path(f).name[:18]:18} | {head}')

    if not args.apply:
        print("（dry-run，未写回）")
        return

    # 3) 写回（按位置倒序插入，避免位移）
    from collections import defaultdict
    per_file = defaultdict(list)
    for r, f, pos, why, head in ok:
        per_file[f].append((pos, clean(r[3]), r, why))
    log = ["# 残文误伤回插记录（2026-10-03）", "", f"回插 {len(ok)} 段", "",
           "| 章节 | 文件 | 定位方式 | 段首 |", "| --- | --- | --- | --- |"]
    for f, items in per_file.items():
        text = v2_text[f]
        for pos, para, r, why in sorted(items, key=lambda x: -x[0]):
            text = text[:pos] + "\n\n" + para + "\n\n" + text[pos:]
            log.append(f"| {r[1][:12]} | {Path(f).name[:20]} | {why} | {para[:40]} |")
        io.open(f, "w", encoding="utf-8", newline="\n").write(text)
        print(f"v2 写回 {Path(f).name}: {len(items)} 段")
    # 阅读版：按同样的邻文在 HTML 里定位，插入 <p>…</p>
    rt = io.open(READER, encoding="utf-8").read()
    rd_hit = rd_miss = 0
    for f, items in per_file.items():
        for pos, para, r, why in items:
            # 取该段在老源里的前邻（用 v2 写回时同样的方法）
            key = para[:20]
            if key in rt:
                continue
            # 用段首 12 字在阅读版找不着，则用其前 30 字上下文
            ctx = None
            for cand_len in (40, 30, 20, 14):
                seg = para[:cand_len]
                if seg and seg in rt:
                    ctx = seg
                    break
            # 直接尝试：在阅读版里找 v2 写回位置之后的邻文
            probe = para[-24:]
            idx = rt.find(probe)
            if idx >= 0:
                end = rt.find("</p>", idx)
                if end >= 0:
                    insert_at = end + len("</p>")
                    rt = rt[:insert_at] + f"\n<p>{para}</p>" + rt[insert_at:]
                    rd_hit += 1
                    continue
            rd_miss += 1
            print("阅读版待人工定位：", para[:40])
    io.open(READER, "w", encoding="utf-8", newline="\n").write(rt)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(log) + "\n")
    print(f"阅读版：自动命中 {rd_hit} 段，待人工 {rd_miss} 段；日志 {LOG}")


if __name__ == "__main__":
    main()
