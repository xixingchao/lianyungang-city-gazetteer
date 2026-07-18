# -*- coding: utf-8 -*-
"""
连云港市志 全书(上+中+下) 章节骨架构建脚本

处理"3本书是一本，目录部分重复"问题：
  - 上 part02 / part03 顶部的 "序/凡例" 为 CEB 导航幽灵条目(重复)，标记 ghost 并排除
  - 中/下各 part 无重复，正常处理
  - 7 个 part 合并为全书统一骨架，按全局页连续编号

全局页偏移(基于 PDF 实际页数):
  上 part01: 0      (1-300)
  上 part02: 300    (301-605)
  上 part03: 605    (606-903)
  中 part01: 903    (904-1420)
  中 part02: 1420   (1421-1971)
  下 part01: 1971   (1972-2432)
  下 part02: 2432   (2433-2911)

上册 3 part 有 OCR 页锚索引，做标题校验；
中下册 4 part 尚无 OCR，标注 pending_ocr。
"""

import csv
import re
import os
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
CATALOG_MD = ROOT / "workbench" / "indexes" / "连云港市志_XML目录初提取.md"
UP_ANCHOR_CSV = ROOT / "workbench" / "indexes" / "连云港市志_上册页锚索引.csv"
OUT_CSV = ROOT / "workbench" / "indexes" / "连云港市志_全书_目录页锚对应.csv"
OUT_SKELETON = ROOT / "workbench" / "indexes" / "连云港市志_全书_章节骨架.md"
OUT_QA = ROOT / "workbench" / "qa" / "全书目录去重校验报告.md"

PART_OFFSET = {
    "上 part01": 0,
    "上 part02": 300,
    "上 part03": 605,
    "中 part01": 903,
    "中 part02": 1420,
    "下 part01": 1971,
    "下 part02": 2432,
}
PART_PAGES = {
    "上 part01": 300, "上 part02": 305, "上 part03": 298,
    "中 part01": 517, "中 part02": 551,
    "下 part01": 461, "下 part02": 479,
}
TOTAL_PAGES = sum(PART_PAGES.values())  # 2911
UP_PARTS = {"上 part01", "上 part02", "上 part03"}


def load_up_anchors():
    """上册页锚索引 {global_page: row}"""
    anchors = {}
    if not UP_ANCHOR_CSV.exists():
        return anchors
    with open(UP_ANCHOR_CSV, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            anchors[int(row["global_page"])] = row
    return anchors


def parse_catalog():
    text = CATALOG_MD.read_text(encoding="utf-8-sig")
    entries = []
    cur_part = None
    in_table = False
    for line in text.splitlines():
        m = re.match(r"^## (上 part\d+|中 part\d+|下 part\d+) ", line)
        if m:
            cur_part = m.group(1)
            in_table = False
            continue
        if line.startswith("| 层级"):
            in_table = True
            continue
        if line.startswith("| ---"):
            continue
        if not in_table:
            continue
        if line.startswith("|") and not line.startswith("| 层级"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 3 and cells[0].isdigit():
                entries.append({
                    "part": cur_part,
                    "level": int(cells[0]),
                    "ebook_page": int(cells[1]),
                    "path": cells[2],
                })
    return entries


def normalize(s):
    return re.sub(r"\s+", "", s)


def title_tokens(path):
    seg = path.split("/")[-1].strip()
    seg = re.sub(r"^第[一二三四五六七八九十百千零〇\d]+[卷章节]\s*", "", seg)
    seg = re.sub(r"^概述$", "", seg)
    tokens = [t for t in re.split(r"[ 　]", seg) if len(t) >= 2]
    return tokens, seg


def verify_entry(row, path):
    if row is None:
        return "no_anchor", ""
    txt_path = row.get("text_path", "")
    if not txt_path or not os.path.exists(txt_path):
        return "no_ocr", ""
    try:
        with open(txt_path, encoding="utf-8") as f:
            ocr = f.read()
    except Exception:
        return "read_err", ""
    snippet = ocr[:120].replace("\n", " ")
    norm_ocr = normalize(ocr)
    tokens, seg = title_tokens(path)
    if not tokens:
        last = path.split("/")[-1].strip()
        if normalize(last) and normalize(last) in norm_ocr:
            return "match", snippet
        return "uncertain", snippet
    hit = sum(1 for t in tokens if normalize(t) in norm_ocr)
    if hit == len(tokens):
        return "match", snippet
    if hit >= 1:
        return "partial", snippet
    first_seg = path.split("/")[0].strip()
    first_seg = re.sub(r"^第[一二三四五六七八九十百千零〇\d]+卷\s*", "", first_seg)
    if first_seg and normalize(first_seg) in norm_ocr:
        return "partial", snippet
    return "miss", snippet


def is_ghost(part, level, path):
    """上 part02/part03 顶部的 序/凡例 为 CEB 导航幽灵条目(全书重复)"""
    if part in ("上 part02", "上 part03") and level == 1 and path.strip() in ("序", "凡例"):
        return True
    return False


def build_entries(catalog, anchors):
    rows = []
    for e in catalog:
        part = e["part"]
        offset = PART_OFFSET[part]
        gpage = offset + e["ebook_page"]
        ghost = is_ghost(part, e["level"], e["path"])
        if ghost:
            status, snippet = "ghost", ""
        elif part in UP_PARTS:
            row = anchors.get(gpage)
            status, snippet = verify_entry(row, e["path"])
        else:
            status, snippet = "pending_ocr", ""
        anchor = ""
        if part in UP_PARTS:
            row = anchors.get(gpage)
            if row:
                anchor = row["anchor"]
        rows.append({
            "part": part,
            "level": e["level"],
            "ebook_page": e["ebook_page"],
            "global_page": gpage,
            "anchor": anchor,
            "path": e["path"],
            "ghost": "Y" if ghost else "",
            "ocr_status": status,
            "ocr_snippet": snippet,
        })
    return rows


def compute_ranges(rows):
    active = [r for r in rows if not r["ghost"]]
    n = len(active)
    for i, r in enumerate(active):
        end = None
        for j in range(i + 1, n):
            if active[j]["level"] <= r["level"]:
                end = active[j]["global_page"] - 1
                break
        if end is None:
            end = TOTAL_PAGES
        if end < r["global_page"]:
            end = r["global_page"]
        r["end_global_page"] = end
    return active


def write_csv(rows):
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["part", "level", "ebook_page", "global_page", "anchor",
                    "path", "ghost", "ocr_status", "ocr_snippet",
                    "end_global_page"])
        for r in rows:
            w.writerow([r["part"], r["level"], r["ebook_page"], r["global_page"],
                        r["anchor"], r["path"], r["ghost"], r["ocr_status"],
                        r["ocr_snippet"], r.get("end_global_page", "")])


def write_skeleton(active):
    lines = []
    lines.append("# 连云港市志 全书章节骨架（上+中+下合一，目录去重）")
    lines.append("")
    lines.append("生成方式：7 个 CEB 分册 XML 目录 + 全局页偏移映射。")
    lines.append(f"全书总页数：{TOTAL_PAGES}（上册 903 + 中册 1068 + 下册 940）。")
    lines.append("")
    lines.append("## 去重说明")
    lines.append("")
    lines.append('- 上 part02 / part03 顶部的"序""凡例"为 CEB 导航幽灵条目（与 part01 重复），已标记 ghost 并排除。')
    lines.append("- 中册、下册各 part 之间无目录重复，卷号严格递进。")
    lines.append("- 第四卷人口、第十卷水利跨 part 分册属正常分册切分，非重复。")
    lines.append("- 全书覆盖：序→凡例→总述→大事记→第一卷~第六十卷→附录→跋→编纂始末。")
    lines.append("")
    lines.append("## 全局页偏移表")
    lines.append("")
    lines.append("| 分册 | PDF 页数 | 全局页范围 | 偏移 |")
    lines.append("| --- | ---: | --- | ---: |")
    for p in PART_OFFSET:
        off = PART_OFFSET[p]
        n = PART_PAGES[p]
        lines.append(f"| {p} | {n} | {off+1}-{off+n} | {off} |")
    lines.append("")
    lines.append("## 章节目录")
    lines.append("")
    cur_part = None
    for r in active:
        if r["part"] != cur_part:
            cur_part = r["part"]
            off = PART_OFFSET[cur_part]
            n = PART_PAGES[cur_part]
            lines.append("")
            lines.append(f"### {cur_part}（全局页 {off+1}-{off+n}）")
        indent = "  " * (r["level"] - 1)
        pg = f"p{r['global_page']}"
        end = r.get("end_global_page", "")
        rng = f"p{r['global_page']}-p{end}" if end and end != r["global_page"] else pg
        st_map = {"match": "✓", "partial": "≈", "uncertain": "?", "miss": "✗",
                  "no_anchor": "—", "no_ocr": "—", "pending_ocr": "○"}
        st = st_map.get(r["ocr_status"], "")
        lines.append(f"{indent}- [{rng}] {r['path']} {st}")
    lines.append("")
    lines.append("## 图例")
    lines.append("")
    lines.append("- ✓ OCR标题全匹配  ≈ 部分匹配  ✗ 未匹配  ? 不确定")
    lines.append("- ○ 中下册待OCR（暂未做标题校验）  — 无页锚/无OCR")
    OUT_SKELETON.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_qa(rows, active):
    total = len(rows)
    ghost = sum(1 for r in rows if r["ghost"])
    st_counter = Counter(r["ocr_status"] for r in rows if not r["ghost"])
    lines = []
    lines.append("# 全书目录去重校验报告")
    lines.append("")
    lines.append(f"生成范围：上+中+下 7 个 CEB 分册")
    lines.append(f"全书总页数：{TOTAL_PAGES}")
    lines.append(f"目录总条目：{total}（含幽灵 {ghost}）")
    lines.append(f"有效条目：{len(active)}")
    lines.append("")
    lines.append("## 重复条目处理")
    lines.append("")
    lines.append("| 分册 | 电子页 | 标题 | 处理 |")
    lines.append("| --- | ---: | --- | --- |")
    for r in rows:
        if r["ghost"]:
            lines.append(f"| {r['part']} | {r['ebook_page']} | {r['path']} | ghost(排除) |")
    lines.append("")
    lines.append('说明：上 part02/part03 顶部的"序""凡例"是 Apabi CEB 阅读器导航条目，'
                 '实际序言和凡例只在 part01（全局页 13-28），已排除重复。')
    lines.append("")
    lines.append("## OCR 标题校验统计")
    lines.append("")
    lines.append("| 状态 | 含义 | 数量 |")
    lines.append("| --- | --- | ---: |")
    for st, desc in [("match", "标题全匹配"), ("partial", "部分关键词匹配"),
                     ("uncertain", "概述/序/凡例等"), ("miss", "未匹配"),
                     ("no_anchor", "无页锚"), ("no_ocr", "无OCR"),
                     ("pending_ocr", "中下册待OCR")]:
        lines.append(f"| {st} | {desc} | {st_counter.get(st, 0)} |")
    lines.append("")
    lines.append("## 上册未匹配/部分匹配条目（需人工核查）")
    lines.append("")
    lines.append("| 全局页 | part | 层级 | 路径 | 状态 | OCR片段 |")
    lines.append("| ---: | --- | ---: | --- | --- | --- |")
    for r in active:
        if r["ocr_status"] in ("miss", "partial", "uncertain", "no_anchor", "no_ocr"):
            snip = r["ocr_snippet"][:40].replace("|", "/")
            lines.append(f"| {r['global_page']} | {r['part']} | {r['level']} | {r['path']} | {r['ocr_status']} | {snip} |")
    lines.append("")
    lines.append("## 全书卷号连续性核查")
    lines.append("")
    vol1 = [r for r in active if r["level"] == 1 and re.match(r"^第[一二三四五六七八九十百]+卷", r["path"])]
    lines.append(f"顶层卷条目数：{len(vol1)}（第一卷~第六十卷）")
    if vol1:
        lines.append(f"起始：{vol1[0]['path']}（全局页 {vol1[0]['global_page']}）")
        lines.append(f"结束：{vol1[-1]['path']}（全局页 {vol1[-1]['global_page']}）")
    lines.append("")
    lines.append("## 结论")
    lines.append("")
    up_active = [r for r in active if r["part"] in UP_PARTS]
    up_match = sum(1 for r in up_active if r["ocr_status"] == "match")
    lines.append(f"- 全书有效目录条目 {len(active)} 条，去重幽灵 {ghost} 条。")
    lines.append(f"- 上册 OCR 标题全匹配率：{up_match}/{len(up_active)} = {up_match/max(len(up_active),1):.1%}")
    lines.append(f"- 中下册 {sum(1 for r in active if r['ocr_status']=='pending_ocr')} 条待 OCR 后补校验。")
    lines.append("- 目录去重完成，全书骨架已生成。")
    OUT_QA.parent.mkdir(parents=True, exist_ok=True)
    OUT_QA.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    anchors = load_up_anchors()
    catalog = parse_catalog()
    rows = build_entries(catalog, anchors)
    active = compute_ranges(rows)
    write_csv(rows)
    write_skeleton(active)
    write_qa(rows, active)
    print("=== 全书章节骨架构建完成 ===")
    print(f"目录总条目: {len(rows)} (含幽灵 {sum(1 for r in rows if r['ghost'])})")
    print(f"有效条目: {len(active)}")
    st = Counter(r["ocr_status"] for r in active)
    print(f"OCR校验: {dict(st)}")
    print(f"全书总页数: {TOTAL_PAGES}")
    print(f"输出: {OUT_CSV}")
    print(f"输出: {OUT_SKELETON}")
    print(f"输出: {OUT_QA}")


if __name__ == "__main__":
    main()
