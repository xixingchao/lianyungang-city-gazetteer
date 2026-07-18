#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连云港市志 上册 表格结构化流水线
- 从 body_chapters 提取所有 TABLE-PAGE 块
- 分组为独立表格
- 从 JSON OCR 数据重建行列结构
- 输出 CSV + 结构化报告
"""
import sys, re, os, json, csv
import io
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

# === 配置 ===
ROOT = Path(r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation')
BODY_DIR = ROOT / 'workbench' / 'body_chapters' / '上'
OCR_DIR = ROOT / 'workbench' / 'ocr' / 'raw' / '上'
TABLE_DIR = ROOT / 'workbench' / 'table_entries' / '上'
OUT_REPORT = ROOT / 'output' / 'reports' / '上册表格结构化结果.md'

CHAPTER_FILES = [
    "序与凡例.md", "总述与大事记.md", "第一卷_自然环境.md",
    "第二卷_建置区划.md", "第三卷_区县概况.md",
    "第四卷_人口（part01_部分）.md", "第四卷至第十卷（part02）.md",
    "第十卷至第十六卷（part03）.md",
]

# part → (global_start, global_end)
PART_OFFSET = {'part01': (1, 300), 'part02': (301, 605), 'part03': (606, 903)}

# 页面范围到卷章映射（用于表格编号）
VOLUME_CHAPTER = {
    (1, 12): ('序', '序与凡例'), (13, 28): ('凡例', '序与凡例'),
    (29, 123): ('总述与大事记', '总述与大事记'),
    (124, 212): ('第一卷', '自然环境'), (213, 231): ('第二卷', '建置区划'),
    (232, 278): ('第三卷', '区县概况'), (279, 300): ('第四卷', '人口'),
    (301, 400): ('第五卷', '城乡建设'), (401, 459): ('第六卷', '环境保护'),
    (460, 510): ('第七卷', '经济综情'), (511, 594): ('第八卷', '经济综合管理'),
    (595, 605): ('第九卷', '农林业'), (606, 652): ('第十卷', '水利'),
    (653, 902): ('第十一卷', '畜牧业/水产/盐业等'),
}


# ===========================================================
# Step 1: 提取 TABLE-PAGE 块
# ===========================================================
def extract_table_blocks():
    """从所有 body 文件中提取 TABLE-PAGE 块"""
    blocks = []
    for fname in CHAPTER_FILES:
        fpath = BODY_DIR / fname
        if not fpath.exists():
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 按页码提取每个 TABLE-PAGE 块
        pattern = re.compile(
            r'<!-- TABLE-PAGE:\s*p(\d+).*?-->\n'
            r'(.*?)(?=<!-- TABLE-PAGE:|<!-- page-anchor:|\Z)',
            re.DOTALL
        )
        for m in pattern.finditer(content):
            page = int(m.group(1))
            ocr_text = m.group(2).strip()
            blocks.append({
                'page': page,
                'file': fname,
                'ocr_text': ocr_text,
                'ocr_len': len(ocr_text),
            })

    blocks.sort(key=lambda b: b['page'])
    return blocks


# ===========================================================
# Step 2: 分组为独立表格
# ===========================================================
def group_tables(blocks):
    """将连续的表格页分为独立表格"""
    tables = []
    current = []
    for b in blocks:
        if current and (b['page'] - current[-1]['page']) > 3:
            tables.append(current)
            current = []
        current.append(b)
    if current:
        tables.append(current)

    # 给每个表格赋 ID 和标题
    result = []
    for i, group in enumerate(tables, 1):
        pages = [b['page'] for b in group]
        # 提取标题（取第一个非 续上表 的文本）
        title = ''
        for b in group:
            text = b['ocr_text']
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            for line in lines:
                line_clean = re.sub(r'^[·\d\s\[\]]+', '', line)
                if '表' in line_clean and len(line_clean) < 100 \
                   and '续上' not in line_clean and '续表' not in line_clean:
                    title = line_clean
                    break
            if title:
                break
        if not title:
            title = f'（第{pages[0]}页表格）'

        result.append({
            'id': i,
            'table_id': f'LYG-上-T{i:03d}',
            'title': title,
            'pages': pages,
            'page_count': len(group),
            'blocks': group,
        })
    return result


# ===========================================================
# Step 3: 从 JSON OCR 数据提取行坐标
# ===========================================================
def get_part_and_local(page):
    """根据全局页码确定 part 和本地页码"""
    for part, (start, end) in PART_OFFSET.items():
        if start <= page <= end:
            return part, page - start + 1
    return None, None


def load_ocr_lines(page):
    """加载一页的 OCR 行坐标数据"""
    part, local = get_part_and_local(page)
    if not part:
        return []

    json_path = OCR_DIR / part / f'page_{local:04d}.json'
    if not json_path.exists():
        return []

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lines = data.get('lines', [])
    result = []
    for line in lines:
        text = line.get('text', '').strip()
        if not text:
            continue
        box = line.get('box', [])
        if len(box) >= 4:
            # 取左上和右下坐标
            x1, y1 = box[0]
            x2, y3 = box[2]
            cx = (x1 + x2) / 2  # 水平中心
            cy = (y1 + y3) / 2  # 垂直中心
        else:
            cx = cy = 0
        result.append({
            'text': text,
            'x': x1 if len(box) >= 4 else 0,
            'y': y1 if len(box) >= 4 else 0,
            'cx': cx,
            'cy': cy,
            'x2': x2 if len(box) >= 4 else 0,
            'y2': y3 if len(box) >= 4 else 0,
        })
    return result


# ===========================================================
# Step 4: 自动重建行列结构
# ===========================================================
def structure_table(lines, y_tolerance=30, min_columns=2):
    """
    基于 y/x 坐标重建表格行列结构。
    - 按 y 坐标分组为行
    - 每行内按 x 坐标排序为列
    """
    if not lines:
        return []

    # 过滤明显不是表格内容的段落级文本（太宽的文字段落）
    # 检测标准：文本框宽度 > 700（全页宽度）且不是标题
    table_lines = []
    for l in lines:
        width = l['x2'] - l['x']
        # 全宽段落（正文）过滤
        if width > 700 and len(l['text']) > 20:
            continue
        # 页码过滤
        if re.match(r'^[·\d\s\[\]]{1,10}$', l['text']):
            continue
        # 页眉过滤
        if re.match(r'^·\d+·', l['text']):
            continue
        table_lines.append(l)

    if not table_lines:
        return []

    # 按 y 坐标排序
    table_lines.sort(key=lambda l: (l['y'], l['x']))

    # 分组为行（y 坐标相近的在一行）
    rows = []
    current_row = [table_lines[0]]
    for l in table_lines[1:]:
        prev = current_row[-1]
        if abs(l['y'] - prev['y']) <= y_tolerance:
            current_row.append(l)
        else:
            # 检查当前行是否很可能是新行的开始（y 跳跃 >= y_tolerance）
            rows.append(current_row)
            current_row = [l]
    if current_row:
        rows.append(current_row)

    # 每行内按 x 坐标排序
    for row in rows:
        row.sort(key=lambda l: l['x'])

    # 转换为行列结构
    # 检测列边界：对所有行的 x 坐标做聚类
    all_x_starts = set()
    for row in rows:
        for cell in row:
            all_x_starts.add(round(cell['x'] / 20) * 20)  # 量化到 20px 粒度

    grid = []
    for row_idx, row in enumerate(rows):
        grid_row = []
        for cell in row:
            grid_row.append(cell['text'])
        grid.append(grid_row)

    return grid


# ===========================================================
# Step 5: 输出处理
# ===========================================================
def grid_to_csv(table_id, grid, output_path):
    """将 grid 数据输出为 CSV"""
    if not grid:
        return 0
    # 估计列数（用最长行）
    max_cols = max(len(r) for r in grid)
    # 补齐所有行的列数
    for row in grid:
        while len(row) < max_cols:
            row.append('')
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(grid)
    return len(grid)


def process_all_tables(tables):
    """处理所有表格"""
    results = []
    TABLE_DIR_RAW.mkdir(parents=True, exist_ok=True)
    TABLE_DIR_CSV.mkdir(parents=True, exist_ok=True)

    for t in tables:
        tid = t['table_id']
        # Step 3: 加载所有页的 OCR 行数据
        all_lines = []
        for b in t['blocks']:
            lines = load_ocr_lines(b['page'])
            all_lines.extend(lines)

        # Step 4: 结构化
        grid = structure_table(all_lines)
        t['grid'] = grid
        t['row_count'] = len(grid)
        t['col_count'] = max(len(r) for r in grid) if grid else 0

        # 保存 raw 文本
        raw_text = ''
        for b in t['blocks']:
            for line in load_ocr_lines(b['page']):
                raw_text += line['text'] + '\n'
        raw_path = TABLE_DIR_RAW / f'{tid}_{t["pages"][0]}.txt'
        raw_path.write_text(raw_text, encoding='utf-8')

        # 输出 CSV
        csv_path = TABLE_DIR_CSV / f'{tid}_{t["pages"][0]}.csv'
        rows = grid_to_csv(tid, grid, csv_path)

        # 输出结构可视化（文本）
        vis_path = TABLE_DIR_CSV / f'{tid}_{t["pages"][0]}_preview.txt'
        vis_lines = [f'表格: {t["title"]}', f'ID: {tid}', f'页: {t["pages"]}',
                     f'行数: {rows}', f'列数: {t["col_count"]}']
        vis_lines.append('')
        for row in grid[:15]:
            vis_lines.append(' | '.join(f'{c[:15]:15s}' for c in row[:6]))
        if len(grid) > 15:
            vis_lines.append(f'... ({len(grid)-15} 行省略)')
        vis_path.write_text('\n'.join(vis_lines), encoding='utf-8')

        results.append({
            'table_id': tid,
            'title': t['title'],
            'pages': t['pages'],
            'page_count': t['page_count'],
            'rows': t['row_count'],
            'cols': t['col_count'],
            'csv': str(csv_path),
        })

        print(f'  [{tid}] {t["title"][:40]:40s}  {t["page_count"]}页  {t["row_count"]}行×{t["col_count"]}列')

    return results


def write_report(all_tables, results):
    """生成处理报告"""
    lines = []
    lines.append('# 连云港市志 上册 表格结构化结果')
    lines.append('')
    lines.append(f'总计: {len(results)} 个独立表格（{sum(t["page_count"] for t in all_tables)} 页）')
    lines.append('')

    # 统计质量
    good = sum(1 for r in results if r['cols'] >= 2 and r['rows'] >= 2)
    needs_review = sum(1 for r in results if r['cols'] < 2 or r['rows'] < 2)
    lines.append(f'自动结构化成功（≥2列×≥2行）: {good}')
    lines.append(f'需人工复查（行列不足）: {needs_review}')
    lines.append('')

    lines.append('## 表格列表')
    lines.append('')
    lines.append('| ID | 标题 | 页码 | 页数 | 行×列 | 质量 |')
    lines.append('|--- | --- | ---: | ---: | ---: | --- |')
    for r in results:
        quality = '✓' if r['cols'] >= 2 and r['rows'] >= 2 else '△'
        pages_str = f'{r["pages"][0]}-{r["pages"][-1]}' if len(r['pages']) > 1 else str(r['pages'][0])
        lines.append(f'| {r["table_id"]} | {r["title"][:40]} | {pages_str} | {r["page_count"]} | {r["rows"]}×{r["cols"]} | {quality} |')

    lines.append('')
    lines.append('## 输出文件')
    lines.append('')
    lines.append(f'- RAW 文本: `table_entries/上/raw/`')
    lines.append(f'- CSV 数据: `table_entries/上/csv/`')
    lines.append(f'- 预览文件: `table_entries/上/csv/*_preview.txt`')
    lines.append('')

    (TABLE_DIR.parent / '上').mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\n报告: {OUT_REPORT}')


# ===========================================================
# Main
# ===========================================================
if __name__ == '__main__':
    TABLE_DIR_RAW = TABLE_DIR / 'raw'
    TABLE_DIR_CSV = TABLE_DIR / 'csv'

    print('=== 连云港市志 上册 表格结构化流水线 ===')
    print()

    print('[Step 1] 提取 TABLE-PAGE 块...')
    blocks = extract_table_blocks()
    print(f'  提取到 {len(blocks)} 个表格页标记')

    print()
    print('[Step 2] 分组为独立表格...')
    tables = group_tables(blocks)
    print(f'  分为 {len(tables)} 个独立表格')

    print()
    print('[Step 3-4] 加载 OCR 行数据 + 自动结构化...')
    results = process_all_tables(tables)

    print()
    print('[Step 5] 生成报告...')
    write_report(tables, results)

    print()
    print('=== 完成 ===')
