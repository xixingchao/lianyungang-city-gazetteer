#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连云港市志 上册 表格页清单生成
提取所有 TABLE-PAGE 标记的页及其上下文，生成表格索引。
"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

BODY_DIR = r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation\workbench\body_chapters\上'
OUTPUT = r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation\output\reports\上册表格页清单.md'

CHAPTER_FILES = [
    "序与凡例.md",
    "总述与大事记.md",
    "第一卷_自然环境.md",
    "第二卷_建置区划.md",
    "第三卷_区县概况.md",
    "第四卷_人口（part01_部分）.md",
    "第四卷至第十卷（part02）.md",
    "第十卷至第十六卷（part03）.md",
]

def get_ocr_raw(page_global, part_offset_map):
    """从 OCR raw 读取原始文本"""
    for part, (start, end, part_dir) in part_offset_map.items():
        if start <= page_global <= end:
            local_page = page_global - start + 1
            txt_path = os.path.join(part_dir, f'page_{local_page:04d}.txt')
            if os.path.exists(txt_path):
                with open(txt_path, 'r', encoding='utf-8') as f:
                    return f.read()
    return None

def extract_table_info():
    # part → (global_start, global_end, dir)
    part_offset_map = {
        'part01': (0, 300, r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation\workbench\ocr\raw\上\part01'),
        'part02': (300, 605, r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation\workbench\ocr\raw\上\part02'),
        'part03': (605, 903, r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation\workbench\ocr\raw\上\part03'),
    }
    # Adjust: part01 global pages = p1-p300, part02 = p301-p605, part03 = p606-p903
    part_offset_map = {
        'part01': (1, 300, r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation\workbench\ocr\raw\上\part01'),
        'part02': (301, 605, r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation\workbench\ocr\raw\上\part02'),
        'part03': (606, 903, r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation\workbench\ocr\raw\上\part03'),
    }
    
    tables = []
    
    for fname in CHAPTER_FILES:
        fpath = os.path.join(BODY_DIR, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all TABLE-PAGE markers
        pattern = re.compile(r'<!-- TABLE-PAGE: p(\d+).*?-->\n\n(.*?)(?=<!-- TABLE-PAGE:|<!-- page-anchor:|\Z)', re.DOTALL)
        for m in pattern.finditer(content):
            page = int(m.group(1))
            ocr_text = m.group(2).strip()
            
            # Get OCR raw
            raw = get_ocr_raw(page, part_offset_map)
            
            # Extract table title from OCR text or body
            title = ''
            lines = ocr_text.split('\n')
            for line in lines:
                line = line.strip()
                if '表' in line and len(line) < 80 and not line.startswith('·'):
                    title = line
                    break
            
            tables.append({
                'page': page,
                'file': fname,
                'title': title[:60] if title else '',
                'ocr_len': len(ocr_text),
                'ocr_preview': ocr_text[:100].replace('\n', ' '),
            })
    
    # Sort by page
    tables.sort(key=lambda t: t['page'])
    
    # Detect cross-page tables
    for i in range(1, len(tables)):
        if abs(tables[i]['page'] - tables[i-1]['page']) <= 2:
            if not tables[i-1].get('continued'):
                tables[i-1]['continued'] = True
            tables[i]['continuation'] = True
    
    return tables

def write_report(tables):
    lines = []
    lines.append('# 连云港市志 上册 表格页清单')
    lines.append('')
    lines.append(f'统计时间：自动生成')
    lines.append(f'表格页总数：{len(tables)}')
    lines.append('')
    
    # Summary by file
    from collections import Counter
    file_counts = Counter(t['file'] for t in tables)
    lines.append('## 分文件统计')
    lines.append('')
    lines.append('| 文件 | 表格页数 |')
    lines.append('| --- | ---: |')
    for fname, cnt in sorted(file_counts.items()):
        lines.append(f'| {fname} | {cnt} |')
    lines.append(f'| **合计** | **{len(tables)}** |')
    lines.append('')
    
    # Cross-page tables
    cont_groups = []
    current = []
    for t in tables:
        if current and abs(t['page'] - current[-1]['page']) > 2:
            if len(current) > 1:
                cont_groups.append(current)
            current = []
        current.append(t)
    if len(current) > 1:
        cont_groups.append(current)
    
    if cont_groups:
        lines.append('## 跨页续表组')
        lines.append('')
        for group in cont_groups:
            pages = [str(t['page']) for t in group]
            titles = [t['title'] for t in group if t['title']]
            title = titles[0] if titles else '(无标题)'
            lines.append(f'- **{title}** — 第 {", ".join(pages)} 页（{len(group)} 页）')
        lines.append('')
    
    # Detail table
    lines.append('## 全部表格页')
    lines.append('')
    lines.append('| # | 页码 | 卷册 | 标题/首行 | OCR 长度 |')
    lines.append('|--- | ---: | --- | --- | ---: |')
    for i, t in enumerate(tables, 1):
        vol = 'part01' if t['page'] <= 300 else ('part02' if t['page'] <= 605 else 'part03')
        tag = ' →续' if t.get('continuation') else ('续→' if t.get('continued') else '')
        lines.append(f'| {i} | {t["page"]} | {vol} | {t["title"][:50]}{tag} | {t["ocr_len"]} |')
    lines.append('')
    
    lines.append('## OCR 原文预览（部分）')
    lines.append('')
    for t in tables[:5]:
        lines.append(f'### 第 {t["page"]} 页 — {t["title"][:40]}')
        lines.append('')
        lines.append('```')
        raw = t['ocr_preview'][:200]
        lines.append(raw)
        lines.append('```')
        lines.append('')
    
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'报告已生成: {OUTPUT}')
    print(f'表格页总数: {len(tables)}')

if __name__ == '__main__':
    tables = extract_table_info()
    write_report(tables)
