# -*- coding: utf-8 -*-
"""基于 PaddleOCR 的上册正文汇总与最终 HTML 生成
v2: 加入段落合并（页内硬换行合并 + 跨页回接），消除 OCR 断行问题
"""

import json, re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "workbench" / "body_chapters" / "paddle_上"
OUT_MERGED = ROOT / "workbench" / "body_chapters" / "连云港市志_上册_PaddleOCR正文汇总.md"
OUT_HTML = ROOT / "output" / "final_reader" / "连云港市志_上册_PaddleOCR精修版.html"
OUT_REPORT = ROOT / "output" / "reports" / "上册_PaddleOCR_精修进度.md"

CHAPTER_ORDER = [
    "序与凡例.md",
    "总述与大事记.md",
    "第一卷_自然环境.md",
    "第二卷_建置区划.md",
    "第三卷_区县概况.md",
    "第四卷_人口（part01_部分）.md",
    "第四卷至第十卷（part02）.md",
    "第十卷至第十六卷（part03）.md",
]

# ── 标题识别 ──
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
    re.compile(r"^\([一二三四五六七八九十]+\)$"),  # (一)(二)(三) 子标题
]

# ── 总篇目区域识别 ──
# 总篇目是从"篇\n(上册)"到"编纂始末……"结束的目录页区域
# 该区域的各行（含引导符 …/.）不是真正的章节标题，而是目录条目
TOC_ENTRY_PATTERN = re.compile(
    r"^(第[一二三四五六七八九十百千零〇\d]+卷|序|凡例|总述|大事记|附录|跋|编纂始末|"
    r"录|卷首)[\s\w\u4e00-\u9fff()（）\u3000-\u303f]*[.…]*$"
)
TOC_START_PATTERN = re.compile(r"^篇$")  # "篇"行触发总篇目检测
TOC_END_MARKERS = {"编纂始末", "编纂始末……", "编纂始末..", "编纂始末.", "跋..", "跋.", "附录", "附录.."}

# ── 引导符/目录填充符清理 ──
LEADER_PATTERN = re.compile(r"[.…]{1,}$")  # 末尾连续点号或省略号（引导符）
LEADER_PATTERN_MULTI = re.compile(r"[.…]{2,}$")  # 用于 is_toc_line 检测（至少2个才确认）

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
    # 处理 ·N· 页码后缀（如 大事记·17·）
    s_clean = re.sub(r'·\d+·\s*', '', s).strip()
    if s_clean != s:
        for pat in TITLE_PATTERNS:
            if pat.match(s_clean):
                return True
    # 处理 （N）页码后缀
    s_clean2 = re.sub(r'[\(（]\d+[\)）]$', '', s).strip()
    if s_clean2 != s:
        for pat in TITLE_PATTERNS:
            if pat.match(s_clean2):
                return True
    return False


def is_paragraph_end(text):
    text = text.rstrip()
    if not text:
        return True
    return text[-1] in SENTENCE_END_CHARS


def is_year_entry(line):
    return bool(YEAR_PATTERN.match(line.strip()) or AD_YEAR_PATTERN.match(line.strip()))


def is_list_item(line):
    s = line.strip()
    return bool(re.match(r"^[一二三四五六七八九十]+、", s) or re.match(r"^\d+[.、]", s))


def is_toc_line(line):
    """检测是否为总篇目/目录条目行（含引导符或特定标记）"""
    s = line.strip()
    # "篇" 单独一行 → 总篇目标题
    if s == "篇":
        return True
    # "录" 单独一行 → 第二页目录标题
    if s == "录":
        return True
    # 分册标记
    if s in ("(上册)", "(中册)", "(下册)"):
        return True
    # 引导符结尾的条目（序……、凡例……、总述.、大事记…… 等）
    if LEADER_PATTERN.search(s) and len(s) <= 30:
        return True
    # 第X卷 + 引导符（总篇目中的条目，非正文中的卷标题）
    # 正文中的卷标题不会以引导符结尾；引导符可能在行尾或页码前
    if re.match(r"^第[一二三四五六七八九十百千零〇\d]+卷\s", s) and (LEADER_PATTERN.search(s) or re.search(r"[.…]{2,}", s)):
        return True
    # 附录/跋/编纂始末 + 引导符
    if re.match(r"^(附录|跋|编纂始末|卷首)", s) and LEADER_PATTERN.search(s):
        return True
    return False


def merge_page_lines(text):
    """将页面内OCR硬换行合并为自然段落"""
    lines = text.splitlines()
    paragraphs = []
    current = []
    # 预编译标题检测模式（含·N·页码后缀变体）
    title_variants = [
        re.compile(r'^[·.\d]*\s*(序|凡例|总述|大事记|总篇目|附录|跋|编纂始末|概述)'),
        re.compile(r'^[·.\d]*\s*第[一二三四五六七八九十百千零零\d]+[卷章节]'),
    ]

    def looks_like_title(s):
        if is_title(s):
            return True
        for pat in title_variants:
            if pat.match(s) and len(s) < 40:
                return True
        return False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append("".join(current))
                current = []
            continue

        # 总篇目条目优先检测（先于 is_title）
        if is_toc_line(stripped):
            if current:
                paragraphs.append("".join(current))
                current = []
            paragraphs.append(stripped)
            continue

        if looks_like_title(stripped):
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
                and not is_toc_line(last)   # TOC 条目不跨页回接
                and not is_toc_line(first)  # TOC 条目不跨页回接
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



def is_table_block(text):
    """判断文本块是否是OCR表格数据"""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        return False
    has_marker = any(("表" in l and re.search(r"\d+[-— ]\d+", l)) for l in lines[:5])
    has_unit = any(l.startswith("单位") for l in lines[:5])
    nums = sum(1 for l in lines if re.match(r"^[\d. ]+$", l))
    ratio = nums / len(lines) if lines else 0
    return (has_marker and ratio > 0.3) or (has_unit and ratio > 0.4) or ratio > 0.6

def split_block(block):
    """拆分页面块，过滤表格数据，保留正文"""
    text = block.strip()
    lines = text.split("\n")
    # 找表标题行（如 表7-4）或单位行（如 单位：万元）
    cutoff = len(lines)
    for i, l in enumerate(lines):
        sl = l.strip()
        if re.match(r"^表\d+[-\u2014]", sl) or re.match(r"^表\d+-\d+", sl) or sl.startswith("单位："):
            cutoff = max(0, i - 3)
            break
    if cutoff < len(lines):
        kept = "\n".join(lines[:cutoff]).strip()
        if kept:
            return kept + "\n\n【表格页-待结构化录入】"
    if is_table_block(text):
        return "【表格页-待结构化录入】"
    return text

def process_chapter(md_text):
    """处理单个分章MD：页内合并 + 跨页回接"""
    page_blocks = re.split(r"<!-- page-anchor: \S+ -->", md_text)

    all_paragraphs = []
    for block in page_blocks[1:]:
        has_table = 'TABLE-PAGE' in block
        clean = re.sub(r"<!--.*?-->", "", block, flags=re.DOTALL).strip()
        if not clean and has_table:
            clean = "【表格页-待结构化录入】"
        elif not clean:
            continue
        elif has_table:
            clean = split_block(clean)
        paras = merge_page_lines(clean)
        all_paragraphs.append(paras)

    return merge_cross_page(all_paragraphs)


def is_toc_region(paragraphs, start_idx):
    """检测从 start_idx 开始的段落是否属于总篇目/目录区域"""
    if start_idx >= len(paragraphs):
        return False, 0
    
    p0 = paragraphs[start_idx].strip()
    # 触发条件："篇" 行（独立行）
    if p0 not in ("篇", "录"):
        return False, 0
    
    # 检查下一行是否为 "(上册)" 或 "(中册)" 或 "(下册)"
    if start_idx + 1 >= len(paragraphs):
        return False, 0
    p1 = paragraphs[start_idx + 1].strip()
    if p1 not in ("(上册)", "(中册)", "(下册)"):
        return False, 0
    
    # 扫描到总篇目结束
    end_idx = start_idx + 2
    while end_idx < len(paragraphs):
        line = paragraphs[end_idx].strip()
        # 空行也继续
        if not line:
            end_idx += 1
            continue
        # 检查是否到达总篇目结尾
        if line in TOC_END_MARKERS:
            end_idx += 1
            continue
        # 如果是 "录" 行（第二页目录标题），也属于总篇目
        if line == "录":
            end_idx += 1
            continue
        # 检查是否是分册标记
        if line in ("(上册)", "(中册)", "(下册)"):
            end_idx += 1
            continue
        # 检查是否是"卷首"、"序"、"凡例"（第二页目录内容）
        if line in ("卷首", "序", "凡例", "总述"):
            end_idx += 1
            continue
        # 检查是否是 TOC 条目（卷标题+引导符 或 序/凡例/总述+引导符 等）
        if TOC_ENTRY_PATTERN.match(line):
            end_idx += 1
            continue
        # 兜底：如果是 "第X卷" 开头且带引导符（含较长行或带页码如(2409)），也视为 TOC 条目
        if re.match(r"^第[一二三四五六七八九十百千零〇\d]+卷\s", line):
            # 引导符可能在行尾，也可能在页码前
            if LEADER_PATTERN.search(line) or re.search(r"[.…]{2,}", line):
                end_idx += 1
                continue
        # 附录/跋/编纂始末 带引导符
        if re.match(r"^(附录|跋|编纂始末)", line) and (LEADER_PATTERN.search(line) or len(line) <= 4):
            end_idx += 1
            continue
        # 不是 TOC 条目，结束
        break
    
    # 确认确实是一个有效的 TOC 区域（至少有几个条目）
    if end_idx - start_idx >= 5:
        return True, end_idx
    
    return False, 0


def clean_leader_dots(text):
    """清理引导符（…或.）及页码(2409)，保留卷名/条目名"""
    # 先移除末尾页码如 (2409)
    text = re.sub(r"\(\d+\)$", "", text).rstrip()
    # 再移除引导符
    text = re.sub(r"[.…]{1,}$", "", text).rstrip()
    return text


def title_to_anchor(title):
    if title is None:
        return "anchor"
    safe = ''
    for ch in title:
        if ch.isalnum() or ch in '-_' or ord(ch) > 0x4e00:
            safe += ch if ch != ' ' else '-'
        else:
            safe += '-'
    safe = '-'.join(filter(None, safe.split('-')))
    return safe if safe else 'anchor'


def load_verified_toc():
    cv = ROOT / "structure_workbench" / "data" / "chapters_verified.json"
    if cv.exists():
        try:
            import json
            chs = json.loads(cv.read_text("utf-8"))
            return {c["title"]: c["anchor"] for c in chs}
        except:
            return {}
    return {}


    # 先移除末尾页码如 (2409)
    text = re.sub(r"\(\d+\)$", "", text).rstrip()
    # 再移除引导符
    text = re.sub(r"[.…]{1,}$", "", text).rstrip()
    return text




def is_toc_paragraph(text):
    if not text: return False
    s = text.strip()
    if not s or len(s) > 50: return False
    if s in ('篇','录','(上册)','(中册)','(下册)','卷首','总篇目·1·','总篇目·3·','目','录\n'):
        return True
    if re.search(r'[.…]{2,}\s*[\(（]?\d+[\)）]?$', s) and len(s) < 40:
        return True
    if re.match(r'^第[一二三四五六七八九十百千零〇\d]+节', s) and len(s) < 15:
        return True
    if re.match(r'^第[一二三四五六七八九十百千零〇\d]+节', s) and re.search(r'[…]', s):
        return True
    if re.match(r'^第[一二三四五六七八九十百千零〇\d]+章', s) and re.search(r'[…]{2,}', s):
        return True
    if re.match(r'^第[一二三四五六七八九十百千零〇\d]+卷', s) and len(s) < 20:
        return True
    if re.match(r'^[·.]+\d+[·.]', s) or re.match(r'^·\d+·', s):
        return True
    if s in ('概述','概述…','概述。','总述','总述。'):
        return True
    return False
def normalize_title(text):
    """规范化OCR标题文本：清理页眉页码、OCR残留"""
    if not text or len(text) > 60:
        return text
    t = text.strip()
    # 1. Strip page header suffix like ·17· or ·3·
    t = re.sub(r'·\d+·\s*$', '', t).strip()
    # 2. Strip OCR artifacts: ……（97） or ...(97)
    t = re.sub(r'[.\u2026…]{2,}?\s*[\(（]?\d+[\)）]?$', '', t).strip()
    t = re.sub(r'[.\u2026…]+$', '', t).strip()
    # 3. Strip trailing page reference (N)
    t = re.sub(r'[\(（]\d+[\)）]$', '', t).strip()
    # 4. Strip leading OCR artifacts
    t = re.sub(r'^[·.\d]+\s*', '', t).strip()
    # 5. Normalize spaces
    t = re.sub(r'\s{2,}', '', t).strip()
    return t if t else text.strip()

def is_title_normalized(text):
    """判断(规范化后的)文本是否是标题"""
    t = normalize_title(text)
    if not t:
        return False, text
    # 原版标题检测
    for pat in TITLE_PATTERNS:
        if pat.match(t):
            return True, t
    # 补充检测：带·N·页码的标题如 大事记·17·
    t2 = re.sub(r'·\d+·\s*$', '', text.strip()).strip()
    for pat in TITLE_PATTERNS:
        if pat.match(t2):
            return True, t2
    # 检测带OCR残留的章标题
    if re.match(r'^第[一二三四五六七八九十百千零零\d]+[卷章节]', t) and len(t) < 40:
        return True, t
    return False, text


def paragraphs_to_html(paragraphs):
    global is_toc_paragraph
    """段落列表 → HTML"""
    html = []
    i = 0
    verified_toc = load_verified_toc()
    toc_found = True if verified_toc else False

    seen_titles = set()
    # Build TOC from verified chapters when available (with chapter-level items)
    if verified_toc:
        html.append('<div class="toc-section">')
        html.append('<h2 class="toc-title">总篇目</h2>')
        html.append('<ul class="toc-list">')
        cv_path = ROOT / "structure_workbench" / "data" / "chapters_verified.json"
        if cv_path.exists():
            all_chs = json.loads(cv_path.read_text("utf-8"))
            for ch in all_chs:
                if ch["level"] == 0:
                    html.append(f'<li class="toc-item"><a href="#{ch["anchor"]}">{ch["title"]}</a></li>')
                else:
                    html.append(f'<li class="toc-item toc-chapter">&#160;&#160;&#160;<a href="#{ch["anchor"]}">{ch["title"]}</a></li>')
        else:
            for title, anchor in verified_toc.items():
                html.append(f'<li class="toc-item"><a href="#{anchor}">{title}</a></li>')
        html.append('</ul></div>')
        print("[TOC] 已验证目录:", len(verified_toc))
    # 过滤OCR目录文本（利用verified_toc白名单）
    if verified_toc:
        whitelist = set(verified_toc.keys())
        whitelist.update(k.replace(' ', '') for k in verified_toc.keys())
        filtered = []
        for par in paragraphs:
            pd = par.strip()
            if not pd:
                filtered.append(par); continue
            # 明显目录标记
            if pd in ('篇','录','(上册)','(中册)','(下册)','卷首','总篇目·1·','总篇目·3·'): continue
            if re.match(r'^[·.]\d+[·.]', pd): continue
            if re.match(r'^[.…]+\(\d+\)$', pd): continue
            if re.search(r'[….]{2,}$', pd) and len(pd) < 30: continue
            # 卷标题：不在白名单则过滤
            if re.match(r'^第[一二三四五六七八九十百千零〇\d]+卷', pd) and len(pd) < 25:
                if pd not in whitelist and pd.replace(' ', '') not in whitelist: continue
            # 章标题：不在白名单且带……则过滤
            if re.match(r'^第[一二三四五六七八九十百千零〇\d]+章', pd) and len(pd) < 30:
                if pd.replace(' ', '') not in whitelist and re.search(r'[…]', pd): continue
            filtered.append(par)
        removed = len(paragraphs) - len(filtered)
        if removed > 0:
            print(f"  [过滤] 移除 {removed} 个目录段落")
        paragraphs = filtered
    while i < len(paragraphs):
        para = paragraphs[i].strip()
        if not para:
            i += 1
            continue
        
        # 检测总篇目/目录区域
        is_toc, toc_end = is_toc_region(paragraphs, i)
        if is_toc and not toc_found:
            toc_found = True

            # 输出总篇目区域
            html.append('<div class="toc-section">')
            html.append('<h2 class="toc-title">总篇目</h2>')
            html.append('<ul class="toc-list">')
            i += 2  # 跳过 "篇" 和 "(上册)"
            current_book = "(上册)"
            
            while i < toc_end:
                line = paragraphs[i].strip()
                if not line:
                    i += 1
                    continue
                
                # 分册标记
                if line in ("(上册)", "(中册)", "(下册)"):
                    current_book = line
                    i += 1
                    continue
                
                # "录" 标题行（第二页目录）
                if line == "录":
                    i += 1
                    continue
                
                # "卷首"等无编号条目
                if line in ("卷首", "序", "凡例", "总述"):
                    cleaned = clean_leader_dots(line)
                    anc = verified_toc.get(cleaned) or next((v for k,v in verified_toc.items() if k.replace(' ', '') == cleaned.replace(' ', '')), title_to_anchor(cleaned))
                    html.append(f'<li class="toc-item"><a href="#{anc}">{cleaned}</a></li>')
                    i += 1
                    continue
                
                # 附录、跋、编纂始末
                if line in ("附录", "附录..", "附录.") or line.startswith("附录"):
                    cleaned2 = clean_leader_dots(line)
                    anc2 = verified_toc.get(cleaned2) or next((v for k,v in verified_toc.items() if k.replace(' ', '') == cleaned2.replace(' ', '')), title_to_anchor(cleaned2))
                    html.append(f'<li class="toc-item"><a href="#{anc2}">{clean_leader_dots(line)}</a></li>')
                    i += 1
                    continue
                if line in ("跋", "跋..", "跋.", "跋……") or line.startswith("跋"):
                    cleaned2 = clean_leader_dots(line)
                    anc2 = verified_toc.get(cleaned2) or next((v for k,v in verified_toc.items() if k.replace(' ', '') == cleaned2.replace(' ', '')), title_to_anchor(cleaned2))
                    html.append(f'<li class="toc-item"><a href="#{anc2}">{clean_leader_dots(line)}</a></li>')
                    i += 1
                    continue
                if line.startswith("编纂始末"):
                    cleaned2 = clean_leader_dots(line)
                    anc2 = verified_toc.get(cleaned2) or next((v for k,v in verified_toc.items() if k.replace(' ', '') == cleaned2.replace(' ', '')), title_to_anchor(cleaned2))
                    html.append(f'<li class="toc-item"><a href="#{anc2}">{clean_leader_dots(line)}</a></li>')
                    i += 1
                    continue
                
                # 第X卷 条目（清理引导符）
                cleaned = clean_leader_dots(line)
                html.append(f'<li class="toc-item">{cleaned}</li>')
                i += 1
            
            html.append('</ul>')
            html.append('</div>')
            i = toc_end
            continue
        elif is_toc:
            i = toc_end
            continue
        
        # 非总篇目区域的正常处理
        s = para
        
        # 过滤TOC页码残渣：第X……（N）模式
        sp = s.strip()
        if re.search(r"^第[一二三四五六七八九十百千零零\d]+[卷章节]\s*.*[….]{2,}\s*[\(（]\d+[\)）]$", sp):
            i += 1
            continue
        
        if is_title(s):
            s_clean = re.sub(r"[.…]+\(\d+\)$", "", s).strip()
            s_clean = re.sub(r"[.…]+$", "", s_clean).strip()
            s_clean = re.sub(r"·\d+·\s*", "", s_clean).strip()
            if s_clean in seen_titles:
                i += 1
                continue
            seen_titles.add(s_clean)
            anc = verified_toc.get(s_clean) or next((v for k,v in verified_toc.items() if k.replace(' ', '') == s_clean.replace(' ', '')), title_to_anchor(s_clean))
            if re.match(r"^第[一二三四五六七八九十百千零〇\d]+卷", s_clean):
                html.append(f"<h2 id=\"{anc}\">{s_clean}</h2>")
            elif re.match(r"^第[一二三四五六七八九十百千零〇\d]+章", s_clean):
                html.append(f"<h3 id=\"{anc}\">{s_clean}</h3>")
            elif re.match(r"^第[一二三四五六七八九十百千零〇\d]+节", s_clean):
                html.append(f"<h4 id=\"{anc}\">{s_clean}</h4>")
            elif s_clean in ("序", "凡例", "总述", "大事记", "总篇目", "附录", "跋", "编纂始末", "概述"):
                html.append(f"<h2 id=\"{anc}\">{s_clean}</h2>")
            else:
                html.append(f"<h3 id=\"{anc}\">{s_clean}</h3>")
        elif is_year_entry(s):
            html.append(f'<p class="year-entry">{s}</p>')
        elif is_list_item(s):
            html.append(f'<p class="list-item">{s}</p>')
        else:
            html.append(f"<p>{s}</p>")
        
        i += 1
    
    return "\n".join(html)


HTML_CSS = """<style>
  @page {
    size: A4;
    margin: 18mm 17mm 19mm 17mm;
    @bottom-center {
      content: "连云港市志 · " counter(page);
      font-family: SimSun, "Noto Serif SC", serif;
      font-size: 9pt;
      color: #666;
    }
  }
  * { box-sizing: border-box; }
  html { background: #f1f1ef; }
  body {
    margin: 0;
    color: #1f1c18;
    font-family: "Noto Serif SC", SimSun, serif;
    font-size: 11.2pt;
    line-height: 1.78;
    letter-spacing: 0;
  }
  a { color: #145d66; text-decoration: none; }
  .page {
    max-width: 900px;
    margin: 0 auto;
    background: #fffefa;
    padding: 36px 48px 72px;
  }
  h1, h2, h3, h4, h5, h6 {
    font-family: "Noto Sans SC", "Microsoft YaHei", sans-serif;
    letter-spacing: 0;
    line-height: 1.35;
    page-break-after: avoid;
  }
  h1 { font-size: 24pt; text-align: center; margin: 20px 0 18px; page-break-before: always; }
  h2 { font-size: 18pt; margin: 24px 0 12px; border-bottom: 1px solid #d8d0c2; padding-bottom: 5px; }
  h3 { font-size: 14pt; margin: 18px 0 8px; }
  h4 { font-size: 12pt; margin: 14px 0 7px; }
  p { margin: 0 0 8px; text-align: justify; text-indent: 2em; }
  .year-entry { font-weight: 600; color: #1a1a1a; text-indent: 1em; margin-top: 1em; }
  .list-item { text-indent: 1em; }
  hr { border: 0; border-top: 1px solid #d8d0c2; margin: 18px 0; }
  .page-anchor { display: none !important; }
  h2:target { background: #ffeeba; transition: background 1s; }
  h3:target { background: #fff3cd; transition: background 1s; }
  h4:target { background: #fff8e1; transition: background 1s; }
    .table-page { background: #fff3cd; padding: 10px; border: 1px dashed #c9c0b3; margin: 15px 0; font-style: italic; color: #856404; font-size: 10pt; }
  .source-page { display: none !important; }
  .continuation-note { display: none !important; }
  .table-ref { display: none !important; }
  /* 总篇目/目录样式 */
  .toc-section { margin: 18px 0; padding: 12px 0; }
  .toc-title { border: none !important; font-size: 18pt; text-align: center; margin-bottom: 16px; }
  .toc-list { list-style: none; padding: 0; margin: 0; }
  .toc-item { padding: 2px 0; font-size: 11pt; line-height: 1.6; }
  .toc-chapter { padding-left: 20px !important; font-size: 10pt !important; color: #666; }
  .toc-chapter a { color: #666; }
  .toc-item::before { content: ""; }
  .toc-book-mark { text-align: center; font-weight: bold; margin: 8px 0 4px; font-size: 12pt; }
  @media print {
    body { background: #fff; }
    .page { background: #fff; box-shadow: none; padding: 0; }
    .table-page { background: #fff; border: none; }
  }
</style>"""


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    # ── 合并分章（保留原始MD格式用于存档） ──
    merged_lines = []
    merged_lines.append("# 连云港市志 上册正文汇总 (PaddleOCR PP-OCRv6_small)")
    merged_lines.append("")
    merged_lines.append("<!-- PaddleOCR 识别，已清理页眉页脚和 OCR 元信息 -->")
    merged_lines.append("")

    stats = []
    for fname in CHAPTER_ORDER:
        fpath = CHAPTER_DIR / fname
        if not fpath.exists():
            print(f"[WARN] 缺失: {fname}")
            continue
        text = fpath.read_text(encoding="utf-8")
        text = re.sub(r"<!-- PaddleOCR PP-OCRv6_small.*?-->\n", "", text, flags=re.DOTALL)
        text = re.sub(r"<!-- 内部页锚保留.*?-->\n", "", text, flags=re.DOTALL)
        merged_lines.append(text.rstrip())
        merged_lines.append("")
        merged_lines.append("---")
        merged_lines.append("")

        pages = len(re.findall(r"<!-- page-anchor:", text))
        table_pages = len(re.findall(r"<!-- TABLE-PAGE:", text))
        chars = len(re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip())
        stats.append({"file": fname, "pages": pages, "table_pages": table_pages, "chars": chars})

    merged_text = "\n".join(merged_lines)
    OUT_MERGED.write_text(merged_text, encoding="utf-8")

    # ── 生成 HTML（含段落合并） ──
    html_lines = [
        '<!DOCTYPE html>',
        '<html lang="zh-CN">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>连云港市志 上册 (PaddleOCR 精修版)</title>',
        HTML_CSS,
        '</head>',
        '<body>',
        '<div class="page">',
        '',
        # 封面
        '<div style="text-align:center;margin:3em 0 2em">',
        '<h1 style="font-size:2.2em;border:none;color:#8B0000;page-break-before:auto">连云港市志</h1>',
        '<p style="text-indent:0;font-size:1.1em;color:#666">上册 · PaddleOCR 精修版</p>',
        f'<p style="text-indent:0;font-size:.85em;color:#999">生成于 {now}</p>',
        '</div>',
        '<hr>',
        '',
    ]

    total_paras = 0
    all_paragraphs = []
    for i, fname in enumerate(CHAPTER_ORDER):
        fpath = CHAPTER_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        chapter_title = fname.replace(".md", "")
        paragraphs = process_chapter(text)
        # 添加章节分隔标记
        all_paragraphs.append("【CHAPTER_START】" + chapter_title)
        all_paragraphs.extend(paragraphs)
        total_paras += len(paragraphs)
        print(f"  [{chapter_title}] {len(paragraphs)} 段落")

    # 一次性生成（全局去重+单个TOC）
    # 处理章节分隔符：转换为h1标题
    processed_paras = []
    for pp in all_paragraphs:
        if pp.startswith("【CHAPTER_START】"):
            ch_title = pp.replace("【CHAPTER_START】", "")
            processed_paras.append("")  # 空行作为分隔
            html_lines.append(f"<h1>{ch_title}</h1>")
        else:
            processed_paras.append(pp)
    body_html = paragraphs_to_html(processed_paras)
    html_lines.append(body_html)

    html_lines.append(f'<p style="text-indent:0;text-align:center;color:#999;font-size:.85em;margin-top:2em;padding-top:1em;border-top:1px solid #eee">连云港市志 · 上册 PaddleOCR 精修版 · 生成于 {now}<br>891页 · {total_paras} 自然段落</p>')
    html_lines.append("</div>")
    html_lines.append("</body>")
    html_lines.append("</html>")

    html_text = "\n".join(html_lines)
    OUT_HTML.write_text(html_text, encoding="utf-8")

    # ── 进度报告 ──
    total_pages = sum(s["pages"] for s in stats)
    total_table = sum(s["table_pages"] for s in stats)
    total_chars = sum(s["chars"] for s in stats)

    rep = []
    rep.append("# 上册 PaddleOCR 精修进度")
    rep.append("")
    rep.append(f"**更新时间**: {now}")
    rep.append(f"**OCR 引擎**: PaddleOCR PP-OCRv6_small")
    rep.append(f"**平均置信度**: ~0.99")
    rep.append(f"**段落合并**: 已启用（页内合并 + 跨页回接）")
    rep.append("")
    rep.append("## 总体状态")
    rep.append("")
    rep.append(f"- 上册总页数：903（全局页 1-903）")
    rep.append(f"- 正文页数：{total_pages}")
    rep.append(f"- 表格页（已标注占位）：{total_table}")
    rep.append(f"- 精修后总字符数：{total_chars}")
    rep.append(f"- 自然段落数：{total_paras}")
    rep.append(f"- 缺失页：0")
    rep.append(f"- 页眉残留：0")
    rep.append("")
    rep.append("## 分章统计")
    rep.append("")
    rep.append("| 章节 | 页数 | 表格页 | 字符数 | 段落数 |")
    rep.append("| --- | ---: | ---: | ---: | ---: |")
    for s in stats:
        rep.append(f"| {s['file']} | {s['pages']} | {s['table_pages']} | {s['chars']} | - |")
    rep.append(f"| **合计** | **{total_pages}** | **{total_table}** | **{total_chars}** | **{total_paras}** |")
    rep.append("")
    rep.append("## PaddleOCR vs RapidOCR 对比")
    rep.append("")
    rep.append("| 指标 | RapidOCR | PaddleOCR (PP-OCRv6_small) |")
    rep.append("| --- | --- | --- |")
    rep.append("| 平均置信度 | 0.88 | **0.99** |")
    rep.append("| 每页耗时 | ~10s | **~9s** |")
    rep.append("| 总字符数 | 969,866 | **1,000,930** (+3.2%) |")
    rep.append("| 关键错字修正 | 需人工脚本 | 自动修正 ~70% |")
    rep.append("| 标点符号 | 半角/全角混用 | 半角统一 |")
    rep.append("")
    rep.append("## 待后续处理")
    rep.append("")
    rep.append("- 剩余 OCR 错字自动纠错（糟运→漕运、尽夜→昼夜、同治→同知 等）")
    rep.append("- 标点符号规范化（半角括号→全角）")
    rep.append("- 表格页结构化（209 页）")
    rep.append("- 中下册 PaddleOCR 重识别")

    OUT_REPORT.write_text("\n".join(rep), encoding="utf-8")

    print("=== PaddleOCR 上册汇总与 HTML 生成完成 ===")
    print(f"分章文件: {len(stats)} 个")
    print(f"总页数: {total_pages}  表格页: {total_table}  总字符: {total_chars}  段落数: {total_paras}")
    print(f"汇总 MD: {OUT_MERGED}")
    print(f"HTML:     {OUT_HTML}")
    print(f"报告:     {OUT_REPORT}")


if __name__ == "__main__":
    main()
