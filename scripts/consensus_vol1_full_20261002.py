# -*- coding: utf-8 -*-
"""批次3：上_1 全册（S-0013..0300）双引擎共识比对 —— 复用 consensus_compare_v2 的算法

输出: output/reports/batch3/上_1_consensus_full.json / .md
"""
import difflib
import importlib.util
import io
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "reports" / "batch3"

spec = importlib.util.spec_from_file_location(
    "cc", ROOT / "scripts" / "consensus_compare_v2_20261001.py")
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

V2FILES = [
    "序与凡例.md", "总述与大事记.md", "第一卷_自然环境.md",
    "第二卷_建置区划.md", "第三卷_区县概况.md", "第四卷_人口（part01_部分）.md",
]
START, END = 1, 300


def main():
    v2pg = []
    for fn in V2FILES:
        v2pg.extend(cc.v2_pages(ROOT / "workbench" / "body_chapters_v2" / fn))
    v2pg = sorted({p: t for p, t in v2pg if START <= p <= END}.items())
    v2_stream = "".join(t for _, t in v2pg)
    v2_pos2page = {}
    off = 0
    for p, t in v2pg:
        for k in range(len(t)):
            v2_pos2page[off + k] = p
        off += len(t)
    print("v2 页数", len(v2pg), "字符", len(v2_stream), flush=True)

    pd, _ = cc.engine_stream("上_1", "paddle", START, END)
    rp, _ = cc.engine_stream("上_1", "rapid", START, END)
    print("paddle 字符", len(pd), "rapid 字符", len(rp), flush=True)
    map_rp = cc.boundary_map(v2_stream, rp)

    flags, stats = [], Counter()
    sm = difflib.SequenceMatcher(None, v2_stream, pd, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        seg_v2 = v2_stream[i1:i2]
        seg_pd = pd[j1:j2]
        seg_rp = rp[map_rp[i1]:map_rp[i2]] if map_rp[i2] >= map_rp[i1] else ""
        seg_all = seg_v2 or seg_pd
        if not seg_all or not cc.HAN.search(seg_all):
            continue
        page = v2_pos2page.get(i1) or v2_pos2page.get(max(i1 - 1, 0), 0)
        if cc.HEADER_PAT.match(seg_pd or "") or cc.HEADER_PAT.match(seg_v2 or ""):
            stats["header_noise"] += 1
            continue
        if cc.digit_ratio(seg_all) > 0.5:
            stats["table_residue"] += 1
            continue
        ctx = (v2_stream[max(0, i1 - 12): i1] + "【" + (seg_v2 or "⟨无⟩") + "】"
               + v2_stream[i2: i2 + 12])
        rec = {"page": page, "v2": seg_v2, "paddle": seg_pd, "rapid": seg_rp, "ctx": ctx}
        if tag == "replace" and seg_v2 and seg_pd:
            if seg_v2 == seg_rp:
                stats["paddle_noise"] += 1
                continue
            if seg_pd == seg_rp:
                rec["type"] = "FLAG_A"
            else:
                rec["type"] = "FLAG_B"
        elif tag == "delete":
            rec["type"] = "FLAG_X"
        elif tag == "insert":
            rec["type"] = "FLAG_M"
            rec["ctx"] = (v2_stream[max(0, i1 - 12): i1] + "⟨漏⟩" + v2_stream[i1: i1 + 12])
        else:
            continue
        flags.append(rec)
        stats[rec["type"]] += 1

    summary = {"part": "上_1", "pages": f"{START}-{END}（全册）",
               "v2_files": V2FILES, "v2_pages": len(v2pg), "v2_chars": len(v2_stream),
               "paddle_chars": len(pd), "rapid_chars": len(rp), "stats": dict(stats)}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    io.open(OUT_DIR / "上_1_consensus_full.json", "w", encoding="utf-8").write(
        json.dumps({"summary": summary, "flags": flags}, ensure_ascii=False, indent=1))

    lines = [f"# 上_1 三方共识比对（{START}-{END} 全册）", "",
             f"- v2 流 {len(v2_stream)} 字（{len(v2pg)} 页） | paddle {len(pd)} 字 | rapid {len(rp)} 字",
             f"- FLAG_A 疑似v2错字: {stats['FLAG_A']} | FLAG_B 三方不同: {stats['FLAG_B']}",
             f"- FLAG_M 疑漏: {stats['FLAG_M']} | FLAG_X 疑多: {stats['FLAG_X']}",
             f"- 噪声过滤: 页眉 {stats['header_noise']} | 表格残文 {stats['table_residue']} | paddle单方 {stats['paddle_noise']}",
             ""]
    for t in ("FLAG_A", "FLAG_B", "FLAG_M", "FLAG_X"):
        lines.append(f"## {t} 明细（{stats[t]}）")
        lines.append("")
        for r in flags:
            if r["type"] == t:
                lines.append(f"- p{r['page']} v2「{r['v2']}」 pd「{r['paddle']}」 rp「{r['rapid']}」 …{r['ctx']}")
        lines.append("")
    io.open(OUT_DIR / "上_1_consensus_full.md", "w", encoding="utf-8").write("\n".join(lines))
    print("stats:", dict(stats))
    print("written", OUT_DIR / "上_1_consensus_full.md")


if __name__ == "__main__":
    main()
