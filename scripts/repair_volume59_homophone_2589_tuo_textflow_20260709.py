from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = [
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "volume59_homophone_2589_tuo_textflow_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_homophone_2589_tuo_textflow_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷同音字汇2589页唾字行界修复.md"

SOURCE_OLD = "t ①施 ②驮坨砣驼佗陀 ③妥椭\ns\n①腮鳃筛塞~入 ④晒赛塞边~\n④唾"
SOURCE_NEW = "t ①施 ②驮坨砣驼佗陀 ③妥椭 ④唾\ns\n①腮鳃筛塞~入 ④晒赛塞边~"
HTML_OLD = "<p>t ①施 ②驮坨砣驼佗陀 ③妥椭</p>\n<p><span class=\"dialect-word-head\">s</span></p>\n<p>①腮鳃筛塞~入 ④晒赛塞边~</p>\n<p>④唾</p>"
HTML_NEW = "<p>t ①施 ②驮坨砣驼佗陀 ③妥椭 ④唾</p>\n<p><span class=\"dialect-word-head\">s</span></p>\n<p>①腮鳃筛塞~入 ④晒赛塞边~</p>"
OCR_EVIDENCE = ["workbench/ocr/paddle_ocr/下/part02/page_0305.txt"]
IMAGE_EVIDENCE = ["workbench/conversion/page_images/下/part02/page_0305_180dpi.jpg"]


def replace_exact(path: Path, old: str, new: str) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path} expected 1 match, got {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    return {"path": str(path.relative_to(ROOT)), "count": count}


def main() -> None:
    changes = [replace_exact(path, SOURCE_OLD, SOURCE_NEW) for path in SOURCE_PATHS]
    changes.append(replace_exact(HTML, HTML_OLD, HTML_NEW))
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "generated_at": now,
        "book_pages": [2589],
        "ocr_evidence": OCR_EVIDENCE,
        "image_evidence": IMAGE_EVIDENCE,
        "changes": changes,
        "repair": "将孤立 `④唾` 归入上一行 `t ①施...③妥椭`。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 第五十九卷同音字汇2589页唾字行界修复",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第三章同音字汇，书页 2589。",
        "- 依据：OCR、源稿、全书汇总和阅读器均显示 `④唾` 被 `s` 组隔开；按同音字组逻辑应归入上一行 `t ①施...③妥椭`。",
        "- 修复：`t ①施 ②驮坨砣驼佗陀 ③妥椭 ④唾`。",
        "- 说明：不改音标、不改字表，只恢复高置信行界。",
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
