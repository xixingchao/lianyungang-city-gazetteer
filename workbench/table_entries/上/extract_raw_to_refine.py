#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取原始OCR文本，尝试提取结构化表格数据，输出精修函数代码片段
"""
import json, re, sys
from pathlib import Path

ROOT = Path(r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation')
RAW_DIR = ROOT / 'workbench' / 'table_entries' / '上' / 'raw'
DATA_DIR = ROOT / 'workbench' / 'table_entries' / '上' / 'data'

def read_raw(table_id):
    txt = sorted(RAW_DIR.glob(f'{table_id}_*.txt'))
    return txt[0].read_text(encoding='utf-8') if txt else ""

def read_json(table_id):
    j = DATA_DIR / f'{table_id}.json'
    return json.loads(j.read_text(encoding='utf-8')) if j.exists() else None

def show_raw_structure(table_id, lines=50):
    """显示原始文本的前N行，帮助理解结构"""
    raw = read_raw(table_id)
    vals = [l.strip() for l in raw.split('\n') if l.strip()]
    skip_headers = ['连云港市志', '续上表', '单位：', '表']
    vals = [v for v in vals if not any(v.startswith(h) for h in skip_headers)]
    print(f"\n=== {table_id} 前{min(lines, len(vals))}个非空值 ===")
    for i, v in enumerate(vals[:lines]):
        print(f"  {i:3d}: {v}")

def extract_year_values(vals):
    """从数值列表中提取(年份, 数字)对"""
    year_pat = re.compile(r'^(19\d\d|20\d\d|\d{4})$')
    years = []
    for i, v in enumerate(vals):
        if year_pat.match(str(v).strip()):
            years.append((i, v))
    return years

def analyze_T018(raw):
    """分析T018工农业总产值及构成表"""
    vals = [l.strip() for l in raw.split('\n') if l.strip()]
    # 过滤掉非数据行
    skip_words = ['连云港市志', '续上表', '单位：', '表', '第一章', '经济发展', '注：', '1978~', '国民收入', 
                  '国内生产总值', '社会总产值', '其中', '万元', '农业', '工业', '建筑业', '商业', '（比重']
    data_vals = [v for v in vals if not any(v.startswith(w) for w in skip_words) 
                 and not v.startswith('一、') and not v.startswith('二、') and not v.startswith('三、')
                 and v not in ['', '年份', '总产值', '工业总产值', '农业总产值', '成（%)']]
    
    # 找年份位置
    year_positions = []
    for i, v in enumerate(data_vals):
        if re.match(r'^(19\d\d)$', v):
            year_positions.append((i, int(v)))
    
    print(f"\n=== T018 数据值数量: {len(data_vals)}, 年份数: {len(year_positions)} ===")
    print(f"年份: {[y for _, y in year_positions]}")
    
    # 尝试提取每个年份周围的数据
    for idx, (pos, year) in enumerate(year_positions):
        # 取年份前6个和后2个值
        start = max(0, pos - 6)
        end = min(len(data_vals), pos + 3)
        context = data_vals[start:end]
        print(f"\n年份 {year} (data_idx={pos}), 周围={context}")

def analyze_T020(raw):
    """分析T020产业结构表"""
    vals = [l.strip() for l in raw.split('\n') if l.strip()]
    skip_words = ['连云港市志', '增', '第二产业', '第三产业', '第一产业', '国内生', '构', '1978~',
                  '产总值', '总值', '占比重', '（万元）', '(%)', '万元']
    data_vals = [v for v in vals if not any(v.startswith(w) for w in skip_words)
                 and v not in ['', '年份', '表']]
    
    year_positions = []
    for i, v in enumerate(data_vals):
        if re.match(r'^(19\d\d)$', v):
            year_positions.append((i, int(v)))
    
    print(f"\n=== T020 数据值数量: {len(data_vals)}, 年份数: {len(year_positions)} ===")
    for idx, (pos, year) in enumerate(year_positions):
        start = max(0, pos - 8)
        end = min(len(data_vals), pos + 3)
        context = data_vals[start:end]
        print(f"年份 {year} (idx={pos}), 周围={context}")


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'T017'
    table_id = f'LYG-上-{target}'
    raw = read_raw(table_id)
    
    if not raw:
        print(f"未找到 {table_id} 的原始文本")
        sys.exit(1)
    
    print(f"=== {table_id} 原始文本长度: {len(raw)} 字符 ===")
    
    if target == 'T017':
        show_raw_structure(table_id, 60)
    elif target == 'T018':
        analyze_T018(raw)
    elif target == 'T020':
        analyze_T020(raw)
    elif target == 'T043':
        show_raw_structure(table_id, 80)
    elif target == 'T044':
        show_raw_structure(table_id, 100)
    else:
        show_raw_structure(table_id, 40)
