from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/第三十卷至第四十二卷（中part02）.md"),
        "replacements": [
            ("输人棉布", "输入棉布", "workbench/ocr/paddle_ocr/中/part02/page_0133.txt:10"),
            ("输人砂糖", "输入砂糖", "workbench/ocr/paddle_ocr/中/part02/page_0144.txt:12"),
            ("输人卷烟", "输入卷烟", "workbench/ocr/paddle_ocr/中/part02/page_0145.txt:21-22"),
            ("输人13367", "输入13367", "workbench/ocr/paddle_ocr/中/part02/page_0245.txt:24"),
            ("输出人港", "输出入港", "workbench/ocr/paddle_ocr/中/part02/page_0245.txt:24"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"),
        "replacements": [
            ("缅甸输人", "缅甸输入", "workbench/ocr/paddle_ocr/下/part02/page_0111.txt:11"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("输人棉布", "输入棉布", "workbench/ocr/paddle_ocr/中/part02/page_0133.txt:10"),
            ("输人卷烟", "输入卷烟", "workbench/ocr/paddle_ocr/中/part02/page_0145.txt:21-22"),
            ("输人13367", "输入13367", "workbench/ocr/paddle_ocr/中/part02/page_0245.txt:24"),
            ("输出人港", "输出入港", "workbench/ocr/paddle_ocr/中/part02/page_0245.txt:24"),
            ("缅甸输人", "缅甸输入", "workbench/ocr/paddle_ocr/下/part02/page_0111.txt:11"),
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
    report_md = ROOT / "output/reports/source_input_residues_batch247_20260707.md"
    report_json = ROOT / "output/reports/source_input_residues_batch247_20260707.json"

    lines = [
        "# 源稿输入残留修复 batch247",
        "",
        f"- 修复总数：{total}",
        "- 范围：中册商业/粮油源稿、下册文物源稿及全书正文汇总。当前阅读稿对应位置已为正确文本。",
        "- 原则：仅替换页级 PaddleOCR 明确支持的具体短语，不处理 `运输人员` 等合法包含 `输人` 的词。",
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
