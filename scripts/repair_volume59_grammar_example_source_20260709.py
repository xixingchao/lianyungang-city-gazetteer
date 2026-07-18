from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = [
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
REPORT_JSON = ROOT / "output" / "reports" / "volume59_grammar_example_source_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_grammar_example_source_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷语法特点2623至2625页核对.md"

OLD = "噎人：饼子太干，~怕人：天乌黑的，好~"
NEW = "噎人：饼子太干，~\n怕人：天乌黑的，好~"
OCR_EVIDENCE = [
    "workbench/ocr/paddle_ocr/下/part02/page_0339.txt",
    "workbench/ocr/paddle_ocr/下/part02/page_0341.txt",
]
IMAGE_EVIDENCE = [
    "workbench/conversion/page_images/下/part02/page_0339_180dpi.jpg",
    "workbench/conversion/page_images/下/part02/page_0341_180dpi.jpg",
]


def replace_exact(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(f"{path} expected 1 match, got {count}")
    path.write_text(text.replace(OLD, NEW, 1), encoding="utf-8", newline="\n")
    return {"path": str(path.relative_to(ROOT)), "count": count}


def main() -> None:
    changes = [replace_exact(path) for path in SOURCE_PATHS]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "generated_at": now,
        "book_pages": [2623, 2625],
        "ocr_evidence": OCR_EVIDENCE,
        "image_evidence": IMAGE_EVIDENCE,
        "changes": changes,
        "html_note": "output/final_reader/连云港市志_全书.html 已将 `噎人`、`怕人` 渲染为两个列表项，本批只同步源稿和全书正文汇总。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 第五十九卷语法特点2623至2625页核对",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第五章语法特点，书页 2623、2625。",
        "- 结论：第五章至第六十卷边界清楚，阅读器例句列表已正确拆分；源稿和全书汇总仍有一处例句粘连，已同步修复。",
        "- 修复：`噎人：饼子太干，~怕人：天乌黑的，好~` -> `噎人：饼子太干，~` 与 `怕人：天乌黑的，好~` 两行。",
        "",
        "## 证据路径",
        "",
    ]
    for path in OCR_EVIDENCE:
        lines.append(f"- OCR：`{path}`")
    for path in IMAGE_EVIDENCE:
        lines.append(f"- 本地页图：`{path}`")
    lines.extend(["", "## 改写文件", "", "| 文件 | 命中 |", "|---|---:|"])
    for change in changes:
        lines.append(f"| `{change['path']}` | {change['count']} |")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS_MD.write_text(text, encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
