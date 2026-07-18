from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
OLD = "\n三、声\n调(5)\n调类代码"
NEW = "\n三、声调(5)\n调类代码"
REPORT_JSON = ROOT / "output" / "reports" / "volume59_tone_heading_source_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_tone_heading_source_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷声调标题源稿断行修复.md"


def main() -> None:
    changes = []
    for path in PATHS:
        text = path.read_text(encoding="utf-8")
        count = text.count(OLD)
        if count != 1:
            raise RuntimeError(f"{path} expected 1 match, got {count}")
        path.write_text(text.replace(OLD, NEW, 1), encoding="utf-8", newline="\n")
        changes.append({"path": str(path.relative_to(ROOT)), "old": "三、声 / 调(5)", "new": "三、声调(5)", "count": count})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"generated_at": now, "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 第五十九卷声调标题源稿断行修复",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷方言第二章语音系统 `三、声调(5)` 标题。",
        "- 依据：OCR `workbench/ocr/paddle_ocr/下/part02/page_0301.txt` 中标题为 `三、声`/`调(5)` 断行，现行阅读器已规范为 `三、声调(5)`；本批同步修复现行源稿。",
        "- 说明：不改声调表内容、音标、调值和阅读器 HTML。",
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
