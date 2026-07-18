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
REPORT_JSON = ROOT / "output" / "reports" / "volume59_homophone_2587_textflow_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_homophone_2587_textflow_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷同音字汇2587页行界修复.md"

SOURCE_OLD = "t ①低提~溜：拎 ③底抵砥柢邸 ④帝\nt ①都首~尿□长时间煮：~豆腐 ②嘟拟声\n缔蒂弟递第地\n词③堵赌睹肚胃 ④度渡镀妒杜肚"
SOURCE_NEW = "t ①低提~溜：拎 ③底抵砥柢邸 ④帝缔蒂弟递第地\nt ①都首~尿□长时间煮：~豆腐 ②嘟拟声词③堵赌睹肚胃 ④度渡镀妒杜肚"
HTML_OLD = "<p>t ①低提~溜：拎 ③底抵砥柢邸 ④帝</p>\n<p>t ①都首~尿□长时间煮：~豆腐 ②嘟拟声</p>\n<p>缔蒂弟递第地</p>\n<p>词③堵赌睹肚胃 ④度渡镀妒杜肚</p>"
HTML_NEW = "<p>t ①低提~溜：拎 ③底抵砥柢邸 ④帝缔蒂弟递第地</p>\n<p>t ①都首~尿□长时间煮：~豆腐 ②嘟拟声词③堵赌睹肚胃 ④度渡镀妒杜肚</p>"
OCR_EVIDENCE = ["workbench/ocr/paddle_ocr/下/part02/page_0303.txt"]
IMAGE_EVIDENCE = ["workbench/conversion/page_images/下/part02/page_0303_180dpi.jpg"]


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
        "book_pages": [2587],
        "ocr_evidence": OCR_EVIDENCE,
        "image_evidence": IMAGE_EVIDENCE,
        "changes": changes,
        "repair": "将 `缔蒂弟递第地` 归入上一行 `④帝...`，并将 `嘟拟声/词` 合并为 `嘟拟声词`。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 第五十九卷同音字汇2587页行界修复",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第三章同音字汇，书页 2587。",
        "- 依据：OCR、源稿、全书汇总和阅读器均显示 `缔蒂弟递第地` 被夹在 `嘟拟声/词` 中间；按同音字组逻辑应归入上一行 `④帝`，同时 `拟声词` 应闭合。",
        "- 修复：`④帝 / ...嘟拟声 / 缔蒂弟递第地 / 词③堵...` -> `④帝缔蒂弟递第地`、`②嘟拟声词③堵...`。",
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
