# -*- coding: utf-8 -*-
"""
连云港市志 全书正文重排版脚本

解决格式问题：
1. 段落内换行合并（OCR硬换行 → 连续文本）
2. 跨页段落回接（句末标点判断 + 下一页首行判断）
3. 按自然段落生成 HTML <p> 标签
4. 章节标题识别与层级化
"""

import re
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BODY_DIR = ROOT / "workbench" / "body_chapters"
FINAL_DIR = ROOT / "output" / "final_reader"
QA_DIR = ROOT / "workbench" / "qa"

# 章节标题模式
TITLE_PATTERNS = [
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+卷\s"),          # 第X卷
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+卷$"),          # 第X卷
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+章\s"),          # 第X章
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+节\s*"),         # 第X节
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+节$"),          # 第X节
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+篇\s"),          # 第X篇
    re.compile(r"^附\d+-\d+"),                                     # 附X-1
    re.compile(r"^(序|凡例|总述|大事记|总篇目|附录|跋|编纂始末)$"),  # 特殊标题
    re.compile(r"^第[一二三四五六七八九十百千零〇\d]+卷[\s\u4e00-\u9fff]"),  # 第X卷+标题
]

# 句末标点（表示句子/段落结束）
SENTENCE_END_CHARS = set("。！？；：」』）)\"'\"'}》")

# 大事记年份条目
YEAR_PATTERN = re.compile(r"^(春秋|秦|汉|三国|晋|南北朝|隋|唐|宋|元|明|清|民国|共和国|周)[^\n]{0,15}年[）)]")
AD_YEAR_PATTERN = re.compile(r"^\d{4}年")


def is_title(line):
    """判断是否为章节标题"""
    s = line.strip()
    if not s or len(s) > 30:
        return False
    for pat in TITLE_PATTERNS:
        if pat.match(s):
            return True
    return False


def is_paragraph_end(text):
    """判断文本末尾是否为段落结束"""
    text = text.rstrip()
    if not text:
        return True
    last = text[-1]
    return last in SENTENCE_END_CHARS


def is_year_entry(line):
    """判断是否为大事记年份条目"""
    s = line.strip()
    if len(s) > 30:
        return False
    return bool(YEAR_PATTERN.match(s) or AD_YEAR_PATTERN.match(s))


def is_list_item(line):
    """判断是否为列表项（一、二、三、或 1. 2. 等）"""
    s = line.strip()
    if len(s) > 40:
        return False
    return bool(re.match(r"^[一二三四五六七八九十]+、", s) or re.match(r"^\d+[.、]", s))


def merge_page_lines(text):
    """将页面内的OCR硬换行合并为自然段落。
    
    规则：
    - 连续的非空行属于同一段落，合并（去换行符）
    - 空行作为段落分隔
    - 标题行、年份条目、列表项独立成段
    """
    lines = text.splitlines()
    paragraphs = []
    current = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            # 空行 = 段落结束
            if current:
                paragraphs.append("".join(current))
                current = []
            continue
        
        # 标题独立成段
        if is_title(stripped):
            if current:
                paragraphs.append("".join(current))
                current = []
            paragraphs.append(stripped)
            continue
        
        # 年份条目独立成段
        if is_year_entry(stripped):
            if current:
                paragraphs.append("".join(current))
                current = []
            paragraphs.append(stripped)
            continue
        
        # 列表项独立成段
        if is_list_item(stripped):
            if current:
                paragraphs.append("".join(current))
                current = []
            current.append(stripped)
            continue
        
        # 普通行：合并到当前段落
        current.append(stripped)
    
    if current:
        paragraphs.append("".join(current))
    
    return paragraphs


def merge_cross_page(all_pages_paragraphs):
    """跨页段落回接。
    
    如果上一页最后一个段落未以句末标点结束，
    且下一页第一个段落不是标题/年份/列表项，
    则合并为一个段落。
    """
    merged = []
    
    for page_idx, paragraphs in enumerate(all_pages_paragraphs):
        if not paragraphs:
            continue
        
        if merged and paragraphs:
            last = merged[-1]
            first = paragraphs[0]
            
            # 判断是否应该回接
            should_join = (
                last  # 上一段非空
                and first  # 下一段非空
                and not is_title(last)  # 上一段不是标题
                and not is_title(first)  # 下一段不是标题
                and not is_year_entry(first)  # 下一段不是年份条目
                and not is_list_item(first)  # 下一段不是列表项
                and not is_paragraph_end(last)  # 上一段未结束
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
    """处理单个分章MD，返回重排后的段落列表"""
    # 提取所有页锚块
    page_blocks = re.split(r"<!-- page-anchor: \S+ -->", md_text)
    
    all_paragraphs = []
    for block in page_blocks[1:]:  # 跳过第一个（标题部分）
        # 去掉 TABLE-PAGE 标记和注释
        block = re.sub(r"<!-- TABLE-PAGE: [^>]*-->", "", block)
        block = re.sub(r"<!--.*?-->", "", block, flags=re.DOTALL)
        block = block.strip()
        if not block:
            continue
        paras = merge_page_lines(block)
        all_paragraphs.append(paras)
    
    # 跨页回接
    merged = merge_cross_page(all_paragraphs)
    return merged


def paragraphs_to_html(paragraphs, chapter_title):
    """将段落列表转为HTML"""
    html = [f'<h1>{chapter_title}</h1>', ""]
    
    for para in paragraphs:
        s = para.strip()
        if not s:
            continue
        
        if is_title(s):
            # 判断标题层级
            if re.match(r"^第[一二三四五六七八九十百千零〇\d]+卷", s):
                html.append(f"<h2>{s}</h2>")
            elif re.match(r"^第[一二三四五六七八九十百千零〇\d]+章", s):
                html.append(f"<h3>{s}</h3>")
            elif re.match(r"^第[一二三四五六七八九十百千零〇\d]+节", s):
                html.append(f"<h4>{s}</h4>")
            elif s in ("序", "凡例", "总述", "大事记", "总篇目", "附录", "跋", "编纂始末"):
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
    print("=== 全书正文重排版 ===")
    
    # 收集所有分章文件
    up_dir = BODY_DIR / "上"
    up_chapters = [
        "序与凡例.md", "总述与大事记.md", "第一卷_自然环境.md",
        "第二卷_建置区划.md", "第三卷_区县概况.md",
        "第四卷_人口（part01_部分）.md",
        "第四卷至第十卷（part02）.md", "第十卷至第十六卷（part03）.md",
    ]
    up_files = [up_dir / f for f in up_chapters if (up_dir / f).exists()]
    skip = set(up_chapters) | {"连云港市志_上册_正文汇总.md", "连云港市志_全书_正文汇总.md"}
    mid_down = sorted(f for f in BODY_DIR.glob("*.md") if f.name not in skip)
    all_files = up_files + mid_down
    
    print(f"分章文件: {len(all_files)}")
    
    all_html_parts = [
        '<!DOCTYPE html>',
        '<html lang="zh-CN">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">',
        '<title>连云港市志</title>',
        '<style>',
        'body{font-family:"Songti SC","SimSun","Noto Serif CJK SC",serif;max-width:800px;margin:2em auto;padding:0 1em;line-height:1.8;color:#333}',
        'h1{font-size:1.8em;text-align:center;margin-top:2em;border-bottom:2px solid #ccc;padding-bottom:.3em}',
        'h2{font-size:1.5em;margin-top:1.8em;color:#1a1a1a}',
        'h3{font-size:1.3em;margin-top:1.5em;color:#333}',
        'h4{font-size:1.1em;margin-top:1.2em;color:#444}',
        'p{text-indent:2em;margin:.3em 0}',
        '.year-entry{text-indent:2em;margin:.4em 0;text-align:justify}',
        '.list-item{text-indent:2em;margin:.4em 0;text-align:justify}',
        '.table-page{background:#f9f9f9;border-left:3px solid #999;padding:.5em 1em;margin:1em 0;color:#666;font-size:.9em;text-indent:0}',
        'hr{border:none;border-top:1px solid #ddd;margin:2em 0}',
        '</style>',
        '</head>',
        '<body>',
        '<h1>连云港市志</h1>',
    ]
    
    total_paras = 0
    for fpath in all_files:
        title = fpath.stem
        # 提取更友好的标题
        if "序与凡例" in title:
            chapter_title = "序 · 凡例"
        elif "总述与大事记" in title:
            chapter_title = "总述 · 大事记"
        else:
            chapter_title = title.replace("_", " ")
        
        md = fpath.read_text(encoding="utf-8")
        paragraphs = process_chapter(md)
        html = paragraphs_to_html(paragraphs, chapter_title)
        all_html_parts.append(html)
        all_html_parts.append("<hr>")
        total_paras += len(paragraphs)
        print(f"  [{chapter_title}] {len(paragraphs)} 段落")
    
    all_html_parts.append('</body>')
    all_html_parts.append('</html>')
    
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    out = FINAL_DIR / "连云港市志_最终阅读版.html"
    out.write_text("\n".join(all_html_parts), encoding="utf-8")
    
    size_mb = out.stat().st_size / 1024 / 1024
    print(f"\n=== 重排版完成 ===")
    print(f"总段落: {total_paras}")
    print(f"输出: {out}")
    print(f"大小: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
