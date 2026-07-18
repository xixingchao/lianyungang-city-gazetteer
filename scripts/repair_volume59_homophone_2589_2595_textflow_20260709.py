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
REPORT_JSON = ROOT / "output" / "reports" / "volume59_homophone_2589_2595_textflow_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "volume59_homophone_2589_2595_textflow_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷同音字汇2589至2595页行界修复.md"

SOURCE_REPLACEMENTS = [
    {
        "name": "垢字归入勾韵k组并合并跑了释义",
        "old": "io\nk ①勾沟钩佝篝 ③狗苟枸 ④够构购\np ①标膘长~镖骠彪飙瞟盯：~着他,别让跑\n垢\n了③表裱婊④標鳔膘油发过的猪皮：\nk①扣纽~抠~出来眍②□凶、厉害：这人",
        "new": "io\nk ①勾沟钩佝篝 ③狗苟枸 ④够构购垢\np ①标膘长~镖骠彪飙瞟盯：~着他,别让跑了③表裱婊④標鳔膘油发过的猪皮：\nk①扣纽~抠~出来眍②□凶、厉害：这人",
        "evidence": "书页 2589 同音字汇 `io` 韵中，孤立 `垢` 与 `够构购` 同音，应归入 `k` 组 ④；`别让跑/了③表...` 也应为同一 `p` 组行。",
    },
    {
        "name": "境镜敬归回in韵tc组",
        "old": "尽烬进浸妗仅噤禁~止劲泾颈茎径竞\nion\n境镜敬\ntc ①军君均钧 ③菌窘迥 ④郡俊骏",
        "new": "尽烬进浸妗仅噤禁~止劲泾颈茎径竞境镜敬\nion\ntc ①军君均钧 ③菌窘迥 ④郡俊骏",
        "evidence": "书页 2595 `境镜敬` 与前行 `径竞` 同属同音字组，当前被 `ion` 韵母标题隔开；移回前行后韵部边界恢复。",
    },
]

HTML_REPLACEMENTS = [
    {
        "name": "垢字归入勾韵k组并合并跑了释义",
        "old": "<p><span class=\"dialect-word-head\">io</span></p>\n<p>k ①勾沟钩佝篝 ③狗苟枸 ④够构购</p>\n<p>p ①标膘长~镖骠彪飙瞟盯：~着他,别让跑</p>\n<p>垢</p>\n<p>了③表裱婊④標鳔膘油发过的猪皮：</p>\n<p>k①扣纽~抠~出来眍②□凶、厉害：这人</p>",
        "new": "<p><span class=\"dialect-word-head\">io</span></p>\n<p>k ①勾沟钩佝篝 ③狗苟枸 ④够构购垢</p>\n<p>p ①标膘长~镖骠彪飙瞟盯：~着他,别让跑了③表裱婊④標鳔膘油发过的猪皮：</p>\n<p>k①扣纽~抠~出来眍②□凶、厉害：这人</p>",
    },
    {
        "name": "境镜敬归回in韵tc组",
        "old": "<p>尽烬进浸妗仅噤禁~止劲泾颈茎径竞</p>\n<p><span class=\"dialect-word-head\">ion</span></p>\n<p>境镜敬</p>\n<p>tc ①军君均钧 ③菌窘迥 ④郡俊骏</p>",
        "new": "<p>尽烬进浸妗仅噤禁~止劲泾颈茎径竞境镜敬</p>\n<p><span class=\"dialect-word-head\">ion</span></p>\n<p>tc ①军君均钧 ③菌窘迥 ④郡俊骏</p>",
    },
]

OCR_EVIDENCE = [
    "workbench/ocr/paddle_ocr/下/part02/page_0305.txt",
    "workbench/ocr/paddle_ocr/下/part02/page_0311.txt",
]
IMAGE_EVIDENCE = [
    "workbench/conversion/page_images/下/part02/page_0305_180dpi.jpg",
    "workbench/conversion/page_images/下/part02/page_0311_180dpi.jpg",
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
        "book_pages": [2589, 2595],
        "ocr_evidence": OCR_EVIDENCE,
        "image_evidence": IMAGE_EVIDENCE,
        "file_changes": file_changes,
        "repairs": [{"name": r["name"], "evidence": r["evidence"]} for r in SOURCE_REPLACEMENTS],
        "not_repaired": [
            "书页 2593 的孤立 `③` 涉及两栏交错，暂不移动，留待页图逐字精校。",
            "不改音标、不改同音字内容，仅恢复高置信行界。",
        ],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 第五十九卷同音字汇2589至2595页行界修复",
        "",
        f"- 时间：{now}",
        "- 范围：第五十九卷第三章同音字汇，书页 2589、2595。",
        "- 原则：只修能由同音字组与韵部边界互证的行界错位；不猜改音标和字表。",
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
    print(json.dumps(payload, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
