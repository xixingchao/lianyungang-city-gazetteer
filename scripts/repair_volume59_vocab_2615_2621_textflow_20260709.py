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
REPORT_JSON = ROOT / "output" / "reports" / "volume59_vocab_2615_2621_textflow_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_vocab_2615_2621_textflow_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷方言词汇2615至2621页核对.md"

SOURCE_REPLACEMENTS = [
    {
        "name": "趁与复三释义串栏",
        "old": "各种 ka13 ton41\neə\n趁kə13一只脚跳动：右脚破了，只好\n复三 fua13 §313\n~着走\n出殡三天之日给坟\n髁头子 kə13 təu35 tl 膝盖\n填土\n咳嗽痨",
        "new": "各种 ka13 ton41\neə\n趁kə13一只脚跳动：右脚破了，只好~着走\n复三 fua13 §313 出殡三天之日给坟填土\n髁头子 kə13 təu35 tl 膝盖\n咳嗽痨",
        "evidence": "书页 2621 OCR/源稿/HTML 均显示 `趁` 释义被 `复三` 打断，`复三` 释义又被 `髁头子` 打断；`只好~着走` 与 `出殡三天之日给坟填土` 均为完整释义。",
    },
]

HTML_REPLACEMENTS = [
    {
        "name": "趁与复三释义串栏",
        "old": "<p>各种 ka13 ton41</p>\n<p><span class=\"dialect-word-head\">eə</span></p>\n<p>趁kə13一只脚跳动：右脚破了，只好</p>\n<p>复三 fua13 §313</p>\n<p>~着走</p>\n<p>出殡三天之日给坟</p>\n<p>髁头子 kə13 təu35 tl 膝盖</p>\n<p>填土</p>\n<p>咳嗽痨 ka13 13 1535 长久咳嗽的人</p>",
        "new": "<p>各种 ka13 ton41</p>\n<p><span class=\"dialect-word-head\">eə</span></p>\n<p>趁kə13一只脚跳动：右脚破了，只好~着走</p>\n<p>复三 fua13 §313 出殡三天之日给坟填土</p>\n<p>髁头子 kə13 təu35 tl 膝盖</p>\n<p>咳嗽痨 ka13 13 1535 长久咳嗽的人</p>",
    },
]

OCR_EVIDENCE = [
    "workbench/ocr/paddle_ocr/下/part02/page_0331.txt",
    "workbench/ocr/paddle_ocr/下/part02/page_0333.txt",
    "workbench/ocr/paddle_ocr/下/part02/page_0335.txt",
    "workbench/ocr/paddle_ocr/下/part02/page_0337.txt",
]
IMAGE_EVIDENCE = [
    "workbench/conversion/page_images/下/part02/page_0331_180dpi.jpg",
    "workbench/conversion/page_images/下/part02/page_0333_180dpi.jpg",
    "workbench/conversion/page_images/下/part02/page_0335_180dpi.jpg",
    "workbench/conversion/page_images/下/part02/page_0337_180dpi.jpg",
]


def replace_exact(path: Path, replacements: list[dict[str, str]]) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    changes: list[dict[str, object]] = []
    for replacement in replacements:
        count = text.count(replacement["old"])
        if count != 1:
            raise RuntimeError(f"{path} {replacement['name']} expected 1 match, got {count}")
        text = text.replace(replacement["old"], replacement["new"], 1)
        changes.append({"name": replacement["name"], "count": count})
    path.write_text(text, encoding="utf-8", newline="\n")
    return changes


def main() -> None:
    file_changes = []
    for path in SOURCE_PATHS:
        file_changes.append({"path": str(path.relative_to(ROOT)), "changes": replace_exact(path, SOURCE_REPLACEMENTS)})
    file_changes.append({"path": str(HTML.relative_to(ROOT)), "changes": replace_exact(HTML, HTML_REPLACEMENTS)})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "generated_at": now,
        "book_pages": [2615, 2617, 2619, 2621],
        "ocr_evidence": OCR_EVIDENCE,
        "image_evidence": IMAGE_EVIDENCE,
        "file_changes": file_changes,
        "repairs": [{"name": r["name"], "evidence": r["evidence"]} for r in SOURCE_REPLACEMENTS],
        "not_repaired": [
            "`杠`/`张`、`不好过`/`刹`、`作兴`/`撇清`/`□tu` 等周边串栏项暂不重排，留待页图逐字精校。",
            "`各种 ka13 ton41` 后的孤立 `eə` 暂不猜改。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 第五十九卷方言词汇2615至2621页核对",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第四章方言词汇，书页 2615、2617、2619、2621。",
        "- 原则：只修释义跨栏断裂且能闭合的词条；音值碎片和复杂两栏顺序暂不猜改。",
        "",
        "## 证据路径",
        "",
    ]
    for path in OCR_EVIDENCE:
        lines.append(f"- OCR：`{path}`")
    for path in IMAGE_EVIDENCE:
        lines.append(f"- 本地页图：`{path}`")
    lines.extend(["", "## 本批修复", ""])
    for repair in payload["repairs"]:
        lines.append(f"- {repair['name']}：{repair['evidence']}")
    lines.extend(["", "## 改写文件", "", "| 文件 | 修复项 | 命中 |", "|---|---|---:|"])
    for file_change in file_changes:
        for change in file_change["changes"]:
            lines.append(f"| `{file_change['path']}` | {change['name']} | {change['count']} |")
    lines.extend(["", "## 暂不处理", ""])
    lines.extend(f"- {item}" for item in payload["not_repaired"])
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS_MD.write_text(text, encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
