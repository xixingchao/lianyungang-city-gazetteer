# -*- coding: utf-8 -*-
"""压平表格残片批量处理：按“就近表号命中已核表”规则自动撤残片；其余列人工清单。

用法:
  py -3 scripts/process_flattened_tables_20261003.py --report   # 只报告分类
  py -3 scripts/process_flattened_tables_20261003.py --apply    # 实际撤除命中项（v2）
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
OUT = os.path.join(ROOT, "output", "reports", "progress", "压平表格残片分类_20261003.md")

pat_num = re.compile(r"[0-9][0-9.,%~～、]{25,}")
pat_unit = re.compile(r"^[（(]?[^）)（）]{0,8}[（(](?:吨|万元|万件|人|亩|平方米|万米|公里|千瓦|台|个|只|头|张|辆|艘|万双|万条|万只|件|具|座)[）)]$")
TABNUM = re.compile(r"表\s*(\d+)\s*[-—–]\s*(\d+)")


def load_tables():
    out = {}
    pages = {}
    for p in glob.glob(os.path.join(TBL, "*", "data", "*.json")):
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except Exception:
            continue
        if d.get("status") != "verified" or not d.get("rows"):
            continue
        tom = TABNUM.search(str(d.get("table_number") or ""))
        if tom:
            key = f"{int(tom.group(1))}-{int(tom.group(2))}"
            out.setdefault(key, []).append(d)
        for pg in (d.get("pages") or []):
            if str(pg).isdigit():
                pages.setdefault(int(pg), []).append(d)
    return out, pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    tmap, pmap = load_tables()

    file_hits = {}
    for f in sorted(glob.glob(os.path.join(V2, "*.md"))):
        lines = io.open(f, encoding="utf-8").read().split("\n")
        for i, l in enumerate(lines):
            s = l.strip()
            if not s or s.startswith("<!--") or s.startswith("{{"):
                continue
            kind = None
            if pat_unit.match(s):
                kind = "unit"
            elif pat_num.search(s):
                kind = "num"
            if not kind:
                continue
            file_hits.setdefault(os.path.basename(f), []).append({"line": i + 1, "kind": kind, "text": s})

    rm, manual = [], []
    for fname, hits in file_hits.items():
        lines = io.open(os.path.join(V2, fname), encoding="utf-8").read().split("\n")
        # 逐处找就近表号（向前 300 行）与页锚
        ANCH = re.compile(r"<!--\s*page-anchor:\s*LYG-(?:S-)?(\d+)\s*-->")
        for h in hits:
            ln = h["line"]
            num = None
            for j in range(ln - 1, max(0, ln - 300), -1):
                m = TABNUM.search(lines[j])
                if m:
                    num = f"{int(m.group(1))}-{int(m.group(2))}"
                    break
            pg_pre = None
            for j in range(ln - 1, max(0, ln - 600), -1):
                m = ANCH.search(lines[j])
                if m:
                    pg_pre = int(m.group(1))
                    break
            pg_post = None
            for j in range(ln - 1, min(len(lines), ln + 600)):
                m = ANCH.search(lines[j])
                if m:
                    pg_post = int(m.group(1))
                    break
            pg = pg_pre
            match = None
            if num and num in tmap:
                cands = tmap[num]
                for d in cands:
                    pgs = [int(x) for x in (d.get("pages") or []) if str(x).isdigit()]
                    if pg_pre in pgs or (pg_post and pg_post in pgs):
                        match = d
                        break
                match = match or cands[0]
            else:
                for cand_pg in (pg_post, pg_pre):
                    if cand_pg and cand_pg in pmap:
                        cands = pmap[cand_pg]
                        if len(cands) == 1:
                            match = cands[0]
                            break
            rec = {**h, "file": fname, "num": num, "page": pg_pre, "page_post": pg_post,
                   "match": match.get("table_id") if match else None,
                   "match_title": (str(match.get("table_number")) + " " + str(match.get("title"))[:36]) if match else None}
            if match and h["kind"] == "unit":
                rm.append(rec)
            else:
                manual.append(rec)

    buf = [f"# 压平表格残片分类（2026-10-03）", "",
           f"- 可自动撤除（unit 残片 + 表号/唯一页命中已核表）：**{len(rm)}** 处",
           f"- 需人工处理（nu m 型或未命中）：**{len(manual)}** 处", "",
           "## 一、可自动撤除", ""]
    for r in rm:
        buf.append(f"- `{r['file']}` L{r['line']} 表{r['num'] or '?'} p{r['page'] or '?'} → {r['match']}（{r['match_title']}）｜ {r['text']}")
    buf += ["", "## 二、需人工处理", ""]
    for r in manual:
        buf.append(f"- `{r['file']}` L{r['line']} [{r['kind']}] 表{r['num'] or '?'} p{r['page'] or '?'}/{r.get('page_post') or '?'} → {r['match'] or '未命中'} ｜ {r['text']}")
    io.open(OUT, "w", encoding="utf-8").write("\n".join(buf))
    print(f"可撤 {len(rm)}；人工 {len(manual)}；报告 {OUT}")

    if args.apply and rm:
        by_file = {}
        for r in rm:
            by_file.setdefault(r["file"], set()).add(r["line"])
        for fname, lns in by_file.items():
            p = os.path.join(V2, fname)
            lines = io.open(p, encoding="utf-8").read().split("\n")
            keep = [l for i, l in enumerate(lines, start=1) if i not in lns]
            io.open(p, "w", encoding="utf-8", newline="").write("\n".join(keep))
            print(f"{fname}: 撤 {len(lns)} 行（{len(lines)}→{len(keep)}）")


if __name__ == "__main__":
    main()
