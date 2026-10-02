# -*- coding: utf-8 -*-
"""批次3：上_1 全册共识比对（分片并行版）——按卷文件切6片，各自对齐后汇总。

输出: output/reports/batch3/上_1_consensus_full.json / .md
"""
import difflib
import importlib.util
import io
import json
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "reports" / "batch3"

CHUNKS = [  # (v2文件, 锚起, 锚止)
    ("序与凡例.md", 1, 30),
    ("总述与大事记.md", 1, 130),
    ("第一卷_自然环境.md", 120, 215),
    ("第二卷_建置区划.md", 210, 235),
    ("第三卷_区县概况.md", 230, 280),
    ("第四卷_人口（part01_部分）.md", 275, 305),
]


def run_chunk(args):
    fn, start, end = args
    spec = importlib.util.spec_from_file_location(
        "cc", ROOT / "scripts" / "consensus_compare_v2_20261001.py")
    cc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cc)

    v2pg = [(p, t) for p, t in cc.v2_pages(ROOT / "workbench" / "body_chapters_v2" / fn)
            if start <= p <= end]
    v2_stream = "".join(t for _, t in v2pg)
    v2_pos2page = {}
    off = 0
    for p, t in v2pg:
        for k in range(len(t)):
            v2_pos2page[off + k] = p
        off += len(t)
    pd, _ = cc.engine_stream("上_1", "paddle", start, end)
    rp, _ = cc.engine_stream("上_1", "rapid", start, end)
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
        rec = {"page": page, "v2": seg_v2, "paddle": seg_pd, "rapid": seg_rp,
               "ctx": ctx, "file": fn}
        if tag == "replace" and seg_v2 and seg_pd:
            if seg_v2 == seg_rp:
                stats["paddle_noise"] += 1
                continue
            rec["type"] = "FLAG_A" if seg_pd == seg_rp else "FLAG_B"
        elif tag == "delete":
            rec["type"] = "FLAG_X"
        elif tag == "insert":
            rec["type"] = "FLAG_M"
            rec["ctx"] = (v2_stream[max(0, i1 - 12): i1] + "⟨漏⟩" + v2_stream[i1: i1 + 12])
        else:
            continue
        flags.append(rec)
        stats[rec["type"]] += 1
    return {"file": fn, "pages": len(v2pg), "v2_chars": len(v2_stream),
            "pd_chars": len(pd), "rp_chars": len(rp), "stats": dict(stats), "flags": flags}


def main():
    with ProcessPoolExecutor(max_workers=3) as ex:
        results = list(ex.map(run_chunk, CHUNKS))
    all_flags = [f for r in results for f in r["flags"]]
    stats = Counter()
    for r in results:
        stats.update(r["stats"])
    tot_v2 = sum(r["v2_chars"] for r in results)
    tot_pd = sum(r["pd_chars"] for r in results)
    tot_rp = sum(r["rp_chars"] for r in results)
    tot_pg = sum(r["pages"] for r in results)
    summary = {"part": "上_1", "pages": "1-300（全册，分片）", "v2_pages": tot_pg,
               "v2_chars": tot_v2, "paddle_chars": tot_pd, "rapid_chars": tot_rp,
               "stats": dict(stats), "chunks": [{k: r[k] for k in
                ("file", "pages", "v2_chars", "pd_chars", "rp_chars", "stats")} for r in results]}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    io.open(OUT_DIR / "上_1_consensus_full.json", "w", encoding="utf-8").write(
        json.dumps({"summary": summary, "flags": all_flags}, ensure_ascii=False, indent=1))
    lines = [f"# 上_1 三方共识比对（1-300 全册，分片）", "",
             f"- v2 流 {tot_v2} 字（{tot_pg} 页） | paddle {tot_pd} 字 | rapid {tot_rp} 字",
             f"- FLAG_A 疑似v2错字: {stats['FLAG_A']} | FLAG_B 三方不同: {stats['FLAG_B']}",
             f"- FLAG_M 疑漏: {stats['FLAG_M']} | FLAG_X 疑多: {stats['FLAG_X']}",
             f"- 噪声过滤: 页眉 {stats['header_noise']} | 表格残文 {stats['table_residue']} | paddle单方 {stats['paddle_noise']}",
             ""]
    for t in ("FLAG_A", "FLAG_B", "FLAG_M", "FLAG_X"):
        lines.append(f"## {t} 明细（{stats[t]}）")
        lines.append("")
        for r in all_flags:
            if r["type"] == t:
                lines.append(f"- p{r['page']} v2「{r['v2']}」 pd「{r['paddle']}」 rp「{r['rapid']}」 …{r['ctx']}")
        lines.append("")
    io.open(OUT_DIR / "上_1_consensus_full.md", "w", encoding="utf-8").write("\n".join(lines))
    print("stats:", dict(stats))
    print("written", OUT_DIR / "上_1_consensus_full.md")


if __name__ == "__main__":
    main()
