#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连云港市志 上册 表格构建脚本生成器
为每个表格生成 build_table 脚本模板（东辛农场志风格）
"""
import sys, re, os, json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation')
BODY_DIR = ROOT / 'workbench' / 'body_chapters' / '上'
SCRIPTS_DIR = ROOT / 'workbench' / 'table_entries' / '上' / 'scripts'
OUT_INDEX = ROOT / 'workbench' / 'table_entries' / '上' / '表格构建脚本清单.md'

CHAPTER_RANGES = [
    (1, 12, '序', '序与凡例'), (13, 28, '凡例', '序与凡例'),
    (29, 123, '总述与大事记', '总述与大事记'),
    (124, 212, '第一卷', '自然环境'), (213, 231, '第二卷', '建置区划'),
    (232, 278, '第三卷', '区县概况'), (279, 300, '第四卷', '人口'),
    (301, 400, '第五卷', '城乡建设'), (401, 459, '第六卷', '环境保护'),
    (460, 510, '第七卷', '经济综情'), (511, 594, '第八卷', '经济综合管理'),
    (595, 605, '第九卷', '农林业'), (606, 652, '第十卷', '水利'),
    (653, 750, '第十一卷', '水产/盐业'), (751, 810, '第十二卷', '工业'),
    (811, 903, '第十三卷', '乡镇/附录'),
]

def get_volume_chapter(page):
    for s, e, vol, ch in CHAPTER_RANGES:
        if s <= page <= e:
            return vol, ch
    return '', ''

def extract_and_group():
    CHAPTER_FILES = [
        "序与凡例.md", "总述与大事记.md", "第一卷_自然环境.md",
        "第二卷_建置区划.md", "第三卷_区县概况.md",
        "第四卷_人口（part01_部分）.md", "第四卷至第十卷（part02）.md",
        "第十卷至第十六卷（part03）.md",
    ]
    blocks = []
    for fname in CHAPTER_FILES:
        fpath = BODY_DIR / fname
        if not fpath.exists():
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = re.compile(
            r'<!-- TABLE-PAGE:\s*p(\d+).*?-->\n'
            r'(.*?)(?=<!-- TABLE-PAGE:|<!-- page-anchor:|\Z)',
            re.DOTALL
        )
        for m in pattern.finditer(content):
            page = int(m.group(1))
            ocr_text = m.group(2).strip()
            blocks.append({'page': page, 'file': fname, 'ocr_text': ocr_text})
    blocks.sort(key=lambda b: b['page'])

    tables = []
    current = []
    for b in blocks:
        if current and (b['page'] - current[-1]['page']) > 3:
            tables.append(current)
            current = []
        current.append(b)
    if current:
        tables.append(current)

    result = []
    for i, group in enumerate(tables, 1):
        pages = [b['page'] for b in group]
        title = ''
        for b in group:
            for line in b['ocr_text'].split('\n'):
                line = line.strip()
                if not line or line.startswith('·') or re.match(r'^[\d\s\[\]\(\)]+$', line):
                    continue
                if '表' in line and '续上' not in line and '续表' not in line and len(line) < 100:
                    title = line
                    break
            if title:
                break
        if not title:
            title = f'第{pages[0]}页表格'
        title = re.sub(r'^[·\d\s]+', '', title)
        title = re.sub(r'[·\d\s]+$', '', title)
        vol, ch = get_volume_chapter(pages[0])
        result.append({
            'id': i, 'table_id': f'LYG-上-T{i:03d}',
            'title': title, 'pages': pages, 'page_count': len(group),
            'volume': vol, 'chapter': ch, 'blocks': group,
        })
    return result

def generate_build_script(table):
    tid = table['table_id']
    title = table['title']
    pages = table['pages']
    vol = table['volume']
    ch = table['chapter']

    # 清理 OCR 文本
    ocr_lines = []
    for b in table['blocks']:
        for line in b['ocr_text'].split('\n'):
            line = line.strip()
            if not line or re.match(r'^[·\d\[\]\s\(\)]+$', line):
                continue
            if '<!--' in line or '-->' in line:
                continue
            ocr_lines.append(line)
    ocr_text = '\n'.join(ocr_lines[:60])

    # 手动构建脚本（避免 f-string 三引号冲突）
    parts = []
    parts.append('#!/usr/bin/env python3')
    parts.append('# -*- coding: utf-8 -*-')
    parts.append('"""')
    parts.append(f'{tid} \u2014 {title}')
    parts.append(f'页: {pages}')
    parts.append(f'卷: {vol} 章: {ch}')
    parts.append('状态: draft（初稿，待对照原图核对）')
    parts.append('"""')
    parts.append('')
    parts.append('import csv, io, json')
    parts.append('from pathlib import Path')
    parts.append('')
    parts.append(f'TABLE_ID = "{tid}"')
    parts.append(f'TITLE = """{title}"""')
    parts.append(f'PAGES = {pages}')
    parts.append('')
    parts.append('# === 列定义（需对照原图确认） ===')
    parts.append('COLUMNS = [')
    parts.append('    # 请在此定义列名，例如:')
    parts.append('    # "序号", "名称", "面积(km2)", "人口(万人)", "年份", "备注"')
    parts.append(']')
    parts.append('')
    parts.append('# === 表格数据（需对照原图逐行录入） ===')
    parts.append('# 格式：CSV 文本，第一行必须是列名（与 COLUMNS 一致）')
    parts.append(f'# 建议对照原图 page_{pages[0]} 录入')
    parts.append('VERIFIED_CSV = """"""')
    parts.append('')
    parts.append('# === OCR 参考文本（仅供参考，请以原图为准） ===')
    parts.append('OCR_REF = """')
    parts.append(ocr_text)
    parts.append('"""')
    parts.append('')
    parts.append('')
    parts.append('def verify_and_export():')
    parts.append('    reader = csv.reader(io.StringIO(VERIFIED_CSV))')
    parts.append('    header = next(reader, [])')
    parts.append('    if header and header != COLUMNS:')
    parts.append('        print(f"警告: CSV 表头与 COLUMNS 不匹配")')
    parts.append('        print(f"  CSV: {header}")')
    parts.append('        print(f"  COL: {COLUMNS}")')
    parts.append('    rows = list(reader)')
    parts.append('    print(f"{TABLE_ID} {TITLE.strip()}")')
    parts.append('    cols = len(COLUMNS)')
    parts.append('    print(f"  页: {PAGES}")')
    parts.append('    print(f"  列数: {cols}")')
    parts.append('    print(f"  数据行数: {len(rows)}")')
    parts.append('')
    parts.append('    # 输出 JSON')
    parts.append('    data_dir = Path(__file__).resolve().parent.parent / "data"')
    parts.append('    data_dir.mkdir(parents=True, exist_ok=True)')
    parts.append('    entry = {')
    parts.append('        "table_id": TABLE_ID,')
    parts.append('        "title": TITLE.strip(),')
    parts.append('        "pages": PAGES,')
    parts.append('        "columns": COLUMNS,')
    parts.append('        "rows": rows,')
    parts.append('        "status": "draft",')
    parts.append('    }')
    parts.append('    out_path = data_dir / f"{TABLE_ID}.json"')
    parts.append('    with open(out_path, "w", encoding="utf-8") as f:')
    parts.append('        json.dump(entry, f, ensure_ascii=False, indent=2)')
    parts.append('    print(f"  输出: {out_path}")')
    parts.append('')
    parts.append('if __name__ == "__main__":')
    parts.append('    verify_and_export()')
    parts.append('')

    return '\n'.join(parts)

def main():
    print('=== 连云港市志 上册 表格构建脚本生成 ===')
    print()
    tables = extract_and_group()
    print(f'共 {len(tables)} 个表格')
    print()

    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    index_lines = [
        '# 连云港市志 上册 表格构建脚本清单',
        '',
        f'共 {len(tables)} 个独立表格（125 个表格页）',
        '构建脚本生成时间: 自动生成',
        '',
        '| ID | 标题 | 页码 | 页数 | 卷 | 脚本文件 |',
        '|--- | --- | ---: | ---: | --- | --- |',
    ]

    for t in tables:
        fname = f'build_{t["table_id"]}.py'
        fpath = SCRIPTS_DIR / fname
        script = generate_build_script(t)
        fpath.write_text(script, encoding='utf-8')
        pages_str = f'{t["pages"][0]}-{t["pages"][-1]}' if len(t["pages"]) > 1 else str(t["pages"][0])
        index_lines.append(
            f'| {t["table_id"]} | {t["title"][:40]} | {pages_str} | {t["page_count"]} | {t["volume"]} | `{fname}` |'
        )
        print(f'  [{t["id"]:2d}/{len(tables)}] {t["table_id"]} \u2014 {t["title"][:40]}')

    OUT_INDEX.parent.mkdir(parents=True, exist_ok=True)
    OUT_INDEX.write_text('\n'.join(index_lines), encoding='utf-8')
    print(f'\n索引: {OUT_INDEX}')
    print(f'脚本目录: {SCRIPTS_DIR}')
    print()
    print('=== 生成完成 ===')

if __name__ == '__main__':
    main()
