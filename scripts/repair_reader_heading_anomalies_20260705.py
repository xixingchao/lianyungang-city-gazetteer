# -*- coding: utf-8 -*-
"""Repair high-confidence heading anomalies in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_MD = ROOT / "output" / "reports" / "reader_heading_anomalies_20260705.md"
REPORT_JSON = ROOT / "output" / "reports" / "reader_heading_anomalies_20260705.json"

OLD = '<h5>、出席山东省各界人民代表会议代表名单</h5>'
NEW = '<h5>一、出席山东省各界人民代表会议代表名单</h5>'


def main() -> None:
    html = HTML.read_text(encoding='utf-8')
    count = html.count(OLD)
    if count != 1:
        raise RuntimeError(f'expected one heading anomaly, got {count}')
    html = html.replace(OLD, NEW, 1)
    HTML.write_text(html, encoding='utf-8')

    payload = {
        'generated_at': datetime.now().isoformat(timespec='seconds'),
        'reader': str(HTML.relative_to(ROOT)).replace('\\', '/'),
        'changes': [{'old': OLD, 'new': NEW}],
        'sources': [
            'output/final_reader/连云港市志_全书.html around 附42-2',
            'workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32781-32784',
        ],
        'note': '源文/OCR 漏“一”作顿号；同组后续标题为“二、出席江苏省协商委员会委员名单”，语义和序号均支持修为“一、”。',
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    REPORT_MD.write_text('\n'.join([
        '# 标题异常修复',
        '',
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        '',
        '## 修复项',
        '',
        '- `附42-2：出席省各界代表会议代表、省协商委员会代表名单` 下，标题 `、出席山东省各界人民代表会议代表名单` 修为 `一、出席山东省各界人民代表会议代表名单`。',
        '- 判断依据：同组下一标题为 `二、出席江苏省协商委员会委员名单`，该处为序号漏识，不改名单正文。',
        '',
        '## 源证据',
        '',
        '- `workbench/body_chapters/第三十卷至第四十二卷（中part02）.md:32781-32784`',
        '- 当前主阅读版 `附42-2` 上下文。',
        '',
    ]) + '\n', encoding='utf-8')
    print(f'changed=1')
    print(f'report={REPORT_MD}')


if __name__ == '__main__':
    main()
