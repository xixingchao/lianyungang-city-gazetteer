# -*- coding: utf-8 -*-
"""
连云港市志 上册 章节骨架构建脚本

输入：
  - workbench/indexes/连云港市志_XML目录初提取.md   (XML 目录初稿)
  - workbench/indexes/连云港市志_上册页锚索引.csv    (OCR 页锚索引)

输出：
  - workbench/indexes/连云港市志_上册_目录页锚对应.csv
  - workbench/indexes/连云港市志_上册_章节骨架.md
  - workbench/qa/上册目录映射校验报告.md

映射规则：
  part01 电子页 N -> 全局页 N        (offset 0)
  part02 电子页 N -> 全局页 300 + N  (offset 300)
  part03 电子页 N -> 全局页 605 + N  (offset 605)

part02 / part03 目录顶部的 “序 / 凡例” 为 CEB 导航幽灵条目（实际序言凡例在 part01），
本脚本将其标记为 ghost 并排除出章节骨架。
"""

import csv
import re
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # 连云港市志_workstation
CATALOG_MD = ROOT / "workbench" / "indexes" / "连云港市志_XML目录初提取.md"
ANCHOR_CSV = ROOT / "workbench" / "indexes" / "连云港市志_上册页锚索引.csv"
OUT_CSV = ROOT / "workbench" / "indexes" / "连云港市志_上册_目录页锚对应.csv"
OUT_SKELETON = ROOT / "workbench" / "indexes" / "连云港市志_上册_章节骨架.md"
OUT_QA = ROOT / "workbench" / "qa" / "上册目录映射校验报告.md"

PART_OFFSET = {"上 part01": 0, "上 part02": 300, "上 part03": 605}
# 仅处理上册三个 part
UP_PARTS = ["上 part01", "上 part02", "上 part03"]


# ---------- 1. 读取页锚索引 ----------
def load_anchors():
    """返回 {global_page_int: row_dict}"""
    anchors = {}
    with open(ANCHOR_CSV, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            anchors[int(row["global_page"])] = row
    return anchors


# ---------- 2. 解析目录 MD ----------
def parse_catalog():
    """返回 list[dict]: part, level, ebook_page, path"""
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
        if cur_part not in UP_PARTS:
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


# ---------- 3. 标题归一化与 OCR 校验 ----------
def normalize(s):
    return re.sub(r"\s+", "", s)


def title_tokens(path):
    """从目录路径取校验用关键词：最后一段的 章/节 标题"""
    seg = path.split("/")[-1].strip()
    # 去掉 “第X卷/第X章/第X节” 前缀后的实质词
    seg = re.sub(r"^第[一二三四五六七八九十百千零〇\d]+[卷章节]\s*", "", seg)
    seg = re.sub(r"^概述$", "", seg)
    tokens = [t for t in re.split(r"[ 　]", seg) if len(t) >= 2]
    return tokens, seg


def verify_entry(row, path):
    """读取该页 OCR 文本，判断目录标题是否出现。返回 (status, snippet)"""
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
        # 概述 / 序 / 凡例 等：宽松匹配路径末段
        last = path.split("/")[-1].strip()
        if normalize(last) and normalize(last) in norm_ocr:
            return "match", snippet
        return "uncertain", snippet
    hit = sum(1 for t in tokens if normalize(t) in norm_ocr)
    if hit == len(tokens):
        return "match", snippet
    if hit >= 1:
        return "partial", snippet
    # 卷/章 级别标题常以页眉形式出现，放宽：取第一段卷名
    first_seg = path.split("/")[0].strip()
    first_seg = re.sub(r"^第[一二三四五六七八九十百千零〇\d]+卷\s*", "", first_seg)
    if first_seg and normalize(first_seg) in norm_ocr:
        return "partial", snippet
    return "miss", snippet


# ---------- 4. 幽灵条目判定 ----------
def is_ghost(part, level, path):
    """part02/part03 顶部的 序/凡例 为导航幽灵条目"""
    if part in ("上 part02", "上 part03") and level == 1 and path.strip() in ("序", "凡例"):
        return True
    return False


# ---------- 5. 构建条目列表 ----------
def build_entries(catalog, anchors):
    rows = []
    for e in catalog:
        part = e["part"]
        offset = PART_OFFSET[part]
        gpage = offset + e["ebook_page"]
        row = anchors.get(gpage)
        ghost = is_ghost(part, e["level"], e["path"])
        if ghost:
            status, snippet = "ghost", ""
        else:
            status, snippet = verify_entry(row, e["path"])
        anchor = row["anchor"] if row else ""
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


# ---------- 6. 计算章节页范围 ----------
def compute_ranges(rows):
    """为每条目计算 end_global_page = 下一条同层或更高级条目的起始页 - 1"""
    active = [r for r in rows if not r["ghost"]]
    n = len(active)
    for i, r in enumerate(active):
        end = None
        for j in range(i + 1, n):
            if active[j]["level"] <= r["level"]:
                end = active[j]["global_page"] - 1
                break
        if end is None:
            end = 903  # 上册末页
        # 同页多节时 end 可能 < start，归并为单页
        if end < r["global_page"]:
            end = r["global_page"]
        r["end_global_page"] = end
    return active


# ---------- 7. 写 CSV ----------
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


# ---------- 8. 写章节骨架 MD ----------
def write_skeleton(active):
    lines = []
    lines.append("# 连云港市志 上册 章节骨架")
    lines.append("")
    lines.append("生成方式：XML 目录电子页 + per-part 偏移映射到全局 OCR 页锚。")
    lines.append("偏移：part01=0, part02=300, part03=605。")
    lines.append("part02/part03 顶部 序/凡例 为 CEB 导航幽灵条目，已排除。")
    lines.append("")
    cur_part = None
    for r in active:
        if r["part"] != cur_part:
            cur_part = r["part"]
            lines.append("")
            lines.append(f"## {cur_part}（全局页 {r['global_page']} 起）")
        indent = "  " * (r["level"] - 1)
        pg = f"p{r['global_page']}"
        end = r.get("end_global_page", "")
        rng = f"p{r['global_page']}-p{end}" if end and end != r["global_page"] else pg
        st = {"match": "✓", "partial": "≈", "uncertain": "?", "miss": "✗",
              "no_anchor": "—", "no_ocr": "—"}.get(r["ocr_status"], "")
        lines.append(f"{indent}- [{rng}] {r['path']} {st}")
    OUT_SKELETON.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------- 9. 特殊页标记 ----------
def mark_special_pages(anchors):
    """基于字符数与 OCR 文本标记低字符页、表格页、名单页"""
    special = {"low_char": [], "table": [], "list": []}
    for gp, row in sorted(anchors.items()):
        chars = int(row.get("chars", 0) or 0)
        txt_path = row.get("text_path", "")
        ocr = ""
        if txt_path and os.path.exists(txt_path):
            try:
                ocr = open(txt_path, encoding="utf-8").read()
            except Exception:
                ocr = ""
        if chars < 40:
            special["low_char"].append(gp)
        if ocr and re.search(r"续上表|续表|表\d+[-—]\d+", ocr):
            special["table"].append(gp)
        # 名单页启发式：大量短行 + 人名特征
        if ocr:
            short_lines = sum(1 for ln in ocr.splitlines() if 0 < len(ln.strip()) <= 12)
            if short_lines >= 15 and chars > 100:
                special["list"].append(gp)
    return special


# ---------- 10. 写校验报告 ----------
def write_qa(rows, active, special):
    from collections import Counter
    total = len(rows)
    ghost = sum(1 for r in rows if r["ghost"])
    st_counter = Counter(r["ocr_status"] for r in rows if not r["ghost"])
    lines = []
    lines.append("# 上册目录映射校验报告")
    lines.append("")
    lines.append(f"目录总条目：{total}（含幽灵 {ghost}）")
    lines.append(f"有效条目：{len(active)}")
    lines.append("")
    lines.append("## OCR 标题校验统计")
    lines.append("")
    lines.append("| 状态 | 含义 | 数量 |")
    lines.append("| --- | --- | ---: |")
    for st, desc in [("match", "标题全匹配"), ("partial", "部分关键词匹配"),
                     ("uncertain", "概述/序/凡例等无法精确匹配"),
                     ("miss", "未匹配"), ("no_anchor", "无页锚"),
                     ("no_ocr", "无 OCR 文本")]:
        lines.append(f"| {st} | {desc} | {st_counter.get(st, 0)} |")
    lines.append("")
    lines.append("## 未匹配 / 部分匹配条目（需人工核查）")
    lines.append("")
    lines.append("| 全局页 | part | 层级 | 路径 | 状态 | OCR片段 |")
    lines.append("| ---: | --- | ---: | --- | --- | --- |")
    for r in active:
        if r["ocr_status"] in ("miss", "partial", "uncertain", "no_anchor", "no_ocr"):
            snip = r["ocr_snippet"][:40].replace("|", "/")
            lines.append(f"| {r['global_page']} | {r['part']} | {r['level']} | {r['path']} | {r['ocr_status']} | {snip} |")
    lines.append("")
    lines.append("## 特殊页标记")
    lines.append("")
    lines.append(f"- 低字符页（<40字，封面/空白/过渡）：{len(special['low_char'])} 页")
    lines.append(f"- 表格页（含 续上表/表X-X）：{len(special['table'])} 页")
    lines.append(f"- 疑似名单页（多短行）：{len(special['list'])} 页")
    lines.append("")
    if special["low_char"]:
        lines.append("### 低字符页清单（前 40）")
        lines.append("")
        lines.append(", ".join(f"p{p}" for p in special["low_char"][:40]))
        lines.append("")
    if special["table"]:
        lines.append("### 表格页清单（前 40）")
        lines.append("")
        lines.append(", ".join(f"p{p}" for p in special["table"][:40]))
        lines.append("")
    lines.append("## 结论")
    lines.append("")
    match_rate = st_counter.get("match", 0) / max(len(active), 1)
    lines.append(f"- 有效条目标题全匹配率：{match_rate:.1%}")
    lines.append("- 未匹配条目需对照页图核查，常见原因：OCR 把章节标题识别为页眉、"
                 "标题跨页、该页为续表/图片页。")
    lines.append("- 低字符页与表格页已标记，后续正文精修时表格页只放占位，不混入 OCR 噪声。")
    OUT_QA.parent.mkdir(parents=True, exist_ok=True)
    OUT_QA.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------- main ----------
def main():
    anchors = load_anchors()
    catalog = parse_catalog()
    rows = build_entries(catalog, anchors)
    active = compute_ranges(rows)
    write_csv(rows)
    write_skeleton(active)
    special = mark_special_pages(anchors)
    write_qa(rows, active, special)
    print("=== 上册章节骨架构建完成 ===")
    print(f"目录总条目: {len(rows)} (含幽灵 {sum(1 for r in rows if r['ghost'])})")
    print(f"有效条目: {len(active)}")
    from collections import Counter
    st = Counter(r["ocr_status"] for r in active)
    print(f"OCR校验: {dict(st)}")
    print(f"低字符页: {len(special['low_char'])}  表格页: {len(special['table'])}  疑似名单页: {len(special['list'])}")
    print(f"输出: {OUT_CSV}")
    print(f"输出: {OUT_SKELETON}")
    print(f"输出: {OUT_QA}")


if __name__ == "__main__":
    main()
