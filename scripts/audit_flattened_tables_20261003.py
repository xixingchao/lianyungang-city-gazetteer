# -*- coding: utf-8 -*-
"""压平表格残片审计：扫描全库疑似压平表格残片 → 判断是否已被已核结构化表覆盖。

输出: output/reports/progress/压平表格残片审计_20261003.md
"""
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
OUT = os.path.join(ROOT, "output", "reports", "progress", "压平表格残片审计_20261003.md")

pat_num = re.compile(r"[0-9][0-9.,%~～、]{25,}")
pat_unit = re.compile(r"^[（(]?[^）)（）]{0,6}[（(](?:吨|万元|万件|人|亩|平方米|万米|公里|千瓦|台|个|只|头|张|辆|艘|万双|万条|万只)[）)]$")
ANCH = re.compile(r"<!--\s*page-anchor:\s*LYG-(?:S-)?(\d+)\s*-->")
TABNUM = re.compile(r"表\s*(\d+)\s*[-—–]\s*(\d+)")

# 载入已核结构化表
tables = []
for p in glob.glob(os.path.join(TBL, "*", "data", "*.json")):
    try:
        d = json.load(io.open(p, encoding="utf-8"))
    except Exception:
        continue
    if d.get("status") != "verified" or not d.get("rows"):
        continue
    nums = TABNUM.findall(str(d.get("table_number") or ""))
    tables.append({
        "id": d.get("table_id"),
        "num": f"{int(nums[0][0])}-{int(nums[0][1])}" if nums else "",
        "pages": set(int(x) for x in (d.get("pages") or []) if str(x).isdigit()),
    })

findings = []
for f in sorted(glob.glob(os.path.join(V2, "*.md"))):
    lines = io.open(f, encoding="utf-8").read().split("\n")
    for i, l in enumerate(lines):
        s = l.strip()
        if not s or s.startswith("<!--") or s.startswith("{{"):
            continue
        kind = None
        if pat_num.search(s):
            kind = "num"
        elif pat_unit.match(s):
            kind = "unit"
        if not kind:
            continue
        # 表号（向前 40 行）
        num = ""
        for j in range(i, max(0, i - 40), -1):
            m = TABNUM.search(lines[j])
            if m:
                num = f"{int(m.group(1))}-{int(m.group(2))}"
                break
        # 页锚（向前）
        pg = None
        for j in range(i, max(0, i - 400), -1):
            m = ANCH.search(lines[j])
            if m:
                pg = int(m.group(1))
                break
        covered = None
        for t in tables:
            # 仅接受表号精确匹配；页匹配证据弱，另记为“页邻接（需核）”
            if num and t["num"] == num:
                covered = t["id"]
                break
        page_adj = None
        if not covered and pg:
            for t in tables:
                if pg in t["pages"]:
                    page_adj = t["id"]
                    break
        findings.append({
            "file": os.path.basename(f), "line": i + 1, "kind": kind,
            "num": num, "page": pg, "covered": covered, "page_adj": page_adj, "text": s[:90],
        })

covered_n = sum(1 for x in findings if x["covered"])
adj_n = sum(1 for x in findings if not x["covered"] and x["page_adj"])
print(f"残片 {len(findings)}；已覆盖 {covered_n}；待重建 {len(findings)-covered_n}")

buf = ["# 压平表格残片审计（2026-10-03）", "",
       f"扫描全库疑似压平/残片行共 **{len(findings)}** 处；其中 **{covered_n}** 处表号精确命中已核结构化表"
       f"（可直接撤残片），**{adj_n}** 处仅页邻接（需人工核对），**{len(findings)-covered_n-adj_n}** 处需回源重建。", "",
       "## 一、已被结构化表覆盖（可撤残片）", ""]
for x in findings:
    if x["covered"]:
        buf.append(f"- `{x['file']}` L{x['line']} [{x['kind']}] 表{x['num'] or '?'} p{x['page'] or '?'} → 覆盖表 {x['covered']} ｜ {x['text']}")
buf += ["", "## 二、页邻接已核表（需人工核对该表是否即本残片所属表）", ""]
for x in findings:
    if not x["covered"] and x["page_adj"]:
        buf.append(f"- `{x['file']}` L{x['line']} [{x['kind']}] p{x['page'] or '?'} 页邻接表 {x['page_adj']} ｜ {x['text']}")
buf += ["", "## 三、需回源重建（无表号、无页邻接已核表）", ""]
for x in findings:
    if not x["covered"] and not x["page_adj"]:
        buf.append(f"- `{x['file']}` L{x['line']} [{x['kind']}] p{x['page'] or '?'} ｜ {x['text']}")
io.open(OUT, "w", encoding="utf-8").write("\n".join(buf))
print("报告:", OUT)
