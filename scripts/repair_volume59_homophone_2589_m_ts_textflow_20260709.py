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
REPORT_JSON = ROOT / "output" / "reports" / "volume59_homophone_2589_m_ts_textflow_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_homophone_2589_m_ts_textflow_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷同音字汇2589页贸债行界修复.md"

SOURCE_OLD = "m\n①摸②谟模馒磨~刀魔摩摹~仿\nts\n①灾栽斋 ③宰载年~崽 ④在再载\n③亩母拇牡抹涂~④贸磨石~茂墓\n装~债寨瘵□~子：手脚上的鸡眼□钉：~\n暮慕募幕\n鞋，钉子：鞋~子□用清水冲洗：~碗"
SOURCE_NEW = "m\n①摸②谟模馒磨~刀魔摩摹~仿\n③亩母拇牡抹涂~④贸磨石~茂墓暮慕募幕\nts\n①灾栽斋 ③宰载年~崽 ④在再载装~债寨瘵□~子：手脚上的鸡眼□钉：~鞋，钉子：鞋~子□用清水冲洗：~碗"
HTML_OLD = "<p><span class=\"dialect-word-head\">m</span></p>\n<p>①摸②谟模馒磨~刀魔摩摹~仿</p>\n<p><span class=\"dialect-word-head\">ts</span></p>\n<p>①灾栽斋 ③宰载年~崽 ④在再载</p>\n<p>③亩母拇牡抹涂~④贸磨石~茂墓</p>\n<p>装~债寨瘵□~子：手脚上的鸡眼□钉：~</p>\n<p>暮慕募幕</p>\n<p>鞋，钉子：鞋~子□用清水冲洗：~碗</p>"
HTML_NEW = "<p><span class=\"dialect-word-head\">m</span></p>\n<p>①摸②谟模馒磨~刀魔摩摹~仿</p>\n<p>③亩母拇牡抹涂~④贸磨石~茂墓暮慕募幕</p>\n<p><span class=\"dialect-word-head\">ts</span></p>\n<p>①灾栽斋 ③宰载年~崽 ④在再载装~债寨瘵□~子：手脚上的鸡眼□钉：~鞋，钉子：鞋~子□用清水冲洗：~碗</p>"
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
        "repair": "将 `暮慕募幕` 归入 m 组，并将 `装~债...鞋~子...~碗` 合并到 ts 组。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 第五十九卷同音字汇2589页贸债行界修复",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第三章同音字汇，书页 2589。",
        "- 依据：OCR、源稿、全书汇总和阅读器均显示 `暮慕募幕` 被夹入 ts 组释义中；`装~债.../鞋，钉子...` 被 m 组行隔开。",
        "- 修复：`④贸磨石~茂墓暮慕募幕` 与 `④在再载装~债寨瘵...~鞋，钉子...~碗` 分别合并。",
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
