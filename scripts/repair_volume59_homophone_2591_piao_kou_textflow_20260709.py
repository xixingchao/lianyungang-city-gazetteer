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
REPORT_JSON = ROOT / "output" / "reports" / "volume59_homophone_2591_piao_kou_textflow_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_homophone_2591_piao_kou_textflow_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷同音字汇2591页膘扣行界修复.md"

SOURCE_OLD = "p ①标膘长~镖骠彪飙瞟盯：~着他,别让跑了③表裱婊④標鳔膘油发过的猪皮：\nk①扣纽~抠~出来眍②□凶、厉害：这人\n吃~汤\n太~③口 ④叩扣~押寇蔻豆~"
SOURCE_NEW = "p ①标膘长~镖骠彪飙瞟盯：~着他,别让跑了③表裱婊④標鳔膘油发过的猪皮：吃~汤\nk①扣纽~抠~出来眍②□凶、厉害：这人太~③口 ④叩扣~押寇蔻豆~"
HTML_OLD = "<p>p ①标膘长~镖骠彪飙瞟盯：~着他,别让跑了③表裱婊④標鳔膘油发过的猪皮：</p>\n<p>k①扣纽~抠~出来眍②□凶、厉害：这人</p>\n<p>吃~汤</p>\n<p>太~③口 ④叩扣~押寇蔻豆~</p>"
HTML_NEW = "<p>p ①标膘长~镖骠彪飙瞟盯：~着他,别让跑了③表裱婊④標鳔膘油发过的猪皮：吃~汤</p>\n<p>k①扣纽~抠~出来眍②□凶、厉害：这人太~③口 ④叩扣~押寇蔻豆~</p>"
OCR_EVIDENCE = ["workbench/ocr/paddle_ocr/下/part02/page_0307.txt"]
IMAGE_EVIDENCE = ["workbench/conversion/page_images/下/part02/page_0307_180dpi.jpg"]


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
        "book_pages": [2591],
        "ocr_evidence": OCR_EVIDENCE,
        "image_evidence": IMAGE_EVIDENCE,
        "changes": changes,
        "repair": "将 `吃~汤` 归入膘释义，并将 `太~` 归入扣组释义。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 第五十九卷同音字汇2591页膘扣行界修复",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第三章同音字汇，书页 2591。",
        "- 依据：OCR、源稿、全书汇总和阅读器均显示 `吃~汤` 被夹在 `k` 组中，`太~` 与 `这人` 被断开；两处释义可闭合。",
        "- 修复：`膘油发过的猪皮：吃~汤` 与 `这人太~` 分别合并。",
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
