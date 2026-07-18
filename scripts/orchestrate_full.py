# -*- coding: utf-8 -*-
"""
连云港市志 全书统一推进脚本
OCR 完成后一键执行：页锚索引 → 中下册精修 → 全书汇总 → 校验 → 阅读版HTML

全局页偏移:
  上 part01: 0, part02: 300, part03: 605
  中 part01: 903, part02: 1420
  下 part01: 1971, part02: 2432
"""

import csv
import json
import re
import os
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
WORKSTATION = ROOT
OCR_BASE = ROOT / "workbench" / "ocr" / "raw"
INDEX_DIR = ROOT / "workbench" / "indexes"
BODY_DIR = ROOT / "workbench" / "body_chapters"
QA_DIR = ROOT / "workbench" / "qa"
REPORT_DIR = ROOT / "output" / "reports"
FINAL_DIR = ROOT / "output" / "final_reader"

PARTS = [
    ("上", "part01", 0, 300),
    ("上", "part02", 300, 305),
    ("上", "part03", 605, 298),
    ("中", "part01", 903, 517),
    ("中", "part02", 1420, 551),
    ("下", "part01", 1971, 461),
    ("下", "part02", 2432, 479),
]

# 中下册章节计划（从骨架CSV自动提取的卷范围）
MID_DOWN_CHAPTERS = [
    # 中 part01: 第十七卷~第二十九卷
    ("中/part01", 922, 1420, "第十七卷至第二十九卷（中part01）"),
    # 中 part02: 第三十卷~第四十二卷
    ("中/part02", 1438, 1971, "第三十卷至第四十二卷（中part02）"),
    # 下 part01: 第四十三卷~第五十一卷
    ("下/part01", 1987, 2432, "第四十三卷至第五十一卷（下part01）"),
    # 下 part02: 第五十二卷~第六十卷+附录+跋+编纂始末
    ("下/part02", 2447, 2911, "第五十二卷至第六十卷及附录（下part02）"),
]

HEADER_PATTERNS = [
    re.compile(r"^·\d+·连云港市志·[^\n]+\s*$", re.MULTILINE),
    re.compile(r"^[^\n]+·\d+·\s*$", re.MULTILINE),
    re.compile(r"^·\d+·\s*$", re.MULTILINE),
    re.compile(r"^连云港市志·[^\n]+\s*$", re.MULTILINE),
    re.compile(r"^\.\d+\.[iil]\s*$", re.MULTILINE),
    re.compile(r"^\.\d+\.\s*$", re.MULTILINE),
    re.compile(r"^[^\u4e00-\u9fff\n]{1,12}连云港市志·[\u4e00-\u9fff（）()]{1,25}\s*$", re.MULTILINE),
]

TABLE_PATTERN = re.compile(r"续上表|续表|表\d+[-—]\d+")


def step1_build_full_anchor_index():
    """生成全书页锚索引"""
    print("\n[步骤1] 生成全书页锚索引...")
    out_csv = INDEX_DIR / "连云港市志_全书页锚索引.csv"
    rows = []
    seq = 0
    for vol, part, offset, total in PARTS:
        raw_dir = OCR_BASE / vol / part
        img_dir = ROOT / "workbench" / "conversion" / "page_images" / vol / part
        for p in range(1, total + 1):
            gp = offset + p
            seq += 1
            anchor = f"LYG-{seq:04d}"
            txt_path = raw_dir / f"page_{p:04d}.txt"
            json_path = raw_dir / f"page_{p:04d}.json"
            img_path = img_dir / f"page_{p:04d}_180dpi.jpg"
            chars, lines, conf, status = 0, 0, "", "missing"
            if txt_path.exists():
                text = txt_path.read_text(encoding="utf-8", errors="replace")
                body = text.split("\n\n", 1)
                bt = body[1] if len(body) == 2 else text
                chars = len(bt.strip())
                status = "ok" if chars > 0 else "empty"
            if json_path.exists():
                try:
                    d = json.loads(json_path.read_text(encoding="utf-8"))
                    lines = d.get("line_count", 0)
                    conf = d.get("avg_confidence", "")
                except: pass
            rows.append({"anchor": anchor, "global_page": gp, "volume": vol,
                         "part": part, "page": p, "status": status, "chars": chars,
                         "lines": lines, "avg_confidence": conf,
                         "source_pdf": "", "image_path": str(img_path),
                         "text_path": str(txt_path), "json_path": str(json_path)})
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    ok = sum(1 for r in rows if r["status"] == "ok")
    print(f"  全书页锚: {len(rows)} 行 (ok={ok})")
    print(f"  输出: {out_csv}")
    return {int(r["global_page"]): r["anchor"] for r in rows}


def clean_text(text):
    lines = [ln for ln in text.splitlines() if not ln.startswith("# 连云港市志_")]
    text = "\n".join(lines)
    for pat in HEADER_PATTERNS:
        text = pat.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def step2_refine_middown(anchors):
    """精修中下册正文"""
    print("\n[步骤2] 精修中下册正文...")
    BODY_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for part_key, start, end, title in MID_DOWN_CHAPTERS:
        vol, prt = part_key.split("/")
        offset = 0
        for v, p, off, tot in PARTS:
            if v == vol and p == prt:
                offset = off
                break
        ocr_dir = OCR_BASE / vol / prt
        pages = []
        for gp in range(start, end + 1):
            ebook = gp - offset
            txt_path = ocr_dir / f"page_{ebook:04d}.txt"
            anchor = anchors.get(gp, "")
            if not txt_path.exists():
                pages.append({"page": gp, "anchor": anchor, "text": "", "missing": True, "table": False})
                continue
            raw = txt_path.read_text(encoding="utf-8")
            text = clean_text(raw)
            table = bool(TABLE_PATTERN.search(text))
            pages.append({"page": gp, "anchor": anchor, "text": text, "missing": False, "table": table})

        # 生成MD
        md_lines = [f"# {title}", "",
                    "<!-- 精修说明：基于OCR初稿，已清理页眉页脚和元信息。 -->", ""]
        for pg in pages:
            if pg["missing"]:
                md_lines += [f"<!-- page-anchor: {pg['anchor']} -->", f"[缺失页 p{pg['page']}]", ""]
                continue
            if not pg["text"].strip():
                continue
            md_lines += [f"<!-- page-anchor: {pg['anchor']} -->", ""]
            if pg["table"]:
                md_lines += [f"<!-- TABLE-PAGE: p{pg['page']} 表格页 -->", ""]
            md_lines += [pg["text"], ""]

        fname = re.sub(r'[\\/:*?"<>|\s]+', "_", title)
        (BODY_DIR / f"{fname}.md").write_text("\n".join(md_lines), encoding="utf-8")

        missing = sum(1 for pg in pages if pg["missing"])
        table_count = sum(1 for pg in pages if pg["table"])
        total_chars = sum(len(pg["text"]) for pg in pages if not pg["missing"])
        print(f"  [{title}] p{start}-p{end} ({len(pages)}页) 缺失{missing} 表格{table_count} 字符{total_chars}")
        results.append({"title": title, "pages": len(pages), "missing": missing,
                        "table": table_count, "chars": total_chars})

    print(f"  中下册精修完成: {sum(r['pages'] for r in results)}页, {sum(r['chars'] for r in results)}字符")
    return results


def step3_merge_full(anchors):
    """合并全书正文汇总"""
    print("\n[步骤3] 合并全书正文汇总...")
    # 上册文件在 body_chapters/上/ 子目录
    up_dir = BODY_DIR / "上"
    up_chapters = [
        "序与凡例.md", "总述与大事记.md", "第一卷_自然环境.md",
        "第二卷_建置区划.md", "第三卷_区县概况.md",
        "第四卷_人口（part01_部分）.md",
        "第四卷至第十卷（part02）.md", "第十卷至第十六卷（part03）.md",
    ]
    up_files = [up_dir / f for f in up_chapters if (up_dir / f).exists()]
    # 中下册文件在 body_chapters/ 根目录
    skip_names = set(up_chapters) | {"连云港市志_上册_正文汇总.md", "连云港市志_全书_正文汇总.md"}
    mid_down_files = [f for f in BODY_DIR.glob("*.md") if f.name not in skip_names]
    all_files = up_files + sorted(mid_down_files)

    merged = [f"# 连云港市志 全书正文汇总", "",
              "<!-- 由分章精修文件按顺序合并生成。 -->", ""]
    stats = []
    for fpath in all_files:
        text = fpath.read_text(encoding="utf-8")
        text = re.sub(r"<!-- 精修说明：.*?-->\n", "", text, flags=re.DOTALL)
        merged.append(text.rstrip())
        merged += ["", "---", ""]
        pages = len(re.findall(r"<!-- page-anchor:", text))
        tables = len(re.findall(r"<!-- TABLE-PAGE:", text))
        chars = len(re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip())
        stats.append({"file": fpath.name, "pages": pages, "tables": tables, "chars": chars})

    out = BODY_DIR / "连云港市志_全书_正文汇总.md"
    out.write_text("\n".join(merged), encoding="utf-8")
    print(f"  分章: {len(stats)}个  总页数: {sum(s['pages'] for s in stats)}  总字符: {sum(s['chars'] for s in stats)}")
    print(f"  输出: {out}")
    return stats, out


def step4_verify(merged_path):
    """全书校验"""
    print("\n[步骤4] 全书校验...")
    text = merged_path.read_text(encoding="utf-8")
    anchors = re.findall(r"<!-- page-anchor: (\S+) -->", text)
    table_pages = re.findall(r"<!-- TABLE-PAGE: p(\d+) ", text)
    debug_words = ["image_page", "book_page", "导出说明", "{{TABLE"]
    issues = sum(text.count(w) for w in debug_words)
    header_res = text.count("连云港市志·")

    rep = ["# 连云港市志 全书正文汇总校验报告", "",
           f"- 页锚总数：{len(anchors)}",
           f"- TABLE-PAGE 标记数：{len(table_pages)}",
           f"- 页眉残留：{header_res}",
           f"- 调试词残留：{issues}",
           f"- 总字符数：{len(text)}", "",
           "## 结论", ""]
    if issues == 0 and header_res == 0:
        rep.append("全书正文汇总通过校验，可进入阶段G。")
    else:
        rep.append(f"存在残留问题：页眉{header_res} 调试词{issues}，需清理。")

    out = QA_DIR / "全书正文汇总校验报告.md"
    out.write_text("\n".join(rep), encoding="utf-8")
    print(f"  页锚:{len(anchors)}  表格:{len(table_pages)}  页眉残留:{header_res}  调试词:{issues}")
    print(f"  输出: {out}")


def step5_reader_html(merged_path):
    """生成最终阅读版HTML"""
    print("\n[步骤5] 生成最终阅读版HTML...")
    md = merged_path.read_text(encoding="utf-8")
    # 移除内部标记
    text = re.sub(r"<!-- page-anchor: \S+ -->\n?", "", md)
    text = re.sub(r"<!-- TABLE-PAGE: p(\d+) [^>]*-->",
                  r'<div class="table-page">[表格页 p\1]</div>', text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    # Markdown→HTML
    lines = text.splitlines()
    html = []
    in_p = False
    for ln in lines:
        s = ln.strip()
        if not s:
            if in_p: html.append("</p>"); in_p = False
            continue
        if s.startswith("# "):
            if in_p: html.append("</p>"); in_p = False
            html.append(f"<h1>{s[2:]}</h1>")
        elif s.startswith("## "):
            if in_p: html.append("</p>"); in_p = False
            html.append(f"<h2>{s[3:]}</h2>")
        elif s.startswith("### "):
            if in_p: html.append("</p>"); in_p = False
            html.append(f"<h3>{s[4:]}</h3>")
        elif s == "---":
            if in_p: html.append("</p>"); in_p = False
            html.append("<hr>")
        elif s.startswith("<div"):
            if in_p: html.append("</p>"); in_p = False
            html.append(s)
        else:
            if not in_p: html.append("<p>"); in_p = True
            html.append(ln)
    if in_p: html.append("</p>")

    template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>连云港市志</title>
<style>
body{font-family:"Songti SC","SimSun","Noto Serif CJK SC",serif;max-width:800px;margin:2em auto;padding:0 1em;line-height:1.8;color:#333}
h1{font-size:1.8em;text-align:center;margin-top:2em;border-bottom:2px solid #ccc;padding-bottom:.3em}
h2{font-size:1.4em;margin-top:1.5em}
h3{font-size:1.2em;margin-top:1.2em}
p{text-indent:2em;margin:.5em 0}
.table-page{background:#f9f9f9;border-left:3px solid #999;padding:.5em 1em;margin:1em 0;color:#666;font-size:.9em}
hr{border:none;border-top:1px solid #ddd;margin:2em 0}
</style>
</head>
<body>
%s
</body>
</html>""" % "\n".join(html)

    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    out = FINAL_DIR / "连云港市志_最终阅读版.html"
    out.write_text(template, encoding="utf-8")
    size_mb = out.stat().st_size / 1024 / 1024
    print(f"  输出: {out}")
    print(f"  大小: {size_mb:.1f} MB")


def main():
    print("=" * 60)
    print("连云港市志 全书统一推进")
    print("=" * 60)

    anchors = step1_build_full_anchor_index()
    step2_refine_middown(anchors)
    stats, merged = step3_merge_full(anchors)
    step4_verify(merged)
    step5_reader_html(merged)

    print("\n" + "=" * 60)
    print("全书统一推进完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
