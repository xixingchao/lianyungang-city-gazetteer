#!/usr/bin/env python3
# -*- coding: utf-8 -*-"
"""
连云港市志 中册/下册 表格清单提取
从正文章节文件中扫描 TABLE-PAGE 标记，提取表格页信息。
"""
import sys, re, json, os
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation')
BODY_DIR = ROOT / 'workbench' / 'body_chapters'
OUTPUT_DIR = ROOT / 'output' / 'reports'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 卷册配置：(描述, 文件名, 卷号范围)
VOLUMES = [
    {
        "vol": "中",
        "label": "中册 part01",
        "file": "第十七卷至第二十九卷（中part01）.md",
        "vol_range": "第十七卷~第二十九卷",
        "part": "part01",
    },
    {
        "vol": "中",
        "label": "中册 part02",
        "file": "第三十卷至第四十二卷（中part02）.md",
        "vol_range": "第三十卷~第四十二卷",
        "part": "part02",
    },
    {
        "vol": "下",
        "label": "下册 part01",
        "file": "第四十三卷至第五十一卷（下part01）.md",
        "vol_range": "第四十三卷~第五十一卷",
        "part": "part01",
    },
    {
        "vol": "下",
        "label": "下册 part02",
        "file": "第五十二卷至第六十卷及附录（下part02）.md",
        "vol_range": "第五十二卷~第六十卷+附录",
        "part": "part02",
    },
]

def extract_tables_from_file(filepath, vol_info):
    """从正文文件中提取所有 TABLE-PAGE 标记"""
    if not filepath.exists():
        print(f"  文件不存在: {filepath}")
        return []
    
    content = filepath.read_text(encoding='utf-8')
    
    pattern = re.compile(
        r'<!-- TABLE-PAGE: p(\d+) 表格页 -->\n\n(.*?)(?=<!-- TABLE-PAGE:|<!-- page-anchor:|\Z)',
        re.DOTALL
    )
    
    tables = []
    for m in pattern.finditer(content):
        page = int(m.group(1))
        ocr_text = m.group(2).strip()
        
        # 提取表格标题（从OCR文本中找包含"表"字的短行）
        title = ""
        lines = ocr_text.split('\n')
        for line in lines:
            line_stripped = line.strip()
            if '表' in line_stripped and len(line_stripped) < 100:
                title = line_stripped
                break
        
        # 如果没有找到，尝试取前几行的内容
        if not title and lines:
            for line in lines[:5]:
                ls = line.strip()
                if len(ls) > 3 and not ls.startswith('·'):
                    title = ls
                    break
        
        tables.append({
            "page": page,
            "vol": vol_info["vol"],
            "part": vol_info["part"],
            "file": vol_info["file"],
            "vol_range": vol_info["vol_range"],
            "title": title[:80] if title else "",
            "ocr_len": len(ocr_text),
            "ocr_preview": ocr_text[:200].replace('\n', ' '),
        })
    
    return tables

def detect_cross_page_tables(tables):
    """检测跨页续表"""
    sorted_tables = sorted(tables, key=lambda t: t['page'])
    for i in range(1, len(sorted_tables)):
        diff = sorted_tables[i]['page'] - sorted_tables[i-1]['page']
        if diff <= 2:
            if not sorted_tables[i-1].get('continued'):
                sorted_tables[i-1]['continued'] = True
            sorted_tables[i]['continuation'] = True
    return sorted_tables

def assign_table_ids(tables):
    """分配表格ID: LYG-中-T001, LYG-下-T001 等"""
    vol_counters = {}
    for t in tables:
        vol = t['vol']
        vol_counters.setdefault(vol, 0)
        vol_counters[vol] += 1
        t['table_id'] = f"LYG-{vol}-T{vol_counters[vol]:03d}"
    return tables

def main():
    all_tables = []
    
    print("=" * 60)
    print("连云港市志 中册/下册 表格清单提取")
    print("=" * 60)
    
    for v in VOLUMES:
        filepath = BODY_DIR / v['file']
        print(f"\n扫描: {v['label']} — {v['file']}")
        tables = extract_tables_from_file(filepath, v)
        print(f"  找到 {len(tables)} 个表格页")
        all_tables.extend(tables)
    
    # 排序（按页码全局排序）
    all_tables.sort(key=lambda t: t['page'])
    
    # 检测跨页
    all_tables = detect_cross_page_tables(all_tables)
    
    # 分配ID
    all_tables = assign_table_ids(all_tables)
    
    # 统计
    vol_counts = {}
    vol_titles = {}
    for t in all_tables:
        k = f"{t['vol']} ({t['vol_range']})"
        vol_counts[k] = vol_counts.get(k, 0) + 1
        if t['vol'] not in vol_titles:
            vol_titles[t['vol']] = []
        vol_titles[t['vol']].append(t)
    
    print("\n" + "=" * 60)
    print("统计摘要")
    print("=" * 60)
    for k, cnt in sorted(vol_counts.items()):
        print(f"  {k}: {cnt} 个表格页")
    print(f"  总计: {len(all_tables)} 个表格页")
    
    # 输出JSON
    json_path = OUTPUT_DIR / '中下册表格清单.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_tables, f, ensure_ascii=False, indent=2)
    print(f"\nJSON清单: {json_path}")
    
    # 输出Markdown报告
    report_path = OUTPUT_DIR / '中下册表格清单.md'
    lines = []
    lines.append('# 连云港市志 中册/下册 表格清单')
    lines.append('')
    lines.append(f'生成时间: 自动')
    lines.append(f'表格页总数: {len(all_tables)}')
    lines.append('')
    lines.append('## 分卷统计')
    lines.append('')
    lines.append('| 卷册 | 表格页数 |')
    lines.append('| --- | ---: |')
    for k, cnt in sorted(vol_counts.items()):
        lines.append(f'| {k} | {cnt} |')
    lines.append(f'| **合计** | **{len(all_tables)}** |')
    lines.append('')
    
    # 跨页表组
    cont_groups = []
    current = []
    sorted_tables = sorted(all_tables, key=lambda t: t['page'])
    for t in sorted_tables:
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
    
    # 详细清单
    lines.append('## 全部表格清单')
    lines.append('')
    lines.append('| 表格ID | 卷 | 页码 | 标题 | 跨页 |')
    lines.append('| --- | --- | ---: | --- | ---: |')
    for t in all_tables:
        tag = ''
        if t.get('continuation'):
            tag = '续表'
        elif t.get('continued'):
            tag = '→页'
        lines.append(f'| {t["table_id"]} | {t["vol"]} | {t["page"]} | {t["title"][:60]} | {tag} |')
    lines.append('')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"MD报告: {report_path}")
    
    # 输出按卷的ID+页面对照
    for vol in ['中', '下']:
        vol_tables = [t for t in all_tables if t['vol'] == vol]
        mapping_path = OUTPUT_DIR / f'{vol}册表格ID对照表.json'
        mapping = {t['table_id']: {"page": t['page'], "title": t['title']} for t in vol_tables}
        with open(mapping_path, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
        print(f"{vol}册ID对照表: {mapping_path}")
    
    return all_tables

if __name__ == '__main__':
    tables = main()
