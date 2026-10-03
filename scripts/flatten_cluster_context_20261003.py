# -*- coding: utf-8 -*-
"""压平表格残片处理助手：按聚类块输出上下文（含前后 25 行）与可能对应的已核表。

用法: py -3 scripts/flatten_cluster_context_20261003.py <文件> <起行> <止行> [--pre 30] [--post 8]
"""
import argparse
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"E:\codex_Learing\project_连云港市志\repo"
V2 = os.path.join(ROOT, "workbench", "body_chapters_v2")
TBL = os.path.join(ROOT, "workbench", "table_entries")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("start", type=int)
    ap.add_argument("end", type=int)
    ap.add_argument("--pre", type=int, default=30)
    ap.add_argument("--post", type=int, default=8)
    args = ap.parse_args()

    lines = io.open(os.path.join(V2, args.file), encoding="utf-8").read().split("\n")
    seg = lines[max(0, args.start - 1 - args.pre): min(len(lines), args.end + args.post)]
    print(f"===== {args.file} L{args.start - args.pre}–L{args.end + args.post} =====")
    for j, l in enumerate(seg):
        ln = max(0, args.start - 1 - args.pre) + j + 1
        mark = " *" if args.start <= ln <= args.end else "  "
        if l.strip():
            print(f"{ln:6d}{mark} {l[:150]}")
    # 关键词匹配已核表
    blob = "\n".join(seg)
    keys = set(re.findall(r"[\u4e00-\u9fff]{2,8}", blob))
    scored = []
    for p in glob.glob(os.path.join(TBL, "*", "data", "*.json")):
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except Exception:
            continue
        if d.get("status") != "verified" or not d.get("rows"):
            continue
        title = str(d.get("title") or "") + " " + " ".join(str(c) for c in (d.get("columns") or []))
        score = sum(1 for k in keys if len(k) >= 3 and k in title)
        if score >= 2:
            scored.append((score, d.get("table_id"), d.get("table_number"), title[:50], d.get("pages")))
    scored.sort(reverse=True)
    print("--- 可能对应的已核表（关键词≥2）---")
    for s in scored[:6]:
        print("   ", s)


if __name__ == "__main__":
    main()
