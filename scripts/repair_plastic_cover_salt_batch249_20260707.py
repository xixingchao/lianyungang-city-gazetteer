from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/上/第十卷至第十六卷（part03）.md"),
        "replacements": [
            ("塑苦池结晶", "塑苫池结晶", "workbench/ocr/paddle_ocr/上/part03/page_0136.txt:19"),
            ("塑苦盐", "塑苫盐", "workbench/ocr/paddle_ocr/上/part03/page_0142.txt:37"),
            ("塑苦新技术", "塑苫新技术", "workbench/ocr/paddle_ocr/上/part03/page_0143.txt:16"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_上册_正文汇总.md"),
        "replacements": [
            ("塑苦池结晶", "塑苫池结晶", "workbench/ocr/paddle_ocr/上/part03/page_0136.txt:19"),
            ("塑苦盐", "塑苫盐", "workbench/ocr/paddle_ocr/上/part03/page_0142.txt:37"),
            ("塑苦新技术", "塑苫新技术", "workbench/ocr/paddle_ocr/上/part03/page_0143.txt:16"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"),
        "replacements": [
            ("塑苦结晶", "塑苫结晶", "workbench/ocr/paddle_ocr/下/part01/page_0443.txt:22"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("塑苦池结晶", "塑苫池结晶", "workbench/ocr/paddle_ocr/上/part03/page_0136.txt:19"),
            ("塑苦盐", "塑苫盐", "workbench/ocr/paddle_ocr/上/part03/page_0142.txt:37"),
            ("塑苦新技术", "塑苫新技术", "workbench/ocr/paddle_ocr/上/part03/page_0143.txt:16"),
            ("塑苦结晶", "塑苫结晶", "workbench/ocr/paddle_ocr/下/part01/page_0443.txt:22"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_全书.html"),
        "replacements": [
            ("塑苦结晶", "塑苫结晶", "workbench/ocr/paddle_ocr/下/part01/page_0443.txt:22"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_下册.html"),
        "replacements": [
            ("塑苦结晶", "塑苫结晶", "workbench/ocr/paddle_ocr/下/part01/page_0443.txt:22"),
        ],
    },
]


def main():
    changes = []
    for task in TASKS:
        path = ROOT / task["path"]
        text = path.read_text(encoding="utf-8")
        hits = []
        for old, new, evidence in task["replacements"]:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            hits.append({"old": old, "new": new, "count": count, "evidence": evidence})
        path.write_text(text, encoding="utf-8", newline="")
        changes.append({"path": str(task["path"]), "changes": hits})

    total = sum(item["count"] for file in changes for item in file["changes"])
    report_md = ROOT / "output/reports/plastic_cover_salt_batch249_20260707.md"
    report_json = ROOT / "output/reports/plastic_cover_salt_batch249_20260707.json"
    lines = [
        "# 塑苫结晶残留修复 batch249",
        "",
        f"- 修复总数：{total}",
        "- 范围：上册盐业源稿/汇总、下册科技化工源稿、全书汇总及当前下册/全书阅读稿。",
        "- 原则：仅修页级 PaddleOCR 明确支持的 `塑苦 -> 塑苫` 短语，不处理备份目录与 OCR 原始层。",
        "",
        "## 替换明细",
    ]
    for file in changes:
        lines.append(f"\n### {file['path']}")
        for item in file["changes"]:
            lines.append(f"- `{item['old']}` -> `{item['new']}`；次数 {item['count']}；证据 `{item['evidence']}`")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps({"total": total, "changes": changes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(total)
    for file in changes:
        if any(item["count"] for item in file["changes"]):
            print(file["path"])


if __name__ == "__main__":
    main()
