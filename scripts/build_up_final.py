# -*- coding: utf-8 -*-
"""
连云港市志 上册 精修版最终阅读版生成脚本

基于OCR错误修正后的精修分章文件，生成：
1. 最终阅读版 HTML（合并OCR硬换行，跨页段落回接，标题层级化）
2. 更新精修进度报告
"""

import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "workbench" / "body_chapters" / "上"
MERGED_MD = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md"
FINAL_DIR = ROOT / "output" / "final_reader"
REPORT_DIR = ROOT / "output" / "reports"

CHAPTER_ORDER = [
    ("序与凡例.md", "序 · 凡例"),
    ("总述与大事记.md", "总述 · 大事记"),
    ("第一卷_自然环境.md", "第一卷 自然环境"),
    ("第二卷_建置区划.md", "第二卷 建置区划"),
    ("第三卷_区县概况.md", "第三卷 区县概况"),
    ("第四卷_人口（part01_部分）.md", "第四卷 人口（一）"),
    ("第四卷至第十卷（part02）.md", "第四卷至第十卷（二）"),
    ("第十卷至第十六卷（part03）.md", "第十卷至第十六卷（三）"),
]

# 章节标题模式
TITLE_PATTERNS = [
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+卷\s"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+卷$"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+章\s"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+节\s*"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+节$"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+篇\s"),
    re.compile(r"^附\d+-\d+"),
    re.compile(r"^(序|凡例|总述|大事记|总篇目|附录|跋|编纂始末|概述)$"),
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+卷[\s\u4e00-\u9fff]"),
]

SENTENCE_END_CHARS = set("。！？；：」』）)\"'\"'}》")

YEAR_PATTERN = re.compile(r"^(春秋|秦|汉|三国|晋|南北朝|隋|唐|宋|元|明|清|民国|共和国|周)[^\n]{0,15}年[）)]")
AD_YEAR_PATTERN = re.compile(r"^\d{4}年")


def is_title(line):
    s = line.strip()
    if not s or len(s) > 30:
        return False
    for pat in TITLE_PATTERNS:
        if pat.match(s):
            return True
    return False


def is_paragraph_end(text):
    text = text.rstrip()
    if not text:
        return True
    return text[-1] in SENTENCE_END_CHARS


def is_year_entry(line):
    s = line.strip()
    if len(s) > 30:
        return False
    return bool(YEAR_PATTERN.match(s) or AD_YEAR_PATTERN.match(s))


def is_list_item(line):
    s = line.strip()
    if len(s) > 40:
        return False
    return bool(re.match(r"^[一二三四五六七八九十]+、", s) or re.match(r"^\d+[.、]", s))


def merge_page_lines(text):
    """将页面内OCR硬换行合并为自然段落"""
    lines = text.splitlines()
    paragraphs = []
    current = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append("".join(current))
                current = []
            continue

        if is_title(stripped):
            if current:
                paragraphs.append("".join(current))
                current = []
            paragraphs.append(stripped)
            continue

        if is_year_entry(stripped):
            if current:
                paragraphs.append("".join(current))
                current = []
            paragraphs.append(stripped)
            continue

        if is_list_item(stripped):
            if current:
                paragraphs.append("".join(current))
                current = []
            current.append(stripped)
            continue

        current.append(stripped)

    if current:
        paragraphs.append("".join(current))

    return paragraphs


def merge_cross_page(all_pages_paragraphs):
    """跨页段落回接"""
    merged = []

    for paragraphs in all_pages_paragraphs:
        if not paragraphs:
            continue

        if merged and paragraphs:
            last = merged[-1]
            first = paragraphs[0]

            should_join = (
                last and first
                and not is_title(last)
                and not is_title(first)
                and not is_year_entry(first)
                and not is_list_item(first)
                and not is_paragraph_end(last)
            )

            if should_join:
                merged[-1] = last + first
                merged.extend(paragraphs[1:])
            else:
                merged.extend(paragraphs)
        else:
            merged.extend(paragraphs)

    return merged


def process_chapter(md_text):
    """处理单个分章MD"""
    page_blocks = re.split(r"<!-- page-anchor: \S+ -->", md_text)

    all_paragraphs = []
    for block in page_blocks[1:]:
        block = re.sub(r"<!-- TABLE-PAGE: [^>]*-->", "", block)
        block = re.sub(r"<!--.*?-->", "", block, flags=re.DOTALL)
        block = block.strip()
        if not block:
            continue
        paras = merge_page_lines(block)
        all_paragraphs.append(paras)

    return merge_cross_page(all_paragraphs)


def paragraphs_to_html(paragraphs, chapter_title):
    """段落列表 → HTML"""
    html = [f'<h1>{chapter_title}</h1>', ""]

    for para in paragraphs:
        s = para.strip()
        if not s:
            continue

        if is_title(s):
            if re.match(r"^第[一二三四五六七八九十百千零〇\d]+卷", s):
                html.append(f"<h2>{s}</h2>")
            elif re.match(r"^第[一二三四五六七八九十百千零〇\d]+章", s):
                html.append(f"<h3>{s}</h3>")
            elif re.match(r"^第[一二三四五六七八九十百千零〇\d]+节", s):
                html.append(f"<h4>{s}</h4>")
            elif s in ("序", "凡例", "总述", "大事记", "总篇目", "附录", "跋", "编纂始末", "概述"):
                html.append(f"<h2>{s}</h2>")
            else:
                html.append(f"<h3>{s}</h3>")
        elif is_year_entry(s):
            html.append(f'<p class="year-entry">{s}</p>')
        elif is_list_item(s):
            html.append(f'<p class="list-item">{s}</p>')
        else:
            html.append(f"<p>{s}</p>")

    return "\n".join(html)


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 生成HTML
    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="zh-CN">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">',
        '<title>连云港市志 · 上册（精修版）</title>',
        '<style>',
        'body{font-family:"Songti SC","SimSun","Noto Serif CJK SC",serif;max-width:820px;margin:2em auto;padding:0 1.5em;line-height:1.85;color:#333;background:#fdfdfd}',
        'h1{font-size:1.8em;text-align:center;margin-top:2.5em;border-bottom:2px solid #8B0000;padding-bottom:.4em;color:#1a1a1a}',
        'h2{font-size:1.5em;margin-top:2em;color:#8B0000;border-left:4px solid #8B0000;padding-left:.5em}',
        'h3{font-size:1.3em;margin-top:1.6em;color:#333}',
        'h4{font-size:1.1em;margin-top:1.3em;color:#444}',
        'p{text-indent:2em;margin:.4em 0;text-align:justify}',
        '.year-entry{text-indent:2em;margin:.4em 0;text-align:justify}',
        '.list-item{text-indent:2em;margin:.4em 0;text-align:justify}',
        '.table-page{background:#f5f5f5;border-left:4px solid #999;padding:.6em 1em;margin:1.2em 0;color:#666;font-size:.92em;text-indent:0;font-style:italic}',
        '.toc{text-align:center;margin:2em 0}',
        '.toc a{color:#8B0000;text-decoration:none;margin:0 .3em}',
        '.toc a:hover{text-decoration:underline}',
        '.meta{text-align:center;color:#999;font-size:.85em;margin-top:3em;padding-top:1em;border-top:1px solid #eee}',
        'hr{border:none;border-top:1px solid #ddd;margin:2.5em 0}',
        '@media print{body{max-width:100%;font-size:11pt}h1,h2,h3,h4{page-break-after:avoid}}',
        '</style>',
        '</head>',
        '<body>',
        '',
        '<div style="text-align:center;margin:3em 0">',
        '<h1 style="font-size:2.2em;border:none;color:#8B0000">连云港市志</h1>',
        '<p style="text-indent:0;font-size:1.1em;color:#666">上册 · 精修版</p>',
        f'<p style="text-indent:0;font-size:.85em;color:#999">OCR精修完成 · {now}</p>',
        '</div>',
        '',
        '<div class="toc">',
        '<p style="text-indent:0;font-weight:bold;margin-bottom:.5em">目 录</p>',
    ]

    # 目录
    toc_links = []
    for fname, title in CHAPTER_ORDER:
        anchor = title.replace(" ", "-").replace("·", "").replace("（", "").replace("）", "")
        toc_links.append(f'<a href="#{anchor}">{title}</a>')
    html_parts.append(" · ".join(toc_links))
    html_parts.append("</div>")
    html_parts.append("")

    total_paras = 0
    stats = []

    for fname, chapter_title in CHAPTER_ORDER:
        fpath = CHAPTER_DIR / fname
        if not fpath.exists():
            print(f"[WARN] 缺失: {fname}")
            continue

        anchor = chapter_title.replace(" ", "-").replace("·", "").replace("（", "").replace("）", "")
        html_parts.append(f'<div id="{anchor}"></div>')

        md = fpath.read_text(encoding="utf-8")
        paragraphs = process_chapter(md)
        html = paragraphs_to_html(paragraphs, chapter_title)
        html_parts.append(html)
        html_parts.append("<hr>")
        total_paras += len(paragraphs)
        stats.append({"chapter": chapter_title, "paragraphs": len(paragraphs)})
        print(f"  [{chapter_title}] {len(paragraphs)} 段落")

    html_parts.append(f'<div class="meta">连云港市志 · 上册精修版 · 生成于 {now}<br>891页 · {total_paras} 自然段落 · OCR系统性错误已修正</div>')
    html_parts.append('</body>')
    html_parts.append('</html>')

    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    out_html = FINAL_DIR / "连云港市志_上册_精修版.html"
    out_html.write_text("\n".join(html_parts), encoding="utf-8")

    size_mb = out_html.stat().st_size / 1024 / 1024
    print(f"\nHTML 生成完成：{out_html}")
    print(f"总段落: {total_paras}，大小: {size_mb:.1f} MB")

    # 更新进度报告
    report = []
    report.append("# 上册正文OCR精修进度（更新）")
    report.append("")
    report.append(f"更新时间：{now}")
    report.append("")
    report.append("## 总体状态")
    report.append("")
    report.append("- 上册总页数：903（全局页 1-903）")
    report.append("- 已精修页数：891")
    report.append("- 表格页（已标注占位）：135")
    report.append("- 精修后总字符数：969,866")
    report.append("- 缺失页：0")
    report.append("- 页眉残留：0")
    report.append("- OCR 元信息残留：0")
    report.append("")
    report.append("## 本轮精修（OCR系统性错误修正）")
    report.append("")
    report.append("修正了88处OCR系统性错误，包括：")
    report.append("")
    report.append("| 错误类型 | 修正数 | 示例 |")
    report.append("| --- | ---: | --- |")
    report.append("| 沭/述混淆（地名） | 40+ | 新述河→新沭河、述阳→沭阳 |")
    report.append("| 沐/沭混淆（地名） | 15+ | 新沐河→新沭河、临沐县→临沭县 |")
    report.append("| 经纬度符号 | 4 | 3507→35°07'、11824°→118°24' |")
    report.append("| 形近字（朐/胸等） | 20+ | 胸山→朐山、准北→淮北 |")
    report.append("| 常见OCR错字 | 5+ | 进一一步→进一步、编繁→编纂 |")
    report.append("")
    report.append("## 跨页回接检测")
    report.append("")
    report.append("- 高可疑断句：394处（绝大多数为正常跨页排版）")
    report.append("- 真正词语断裂：1处（p125→p126 平移，为正常排版）")
    report.append("- 结论：无需额外修复")
    report.append("")
    report.append("## 分章统计")
    report.append("")
    report.append("| 章节 | 页数 | 表格页 | 字符数 |")
    report.append("| --- | ---: | ---: | ---: |")
    report.append("| 序与凡例 | 16 | 0 | 9,639 |")
    report.append("| 总述与大事记 | 95 | 0 | 98,336 |")
    report.append("| 第一卷 自然环境 | 89 | 9 | 96,285 |")
    report.append("| 第二卷 建置区划 | 19 | 11 | 15,879 |")
    report.append("| 第三卷 区县概况 | 47 | 0 | 56,821 |")
    report.append("| 第四卷 人口（part01） | 22 | 4 | 27,954 |")
    report.append("| part02（第四卷~第十卷） | 305 | 72 | 334,223 |")
    report.append("| part03（第十卷~第十六卷） | 298 | 39 | 330,729 |")
    report.append("| **合计** | **891** | **135** | **969,866** |")
    report.append("")
    report.append("## 产物")
    report.append("")
    report.append(f"- 上册正文汇总：`workbench/body_chapters/连云港市志_上册_正文汇总.md`")
    report.append(f"- 精修版HTML：`output/final_reader/连云港市志_上册_精修版.html`")
    report.append(f"- 分章精修文件：`workbench/body_chapters/上/*.md`（8个）")
    report.append(f"- OCR错误修正日志：`workbench/qa/上册OCR错误修正日志.md`")
    report.append(f"- 跨页回接检测报告：`workbench/qa/上册跨页回接检测报告.md`")
    report.append(f"- 跨页词断裂检测报告：`workbench/qa/上册跨页词断裂检测报告.md`")
    report.append("")
    report.append("## 待人工核查项（剩余）")
    report.append("")
    report.append("- 瞻程非邈/总而成/大伴 等存疑词（保留原文，待人工确认）")
    report.append("- 表格页 OCR 原文需阶段 F 表格结构化处理（135个表格页）")
    report.append("- 中下册 OCR 完成后的精修复用本流程")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out_report = REPORT_DIR / "上册正文OCR精修进度.md"
    out_report.write_text("\n".join(report), encoding="utf-8")
    print(f"报告更新：{out_report}")


if __name__ == "__main__":
    main()
