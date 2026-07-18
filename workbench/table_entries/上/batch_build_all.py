#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量构建全部44个表格JSON
- 保留已完成9表的精确数据
- 对剩余35表从raw TXT提取骨架数据
- 输出: data/LYG-上-T*.json
"""
import json, re, sys
from pathlib import Path

ROOT = Path(r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation')
SCRIPTS_DIR = ROOT / 'workbench' / 'table_entries' / '上' / 'scripts'
RAW_DIR = ROOT / 'workbench' / 'table_entries' / '上' / 'raw'
DATA_DIR = ROOT / 'workbench' / 'table_entries' / '上' / 'data'
sys.stdout.reconfigure(encoding='utf-8')

def read_ocr_ref(table_id):
    """从构建脚本中提取OCR_REF文本"""
    script_path = SCRIPTS_DIR / f'build_{table_id}.py'
    if not script_path.exists():
        return ""
    text = script_path.read_text(encoding='utf-8')
    # 提取 OCR_REF = """..."""
    m = re.search(r'OCR_REF\s*=\s*"""(.+?)"""', text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""

def read_raw_txt(table_id, page):
    """读取raw TXT"""
    candidates = sorted(RAW_DIR.glob(f'{table_id}_*.txt'))
    for f in candidates:
        return f.read_text(encoding='utf-8')
    return ""

def guess_columns_from_ocr(ocr_text, table_id):
    """从OCR文本中猜测列名"""
    lines = [l.strip() for l in ocr_text.split('\n') if l.strip()]
    # 对每个表使用预定义列
    predefined = {
        "T004": ["站年", "灾害性质", "发生日期", "年雨量", "最大日雨量", "高水位"],
        "T006": ["朝代", "建置沿革", "隶属", "辖区", "备注"],
        "T010": ["路名", "起讫点", "长度(m)", "宽度(m)", "结构", "年份"],
        "T011": ["年份", "计划取水量", "实际取水量", "节水量", "工业取水量", "重复利用率(%)"],
        "T012": ["路名", "光源", "盏数", "线路长度(m)", "架线方式", "线材"],
        "T014": ["年份", "交易件数", "面积(m²)", "金额(万元)"],
        "T015": ["年份", "废水总量", "工业废水", "生活污水", "COD", "SS"],
        "T017": ["考核项目", "1986", "1987", "1988", "1989", "1990"],
        "T018": ["年份", "GDP(万元)", "工农业总产值", "工业产值", "农业产值"],
        "T019": ["类别", "零售额(万元)"],
        "T020": ["产业", "1978", "1980", "1985", "1986", "1987", "1988", "1989", "1990"],
        "T021": ["部门", "投入(万元)", "产出(万元)", "1987", "1990"],
        "T022": ["年份", "企业数", "注册资金(万元)", "从业人数"],
        "T023": ["项目", "数值", "备注"],
        "T024": ["项目", "数值", "备注"],
        "T025": ["项目名称", "年份", "面积(亩)", "产量(kg/亩)", "新增产值"],
        "T026": ["年份", "面积(亩)", "产量(吨)"],
        "T027": ["建筑物名", "结构", "孔数", "设计流量", "修建年份"],
        "T028": ["水库名", "河流", "总库容", "兴利库容", "灌溉面积(万亩)"],
        "T029": ["河道名", "长度(km)", "流域面积(km²)"],
        "T030": ["指标", "数值"],
        "T031": ["品种", "分布", "储量(吨)", "年捕捞量"],
        "T032": ["品种", "1986", "1987", "1988", "1989", "1990"],
        "T033": ["企业", "所在地", "冷冻能力", "冷藏能力", "投产年份"],
        "T034": ["指标", "1985", "1990"],
        "T035": ["年份", "产量(万吨)", "面积(公顷)"],
        "T036": ["项目", "1985", "1986", "1987", "1988", "1989", "1990"],
        "T037": ["年份", "销量(万吨)", "省内", "省外"],
        "T038": ["项目", "数值"],
        "T039": ["企业", "产品", "产量", "产值"],
        "T040": ["年份", "产值(万元)", "企业数", "职工"],
        "T041": ["年份", "产量(吨)", "产值(万元)", "利税"],
        "T042": ["产品", "1985", "1986", "1987", "1988", "1989", "1990"],
        "T043": ["企业", "所在地", "职工", "主要产品", "产值", "利税"],
        "T044": ["企业", "所在地", "职工", "主要产品", "产值", "利税"],
    }
    tid_short = table_id.replace("LYG-上-", "")
    return predefined.get(tid_short, ["数值"])

def extract_rows_from_ocr(ocr_text, num_cols):
    """从OCR文本中提取可能的行数据"""
    lines = [l.strip() for l in ocr_text.split('\n') if l.strip()]
    # 过滤掉明显不是数据行的内容
    skip_words = ["续上表", "表", "第", "章", "节", "卷", "连云港市志", "页"]
    data_lines = []
    for l in lines:
        l_clean = re.sub(r'[·•◆◇]', '', l)
        if len(l_clean) < 2:
            continue
        if any(l.startswith(w) for w in skip_words):
            continue
        # 包含数字的短线更可能是数据
        if re.search(r'\d', l):
            data_lines.append(l)
    # 去重
    seen = set()
    unique = []
    for l in data_lines:
        if l not in seen:
            seen.add(l)
            unique.append(l)
    # 按列数分组
    if num_cols <= 1:
        return [[l] for l in unique[:50]]
    # 将每行作为单独数据项
    return [[l] for l in unique[:num_cols * 10]]

# ===== 已完成9表 =====
FINISHED = {
    "LYG-上-T001", "LYG-上-T002", "LYG-上-T003",
    "LYG-上-T005", "LYG-上-T007", "LYG-上-T008",
    "LYG-上-T009", "LYG-上-T013", "LYG-上-T016"
}

# ===== 表元数据（基于快速统计） =====
TABLE_META = {}
# 从脚本读取元数据
for i in range(1, 45):
    tid = f"LYG-上-T{i:03d}"
    script_path = SCRIPTS_DIR / f'build_{tid}.py'
    if script_path.exists():
        text = script_path.read_text(encoding='utf-8')
        # 提取PAGES
        m = re.search(r'PAGES\s*=\s*\[(.*?)\]', text)
        pages = []
        if m:
            pages = [int(x.strip()) for x in m.group(1).split(',') if x.strip()]
        # 提取TITLE
        m = re.search(r'TITLE\s*=\s*"""(.*?)"""', text, re.DOTALL)
        title = m.group(1).strip() if m else tid
        TABLE_META[tid] = {"title": title, "pages": pages}

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    built_count = 0
    
    for i in range(1, 45):
        tid = f"LYG-上-T{i:03d}"
        meta = TABLE_META.get(tid, {"title": tid, "pages": []})
        
        if tid in FINISHED:
            print(f"  ✓ {tid} — 已跳过（保留现有精确数据）")
            continue
        
        # 读取OCR参考文本
        ocr_text = read_ocr_ref(tid)
        raw_text = read_raw_txt(tid, meta.get("pages", [None])[0])
        if not ocr_text and raw_text:
            ocr_text = raw_text[:5000]
        
        # 猜测列
        columns = guess_columns_from_ocr(ocr_text, tid)
        
        # 提取行
        rows = extract_rows_from_ocr(ocr_text, len(columns))
        
        if not rows:
            # 空行
            rows = []
        
        entry = {
            "table_id": tid,
            "title": meta.get("title", ""),
            "table_number": "",
            "pages": meta.get("pages", []),
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "col_count": len(columns),
            "status": "draft",
            "notes": "从OCR自动提取骨架，待对照原图精修"
        }
        
        out_path = DATA_DIR / f"{tid}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ {tid} — {meta.get('title','')[:30]}  ({len(rows)}行×{len(columns)}列)")
        built_count += 1
    
    print(f"\n完成: 跳过9个已完成, 构建{built_count}个")
    print(f"数据目录: {DATA_DIR}")

if __name__ == '__main__':
    main()
