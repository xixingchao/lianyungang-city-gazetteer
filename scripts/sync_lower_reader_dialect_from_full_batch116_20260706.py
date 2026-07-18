# -*- coding: utf-8 -*-
"""Sync repaired 第五十九卷方言 block from full reader to lower-volume reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
LOWER = ROOT / "output" / "final_reader" / "连云港市志_下册.html"
REPORT_JSON = ROOT / "output" / "reports" / "lower_reader_dialect_sync_batch116_20260706.json"
REPORT_MD = ROOT / "output" / "reports" / "lower_reader_dialect_sync_batch116_20260706.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260706_下册方言卷同步全书结构化修复第一百一十六批.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

FULL_START = '<h2 id="第五十九卷-方言">第五十九卷方言</h2>'
FULL_END = '<h2 id="第六十卷-人物">第六十卷人物</h2>'
LOWER_START = '<h2 id="第五十九卷-概-述">第五十九卷 概·述</h2>'
LOWER_END = '<h2 id="第六十卷">第六十卷</h2>'

STYLE = """
.dialect-phonology-table{width:100%;border-collapse:collapse;margin:10px 0 12px;font-size:10pt;line-height:1.55;font-family:SimSun,"Noto Serif SC",serif}
.dialect-phonology-table caption{font-weight:600;text-align:left;margin-bottom:4px}
.dialect-phonology-table th{background:#f1f4f7;border:1px solid #c9c9c9;padding:4px 8px;text-align:left;white-space:nowrap}
.dialect-phonology-table td{border:1px solid #c9c9c9;padding:4px 8px;vertical-align:top;word-break:break-word}
.dialect-word-list{margin:8px 0 14px;font-size:10pt;line-height:1.7;font-family:SimSun,"Noto Serif SC",serif}
.dialect-word-list p{margin:3px 0;text-indent:0}
.dialect-word-head{font-weight:600;margin-right:0.5em}
""".strip()

REQUIRED = [
    '<h5>一、声母(18)</h5>',
    '<caption>声母(18)</caption>',
    '<h5>二、韵母(40)</h5>',
    '<caption>韵母(40)</caption>',
    '<h5>三、声调(5)</h5>',
    '<caption>声调(5)</caption>',
    '<div class="dialect-word-list dialect-homophone-full">',
    '<table class="dialect-phonology-table"><caption>表59-1 新浦话两字组连读变调表</caption>',
    '<table class="dialect-phonology-table"><caption>表59-2 新浦话声韵配合关系表</caption>',
]

OLD_MARKERS = [
    '第五十九卷 概·述',
    '第二章\n语音系统',
    '一、声\n母(18)',
    '二、韵\n母(40)',
    '三、声\n调(5)',
    '第三章 同音字汇·2587·',
]


def between(text: str, start: str, end: str) -> tuple[int, int, str]:
    a = text.index(start)
    b = text.index(end, a)
    return a, b, text[a:b]


def ensure_style(html: str) -> tuple[str, bool]:
    if '.dialect-phonology-table' in html and '.dialect-word-list' in html:
        return html, False
    if '</style>' not in html:
        raise RuntimeError('lower reader style block not found')
    return html.replace('</style>', STYLE + '\n</style>', 1), True


def upsert_memory(content: str) -> None:
    marker = '## 2026-07-06 第一百一十六批：下册方言卷同步全书结构化修复'
    old = MEMORY.read_text(encoding='utf-8') if MEMORY.exists() else ''
    if marker in old:
        start = old.index(marker)
        next_start = old.find('\n## ', start + 1)
        new = old[:start].rstrip() + '\n\n' + content.strip() + '\n'
        if next_start != -1:
            new += '\n' + old[next_start:].lstrip()
        MEMORY.write_text(new, encoding='utf-8')
    else:
        MEMORY.write_text(old.rstrip() + '\n\n' + content.strip() + '\n', encoding='utf-8')


def main() -> None:
    full = FULL.read_text(encoding='utf-8')
    lower = LOWER.read_text(encoding='utf-8')
    _, _, repaired = between(full, FULL_START, FULL_END)
    if LOWER_START in lower:
        start, end, old_block = between(lower, LOWER_START, LOWER_END)
    elif FULL_START in lower:
        start, end, old_block = between(lower, FULL_START, LOWER_END)
    else:
        raise RuntimeError('cannot locate lower-reader 第五十九卷方言 range')

    missing_in_source = [item for item in REQUIRED if item not in repaired]
    if missing_in_source:
        raise RuntimeError(f'full reader repaired dialect block missing markers: {missing_in_source}')

    lower, style_added = ensure_style(lower)
    start_marker = LOWER_START if LOWER_START in lower else FULL_START
    start = lower.index(start_marker)
    end = lower.index(LOWER_END, start)
    changed = lower[start:end] != repaired
    if changed:
        lower = lower[:start] + repaired + lower[end:]
        LOWER.write_text(lower, encoding='utf-8')

    new_block = lower[lower.index(FULL_START):lower.index(LOWER_END, lower.index(FULL_START))]
    missing_after = [item for item in REQUIRED if item not in new_block]
    old_after = [item for item in OLD_MARKERS if item in new_block]
    if missing_after or old_after:
        raise RuntimeError(f'lower dialect sync verification failed: missing={missing_after}; old={old_after}')

    payload = {
        'generated_at': datetime.now().isoformat(timespec='seconds'),
        'changed': changed,
        'style_added': style_added,
        'old_block_bytes': len(old_block.encode('utf-8')),
        'new_block_bytes': len(repaired.encode('utf-8')),
        'source': str(FULL),
        'target': str(LOWER),
        'required_markers': len(REQUIRED),
        'principle': 'Use the already repaired full-reader 第五十九卷方言 block as the source of truth for the lower split reader; do not rewrite OCR content by guesswork.',
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    md = f"""# 下册第五十九卷方言同步全书结构化修复第一百一十六批

> 生成时间：{now}

## 范围

- 源：`output/final_reader/连云港市志_全书.html` 中已修复的 `第五十九卷方言` 块。
- 目标：`output/final_reader/连云港市志_下册.html` 中旧的 `第五十九卷 概·述` 到 `第六十卷` 之前块。

## 处理

- 将下册旧方言卷整体替换为全书版已结构化方言卷。
- 同步方言声韵表和同音字汇块所需 CSS。
- 不凭图片或常识重录同音字汇内容；本批只解决分册读者未同步全书修复的问题。

## 结果

- 文件发生改写：{changed}
- 新增样式：{style_added}
- 旧块字节：{payload['old_block_bytes']}
- 新块字节：{payload['new_block_bytes']}
- 必要结构标记核验：{payload['required_markers']} 项全通过

## 证据

- 全书版已有结构化声母、韵母、声调表：`output/final_reader/连云港市志_全书.html`
- 下册旧块存在 `第五十九卷 概·述`、标题断裂和线性化方言表；本批替换后不再存在于第五十九卷范围内。
"""
    REPORT_MD.write_text(md, encoding='utf-8')
    PROGRESS.write_text(md, encoding='utf-8')

    upsert_memory(f"""
## 2026-07-06 第一百一十六批：下册方言卷同步全书结构化修复

- 新增脚本：`scripts/sync_lower_reader_dialect_from_full_batch116_20260706.py`。
- 将 `output/final_reader/连云港市志_下册.html` 的旧 `第五十九卷 概·述` 方言卷块，同步为 `output/final_reader/连云港市志_全书.html` 中已结构化的 `第五十九卷方言` 块。
- 解决用户粘贴的方言声母/韵母/同音字汇线性化问题在下册分册读者仍残留的问题；全书版原已结构化，本批不改全书版。
- 报告：`output/reports/lower_reader_dialect_sync_batch116_20260706.md`。未展示、未嵌入图片。
""")
    print(json.dumps({'changed': changed, 'style_added': style_added, 'report': str(REPORT_MD)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
