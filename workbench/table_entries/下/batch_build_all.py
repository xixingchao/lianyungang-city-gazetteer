#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下册表格批量构建工具
用法: python batch_build_all.py                  # 构建全部
      python batch_build_all.py LYG-下-T001   # 构建单个
"""
import json, sys
from pathlib import Path

ROOT = Path(r'e:/codex_Learing/09_project_东辛农场/连云港市志_workstation')
DATA_DIR = ROOT / 'workbench' / 'table_entries' / '下' / 'data'
sys.stdout.reconfigure(encoding='utf-8')

def build_table(tid):
    json_path = DATA_DIR / f'{tid}.json'
    if not json_path.exists():
        print(f'  ! {tid} — JSON文件不存在')
        return False
    data = json.loads(json_path.read_text(encoding='utf-8'))
    filled = sum(1 for r in data['rows'] for c in r if c and c != '待对照原图录入')
    total_cells = data['row_count'] * data['col_count']
    print(f'  {tid}: ' + data['title'][:50] + f'  {data["row_count"]}行x{data["col_count"]}列  ({filled}/{total_cells}格已填充)')
    return True

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    json_files = sorted(DATA_DIR.glob('LYG-下-T*.json'))
    print(f'下册 共 {len(json_files)} 个表格')
    ok = 0
    for jf in json_files:
        tid = jf.stem
        if target and tid != target:
            continue
        if build_table(tid):
            ok += 1
    print(f'\n完成: {ok}个')

if __name__ == '__main__':
    main()
