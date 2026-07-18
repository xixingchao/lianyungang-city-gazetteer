#!/usr/bin/env python3
"""扫描上册各文件的 A/B/C 类格式问题"""
import re, os, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

body_dir = os.path.join(os.path.dirname(__file__), '..', 'workbench', 'body_chapters', '上')
files = sorted(glob.glob(os.path.join(body_dir, '*.md')))

for fp in files:
    if '汇总' in fp:
        continue
    basename = os.path.basename(fp)
    with open(fp, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f'=== {basename} ===')

    # A. 标题缺少空格
    # 第X卷 + 非空格中文 或 第X章 + 非空格中文 或 第X节 + 非空格中文
    a_issues = []
    for i, line in enumerate(lines, 1):
        s = line.strip()
        # 匹配 "第一章建置" "第一节地质" 等
        m = re.search(r'(第[一二三四五六七八九十\d]+)([卷章节])([^\s])', s)
        if m and not s.startswith('#'):
            # 排除已经是正确格式的 "第X卷 " 或 "第X章 "
            # 捕获: 如 "第一章建置" → "第一章 建置"
            a_issues.append((i, s[:60]))
    if a_issues:
        print(f'  A. 标题缺少空格: {len(a_issues)}处')
        for ln, txt in a_issues[:10]:
            print(f'    L{ln}: {txt}')
        if len(a_issues) > 10:
            print(f'    ... 还有{len(a_issues)-10}处')
    else:
        print(f'  A. 标题缺少空格: 无')

    # B. OCR残留错字
    b_issues = []
    for i, line in enumerate(lines, 1):
        s = line
        if '两干' in s:
            b_issues.append((i, '两干→两千', s.strip()[:80]))
        if '戊成' in s:
            b_issues.append((i, '戊成→戊戌', s.strip()[:80]))
        if '车业' in s or '农车' in s:
            b_issues.append((i, '农車业→农副业', s.strip()[:80]))
        if '盲自' in s:
            b_issues.append((i, '盲自→盲目', s.strip()[:80]))
        if '稀蔬' in s or '人口蔬' in s:
            b_issues.append((i, '稀蔬→稀疏', s.strip()[:80]))
    if b_issues:
        print(f'  B. OCR残留错字: {len(b_issues)}处')
        for ln, kind, txt in b_issues:
            print(f'    L{ln} [{kind}]: {txt}')
    else:
        print(f'  B. OCR残留错字: 无')

    # C. 正文重复卷标题 - 检查 "第X卷" 在正文中重复出现
    # 跳过第一行（# 第X卷 ... markdown标题）
    c_issues = []
    for i, line in enumerate(lines, 2):  # 从第2行开始
        s = line.strip()
        if re.match(r'^第[一二三四五六七八九十\d]+卷$', s) and len(s) <= 10:
            c_issues.append((i, s))
    if c_issues:
        print(f'  C. 正文重复卷标题: {len(c_issues)}处')
        for ln, txt in c_issues:
            print(f'    L{ln}: {txt}')
    else:
        print(f'  C. 正文重复卷标题: 无')

    print()
