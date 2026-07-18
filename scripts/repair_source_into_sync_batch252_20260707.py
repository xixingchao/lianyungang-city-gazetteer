from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"),
        "replacements": [
            ("并人治安科", "并入治安科", "workbench/ocr/paddle_ocr/下/part01/page_0063.txt:32"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第三十卷至第四十二卷（中part02）.md"),
        "replacements": [
            ("划人江苏省", "划入江苏省", "workbench/ocr/paddle_ocr/中/part02/page_0484.txt:21"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("并人治安科", "并入治安科", "workbench/ocr/paddle_ocr/下/part01/page_0063.txt:32"),
            ("划人江苏省", "划入江苏省", "workbench/ocr/paddle_ocr/中/part02/page_0413.txt:9;page_0484.txt:21"),
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
    report_md = ROOT / "output/reports/source_into_sync_batch252_20260707.md"
    report_json = ROOT / "output/reports/source_into_sync_batch252_20260707.json"
    lines = [
        "# 源稿并入划入残留修复 batch252",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册公安源稿、中册政府源稿及全书正文汇总。当前阅读稿对应短语无残留。",
        "- 原则：仅修页级 PaddleOCR 明确支持的 `并人/划人` 具体短语，不处理其他高频 `投人/并人/划人`。",
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
