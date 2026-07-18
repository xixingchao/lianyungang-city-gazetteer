#!/usr/bin/env python3
# -*- coding: utf-8 -*-"
"""
连云港市志 中册/下册 表格骨架自动生成
- 读取表格清单JSON
- 创建 table_entries/中/ 和 下/ 目录结构
- 生成所有表格的初始 JSON 骨架 (data/)
- 提取 OCR raw文本 (raw/)
- 生成 refine_tables.py （含所有 stub 函数）
- 生成 batch_build_all.py
"""
import sys, re, json, os
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation')
BODY_DIR = ROOT / 'workbench' / 'body_chapters'
OUTPUT_DIR = ROOT / 'output' / 'reports'
INVENTORY_FILE = OUTPUT_DIR / '中下册表格清单.json'

def load_inventory():
    with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_body_file_content(vol, part, page):
    """从正文文件中获取特定页附近的OCR文本"""
    fname_map = {
        "中_part01": "第十七卷至第二十九卷（中part01）.md",
        "中_part02": "第三十卷至第四十二卷（中part02）.md",
        "下_part01": "第四十三卷至第五十一卷（下part01）.md",
        "下_part02": "第五十二卷至第六十卷及附录（下part02）.md",
    }
    key = f"{vol}_{part}"
    fname = fname_map.get(key)
    if not fname:
        return ""
    fpath = BODY_DIR / fname
    if not fpath.exists():
        return ""
    return fpath.read_text(encoding='utf-8')

def extract_ocr_context_for_table(content, page):
    """从正文内容中提取指定页码的表格OCR文本"""
    pattern = re.compile(
        rf'<!-- TABLE-PAGE: p{page} 表格页 -->\n\n(.*?)(?=<!-- TABLE-PAGE:|<!-- page-anchor:|\Z)',
        re.DOTALL
    )
    m = pattern.search(content)
    if m:
        return m.group(1).strip()
    return ""

def get_previous_real_title(content, page):
    """向上查找最近的、不是'续上表'的表格标题"""
    pattern = re.compile(r'<!-- TABLE-PAGE: p(\d+) 表格页 -->\n\n(.*?)(?=<!-- TABLE-PAGE:|<!-- page-anchor:|\Z)', re.DOTALL)
    matches = list(pattern.finditer(content))
    for m in reversed(matches):
        p = int(m.group(1))
        if p > page:
            continue
        text = m.group(2).strip()
        lines = text.split('\n')
        for line in lines:
            ls = line.strip()
            if '表' in ls and '续上表' not in ls and len(ls) < 100 and len(ls) > 4:
                return ls
    return "(标题待确认)"

def get_ocr_raw_from_pages(page, vol, part):
    """从OCR raw页面文件读取原始文本"""
    # 页码偏移映射
    OFFSETS = {
        ("中", "part01"): (904, 1420),
        ("中", "part02"): (1421, 1971),
        ("下", "part01"): (1972, 2432),
        ("下", "part02"): (2433, 2911),
    }
    key = (vol, part)
    if key not in OFFSETS:
        return ""
    start, end = OFFSETS[key]
    if not (start <= page <= end):
        return ""
    local_page = page - start + 1
    
    raw_dir = ROOT / 'workbench' / 'ocr' / 'raw' / vol / part
    txt_path = raw_dir / f'page_{local_page:04d}.txt'
    if txt_path.exists():
        return txt_path.read_text(encoding='utf-8')
    return ""

def clean_table_title(title):
    """清理表格标题"""
    if not title:
        return ""
    title = re.sub(r'^\d+[\.、]\s*', '', title)
    # 移除"第X章"前缀
    title = re.sub(r'^第[一二三四五六七八九十]+章\s*', '', title)
    return title.strip()

def improve_title(tables, idx, content, vol, part):
    """改善标题：对于'续上表'类标题，向上查找真实表名"""
    t = tables[idx]
    if t['title'] in ('续上表', '') or '续上表' in t['title']:
        real_title = get_previous_real_title(content, t['page'])
        return real_title
    return t['title']

def main():
    tables = load_inventory()
    print(f"加载 {len(tables)} 个表格记录")
    
    # 按卷分组
    vol_tables = {}
    for t in tables:
        vol_tables.setdefault(t['vol'], []).append(t)
    
    for vol in ['中', '下']:
        vol_dir = ROOT / 'workbench' / 'table_entries' / vol
        data_dir = vol_dir / 'data'
        raw_dir = vol_dir / 'raw'
        scripts_dir = vol_dir / 'scripts'
        
        data_dir.mkdir(parents=True, exist_ok=True)
        raw_dir.mkdir(parents=True, exist_ok=True)
        scripts_dir.mkdir(parents=True, exist_ok=True)
        
        vtables = vol_tables.get(vol, [])
        print(f"\n{'='*60}")
        print(f"处理 {vol}册: {len(vtables)} 个表格")
        print(f"  目录: {vol_dir}")
        
        # 预加载正文内容
        body_content = ""
        if vol == "中":
            b1 = get_body_file_content("中", "part01", 0)
            b2 = get_body_file_content("中", "part02", 0)
            body_content = (b1 or "") + "\n" + (b2 or "")
        else:
            b1 = get_body_file_content("下", "part01", 0)
            b2 = get_body_file_content("下", "part02", 0)
            body_content = (b1 or "") + "\n" + (b2 or "")
        
        refined_funcs = {}  # 用于 refine_tables.py
        batch_entries = []  # 用于 batch_build_all.py
        
        for i, t in enumerate(vtables):
            tid = t['table_id']
            page = t['page']
            title = improve_title(tables, i, body_content, vol, t['part'])
            title_clean = clean_table_title(title)
            
            print(f"  [{i+1}/{len(vtables)}] {tid} (p{page}) — {title_clean[:60]}")
            
            # 1. 生成 JSON 骨架
            json_entry = {
                "table_id": tid,
                "title": title_clean,
                "table_number": "",
                "page": page,
                "pages": [page],
                "part": t['part'],
                "vol": vol,
                "columns": ["数值"],
                "rows": [["待对照原图录入"]],
                "row_count": 1,
                "col_count": 1,
                "status": "draft",
                "notes": f"从OCR自动提取骨架，待对照原图精修 (p{page})"
            }
            
            json_path = data_dir / f'{tid}.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_entry, f, ensure_ascii=False, indent=2)
            
            # 2. 提取 OCR raw 文本
            ocr_text = extract_ocr_context_for_table(body_content, page)
            raw_path = raw_dir / f'{tid}_{page}.txt'
            with open(raw_path, 'w', encoding='utf-8') as f:
                f.write(ocr_text)
            
            # 3. 为 refine_tables.py 准备 stub 函数(使用table_id去除了"LYG-"前缀)
            # func_name: Python合法标识符 (无连字符)
            # REFINERS key保持: LYG-中-Tnnn
            tid_short = tid.replace('LYG-', '')       # "中-T001"
            func_name = f"refine_{tid_short.replace('-', '_')}"  # "refine_中_T001"
            # 猜测列数：从OCR文本中尝试提取
            col_hint = 3 if vol == '中' and page > 1400 else 4  # 简单启发
            
            refined_funcs[tid] = {
                "func_name": func_name,
                "tid_short": tid_short,
                "title": title_clean,
                "page": page,
                "vol": vol,
                "part": t['part'],
                "col_hint": col_hint,
            }
            
            batch_entries.append(tid)
        
        # ===== 2. 生成 refine_tables.py =====
        refine_lines = [
            '#!/usr/bin/env python3',
            '# -*- coding: utf-8 -*-',
            '"""',
            f'表格数据精修脚本 — {vol}册 ({len(vtables)}个表格)',
            '使用方法: python refine_tables.py <table_id>',
            f'  例: python refine_tables.py LYG-{vol}-T001',
            '  不指定ID则处理所有表格',
            '"""',
            'import json, re, sys',
            'from pathlib import Path',
            '',
            f'ROOT = Path(r\'{ROOT.as_posix()}\')',
            f'DATA_DIR = ROOT / \'workbench\' / \'table_entries\' / \'{vol}\' / \'data\'',
            f'RAW_DIR = ROOT / \'workbench\' / \'table_entries\' / \'{vol}\' / \'raw\'',
            "sys.stdout.reconfigure(encoding='utf-8')",
            '',
            'def read_raw(table_id):',
            '    txt = sorted(RAW_DIR.glob(f\'{table_id}_*.txt\'))',
            "    return txt[0].read_text(encoding='utf-8') if txt else \"\"",
            '',
            'def read_json(table_id):',
            "    j = DATA_DIR / f'{table_id}.json'",
            "    return json.loads(j.read_text(encoding='utf-8')) if j.exists() else None",
            '',
            'def save_json(table_id, data):',
            "    j = DATA_DIR / f'{table_id}.json'",
            "    data['row_count'] = len(data['rows'])",
            "    data['col_count'] = len(data['columns'])",
            "    j.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')",
            '',
            '# ============================================================',
            '# 各表的精修函数',
            '# 返回: {columns, rows} 更新后的结构',
            f'# {vol}册 — {len(vtables)}个表格 (页码 {vtables[0]["page"]}~{vtables[-1]["page"]})',
            '# ============================================================',
            '',
        ]
        
        # 按页码排序生成stub函数
        sorted_funcs = sorted(refined_funcs.values(), key=lambda x: x['page'])
        for rf in sorted_funcs:
            refine_lines.append(f'')
            refine_lines.append(f'def {rf["func_name"]}(raw):')
            refine_lines.append(f'    """{rf["title"][:80]} (p{rf["page"]}, {rf["part"]})')
            refine_lines.append(f'    ⚠ OCR碎片化，需对照原图录入列定义与数据。"""')
            refine_lines.append(f'    return {{"columns": ["数值"],')
            refine_lines.append(f'            "rows": [["待对照原图录入"]]}}')
            refine_lines.append(f'')
        
        # REFINERS 调度表
        refine_lines.append('# ===== 调度表 =====')
        refine_lines.append('REFINERS = {')
        for rf in sorted_funcs:
            refine_lines.append(f'    "LYG-{rf["tid_short"]}": {rf["func_name"]},')
        refine_lines.append('}')
        refine_lines.append('')
        refine_lines.append('')
        refine_lines.append('def main():')
        refine_lines.append('    target = sys.argv[1] if len(sys.argv) > 1 else None')
        refine_lines.append('    refined = 0')
        refine_lines.append('')
        refine_lines.append('    for tid, refiner in REFINERS.items():')
        refine_lines.append('        if target and tid != target:')
        refine_lines.append('            continue')
        refine_lines.append('')
        refine_lines.append('        data = read_json(tid)')
        refine_lines.append('        if not data:')
        refine_lines.append('            print(f"  ! {tid} — JSON不存在")')
        refine_lines.append('            continue')
        refine_lines.append('')
        refine_lines.append('        raw = read_raw(tid)')
        refine_lines.append('        result = refiner(raw)')
        refine_lines.append('')
        refine_lines.append("        data['columns'] = result['columns']")
        refine_lines.append("        data['rows'] = result['rows']")
        refine_lines.append("        data['notes'] = data.get('notes', '').replace('从OCR自动提取骨架', '已精修')")
        refine_lines.append("        if '待对照原图精修' in data.get('notes', ''):")
        refine_lines.append("            data['notes'] = data['notes'].replace('待对照原图精修', '对照原图确认')")
        refine_lines.append('')
        refine_lines.append('        save_json(tid, data)')
        refine_lines.append('        rcount = len(result["rows"])')
        refine_lines.append('        ccount = len(result["columns"])')
        refine_lines.append('        filled = sum(1 for r in result["rows"] for c in r if c and c != "待对照原图录入")')
        refine_lines.append('        print(f"  ✓ {tid}: {rcount}行×{ccount}列 ({filled}个已填充)")')
        refine_lines.append('        refined += 1')
        refine_lines.append('')
        refine_lines.append('    if refined == 0:')
        refine_lines.append('        print("未处理任何表。支持的ID:")')
        refine_lines.append('        for k in REFINERS:')
        refine_lines.append('            print(f"  {k}")')
        refine_lines.append('    else:')
        refine_lines.append('        print(f"\\n精修完成: {refined}个")')
        refine_lines.append('')
        refine_lines.append("if __name__ == '__main__':")
        refine_lines.append('    main()')
        
        refine_path = vol_dir / 'refine_tables.py'
        with open(refine_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(refine_lines))
        print(f"  ✓ refine_tables.py ({len(sorted_funcs)} 个stub函数)")
        
        # ===== 3. 生成 batch_build_all.py =====
        batch_lines = [
            '#!/usr/bin/env python3',
            '# -*- coding: utf-8 -*-',
            '"""',
            f'批量构建{vol}册全部{len(batch_entries)}个表格JSON',
            f'- 从JSON数据构建',
            f'- 输出: data/LYG-{vol}-T*.json',
            '"""',
            'import json, sys',
            'from pathlib import Path',
            '',
            f'ROOT = Path(r\'{ROOT.as_posix()}\')',
            f'DATA_DIR = ROOT / \'workbench\' / \'table_entries\' / \'{vol}\' / \'data\'',
            "sys.stdout.reconfigure(encoding='utf-8')",
            '',
            "FINISHED = {}  # 已精修的表ID集合（逐步填充）",
            '',
            'def main():',
            '    DATA_DIR.mkdir(parents=True, exist_ok=True)',
            '    # 从 JSON 文件列表中发现所有表格',
            '    json_files = sorted(DATA_DIR.glob(f"LYG-*-T*.json"))',
            f'    print(f"发现 {{len(json_files)}} 个JSON文件")',
            '    for jf in json_files:',
            '        tid = jf.stem',
            '        data = json.loads(jf.read_text(encoding="utf-8"))',
            '        print(f"  ✓ {tid}: {data.get(\"title\",\"\")[:40]}  ({data[\"row_count\"]}行×{data[\"col_count\"]}列)")',
            '',
            "if __name__ == '__main__':",
            '    main()',
        ]
        
        batch_path = vol_dir / 'batch_build_all.py'
        with open(batch_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(batch_lines))
        print(f"  ✓ batch_build_all.py")
        
        # ===== 4. 统计 =====
        json_count = len(list(data_dir.glob('*.json')))
        raw_count = len(list(raw_dir.glob('*.txt')))
        print(f"  ✓ JSON骨架: {json_count} 个")
        print(f"  ✓ OCR raw: {raw_count} 个")

    # ===== 最终汇总 =====
    print(f"\n{'='*60}")
    print("生成完毕")
    print("=" * 60)
    for vol in ['中', '下']:
        vol_dir = ROOT / 'workbench' / 'table_entries' / vol
        json_count = len(list((vol_dir / 'data').glob('*.json')))
        raw_count = len(list((vol_dir / 'raw').glob('*.txt')))
        print(f"  {vol}册: {json_count} JSON + {raw_count} raw在 {vol_dir}")

if __name__ == '__main__':
    main()
