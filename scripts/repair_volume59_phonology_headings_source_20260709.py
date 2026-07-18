from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPLACEMENTS = [
    ("\n一、声\n母(18)\n", "\n一、声母(18)\n"),
    ("\n二、韵\n母(40)\n", "\n二、韵母(40)\n"),
]
REPORT_JSON = ROOT / "output" / "reports" / "volume59_phonology_headings_source_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_phonology_headings_source_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷声韵调标题源稿断行修复.md"


def main() -> None:
    changes = []
    for path in PATHS:
        text = path.read_text(encoding="utf-8")
        for old, new in REPLACEMENTS:
            count = text.count(old)
            if count != 1:
                raise RuntimeError(f"{path} expected 1 match for {old!r}, got {count}")
            text = text.replace(old, new, 1)
            changes.append({"path": str(path.relative_to(ROOT)), "old": old.strip().replace("\n", " / "), "new": new.strip(), "count": count})
        path.write_text(text, encoding="utf-8", newline="\n")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"generated_at": now, "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 第五十九卷声韵调标题源稿断行修复",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷方言第二章语音系统第一节声韵调。",
        "- 动作：同步修复现行源稿中 `一、声母(18)`、`二、韵母(40)` 标题断行。",
        "- 说明：阅读器 HTML 已正确表格化，本批不改表格内容、音标、例字和阅读器 HTML。",
        "",
        "## 改写清单",
        "",
        "| 文件 | 原文 | 新文 |",
        "|---|---|---|",
    ]
    for c in changes:
        lines.append(f"| `{c['path']}` | `{c['old']}` | `{c['new']}` |")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS_MD.write_text(text, encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
