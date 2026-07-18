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
REPORT_JSON = ROOT / "output" / "reports" / "volume59_vocab_2607_2613_textflow_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_vocab_2607_2613_textflow_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷方言词汇2607至2613页核对.md"

SOURCE_REPLACEMENTS = [
    {
        "name": "干石洺词条释义断行",
        "old": "干石洺 k 313 tuə13 tuə13 稠：稀饭 ~\n儿\n的\n烂沫淤",
        "new": "干石洺 k 313 tuə13 tuə13 稠：稀饭 ~的\n烂沫淤",
        "evidence": "OCR/源稿/HTML 均显示 `稀饭 ~` 后接孤立 `儿`、`的`；释义 `稀饭~的` 语义完整，孤立 `儿` 按版面噪声剔除。",
    },
    {
        "name": "嫌好识歹词条释义断行",
        "old": "嫌好识歹 cie35\nx41\nS13\ntε41过份\n填坟 tie35 fər35 为坟墓添土修饰\n挑剔\n甜 tiě",
        "new": "嫌好识歹 cie35\nx41\nS13\ntε41过份挑剔\n填坟 tie35 fər35 为坟墓添土修饰\n甜 tiě",
        "evidence": "书页 2613 OCR/源稿/HTML 均显示 `过份` 与孤立 `挑剔` 被 `填坟` 词条隔断；`过份挑剔` 为同一释义。",
    },
]

HTML_REPLACEMENTS = [
    {
        "name": "干石洺词条释义断行",
        "old": "<p>干石洺 k 313 tuə13 tuə13 稠：稀饭 ~</p>\n<p>儿</p>\n<p>的</p>\n<p>烂沫淤 1 55 mə13 y313 淤泥</p>",
        "new": "<p>干石洺 k 313 tuə13 tuə13 稠：稀饭 ~的</p>\n<p>烂沫淤 1 55 mə13 y313 淤泥</p>",
    },
    {
        "name": "嫌好识歹词条释义断行",
        "old": "<p>嫌好识歹 cie35</p>\n<p><span class=\"dialect-word-head\">x41</span></p>\n<p><span class=\"dialect-word-head\">S13</span></p>\n<p>tε41过份</p>\n<p>填坟 tie35 fər35 为坟墓添土修饰</p>\n<p>挑剔</p>\n<p>甜 tiě 盐少味淡</p>",
        "new": "<p>嫌好识歹 cie35</p>\n<p><span class=\"dialect-word-head\">x41</span></p>\n<p><span class=\"dialect-word-head\">S13</span></p>\n<p>tε41过份挑剔</p>\n<p>填坟 tie35 fər35 为坟墓添土修饰</p>\n<p>甜 tiě 盐少味淡</p>",
    },
]

OCR_EVIDENCE = [
    "workbench/ocr/paddle_ocr/下/part02/page_0323.txt",
    "workbench/ocr/paddle_ocr/下/part02/page_0329.txt",
]
IMAGE_EVIDENCE = [
    "workbench/conversion/page_images/下/part02/page_0323_180dpi.jpg",
    "workbench/conversion/page_images/下/part02/page_0329_180dpi.jpg",
]


def replace_exact(path: Path, replacements: list[dict[str, str]]) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    changes: list[dict[str, object]] = []
    for replacement in replacements:
        old = replacement["old"]
        new = replacement["new"]
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"{path} {replacement['name']} expected 1 match, got {count}")
        text = text.replace(old, new, 1)
        changes.append({"name": replacement["name"], "count": count})
    path.write_text(text, encoding="utf-8", newline="\n")
    return changes


def main() -> None:
    file_changes = []
    for path in SOURCE_PATHS:
        file_changes.append(
            {
                "path": str(path.relative_to(ROOT)),
                "changes": replace_exact(path, SOURCE_REPLACEMENTS),
            }
        )
    file_changes.append(
        {
            "path": str(HTML.relative_to(ROOT)),
            "changes": replace_exact(HTML, HTML_REPLACEMENTS),
        }
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "generated_at": now,
        "book_pages": [2607, 2609, 2611, 2613],
        "ocr_evidence": OCR_EVIDENCE,
        "image_evidence": IMAGE_EVIDENCE,
        "file_changes": file_changes,
        "repairs": [
            {
                "name": r["name"],
                "evidence": r["evidence"],
            }
            for r in SOURCE_REPLACEMENTS
        ],
        "not_repaired": [
            "`x41`、`S13` 等音值碎片暂不猜改，留待页图逐字精校。",
            "`山水牛牛`、`甜不拉叽` 附近两栏交错项暂不重排，避免无证据合并。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 第五十九卷方言词汇2607至2613页核对",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第四章方言词汇，书页 2607、2609、2611、2613。",
        "- 原则：只修 OCR、源稿、HTML 三处同形且语义边界明确的词条断行；音标和两栏交错项不猜改。",
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
