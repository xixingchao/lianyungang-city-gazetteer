#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从OCR文本中解析T018工农业总产值及构成表数据"""
import re
from pathlib import Path

RAW_DIR = Path(r'e:\codex_Learing\09_project_东辛农场\连云港市志_workstation\workbench\table_entries\上\raw')
raw = sorted(RAW_DIR.glob('LYG-上-T018_*.txt'))[0].read_text(encoding='utf-8')

lines = [l.strip() for l in raw.split('\n')]

# 找到所有数字和年份
tokens = []
for l in lines:
    if not l or l.startswith('连云港市志') or l.startswith('续上表') or l.startswith('第一章'):
        continue
    tokens.append(l)

# 提取所有数字和年份
nums = []
for t in tokens:
    t_clean = t.replace(',', '').replace('，', '').strip()
    # 尝试匹配数字（整数或浮点数）
    m = re.match(r'^(\d+(?:\.\d+)?)$', t_clean)
    if m:
        nums.append(m.group(1))
    elif re.match(r'^(19\d\d)$', t):
        nums.append(t)

# 按年份分组
year_data = {}
for i, n in enumerate(nums):
    if re.match(r'^(19\d\d)$', n):
        year = int(n)
        # 取年份前后的值
        start = max(0, i-6)
        end = min(len(nums), i+4)
        context = nums[start:end]
        year_data[year] = context

# 解析每个年份的数据
# 表结构: 年份, 总产值(万元), 工业总产值(万元), 农业总产值(万元), 工业占比(%), 农业占比(%)
for year in sorted([y for y in year_data.keys() if 1940 <= y <= 1990]):
    ctx = year_data[year]
    print(f"{year}: {ctx}")
