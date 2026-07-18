# -*- coding: utf-8 -*-
"""Remove two duplicated currency item titles in the final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_currency_duplicate_titles_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_currency_duplicate_titles_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_货币小节重复标题清理.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/连云港市志_全书_正文汇总.md:81145-81182"

REPLACEMENTS = [
    (
        "<p>一、铸钱一、铸钱始于商周，发展于春秋战国，统于秦始皇，以后各朝均有铸币。",
        "<p>一、铸钱始于商周，发展于春秋战国，统于秦始皇，以后各朝均有铸币。",
    ),
    (
        "<p>一、兑换券一、兑换券境内流通主要是清光绪三十一年（1905年）由户部银行发行的以银两为单位的户部官票、",
        "<p>一、兑换券境内流通主要是清光绪三十一年（1905年）由户部银行发行的以银两为单位的户部官票、",
    ),
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changed = 0
    cleaned = 0
    details = []
    for old, new in REPLACEMENTS:
        old_count = html.count(old)
        new_count = html.count(new)
        if old_count == 1:
            html = html.replace(old, new, 1)
            changed += 1
            cleaned += 1
            status = "changed"
        elif old_count == 0 and new_count >= 1:
            cleaned += 1
            status = "already_applied"
        else:
            raise RuntimeError(f"unexpected count for {old[:30]!r}: old={old_count}, new={new_count}")
        details.append({"old": old, "new": new, "status": status})

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "target": str(HTML.relative_to(ROOT)).replace("\\", "/"),
        "changed": changed,
        "targets_cleaned": cleaned,
        "source": SOURCE,
        "details": details,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    text = f"""# 货币小节重复标题清理

- 时间：{now}
- 范围：`{HTML.relative_to(ROOT)}`。
- 对象：金融卷货币章节 `一、铸钱`、`一、兑换券` 两处段首重复题名。
- 处理：据正文汇总确认源文标题单独成行，最终阅读版只删除重复的第二个题名，不改正文内容。
- 状态：目标清理 {cleaned}/2 处；本次运行变更 {changed} 处。
- 源证据：`{SOURCE}`。
"""
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 货币小节重复标题清理"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_currency_duplicate_titles_20260705.py`，清理最终阅读版金融卷货币章节 `一、铸钱一、铸钱...` 与 `一、兑换券一、兑换券...` 两处重复题名。
- 源证据：`{SOURCE}` 显示 `一、铸钱`、`一、兑换券` 为独立标题，正文分别从下一行起。
- 报告：`output/reports/reader_currency_duplicate_titles_20260705.md`。
""",
    )

    print("reader_currency_duplicate_titles_cleaned")
    print(f"changed={changed}")
    print(f"targets_cleaned={cleaned}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
