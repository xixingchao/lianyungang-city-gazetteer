from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/第三十卷至第四十二卷（中part02）.md"),
        "replacements": [
            ("侨券中担任", "侨眷中担任", "workbench/ocr/paddle_ocr/中/part02/page_0455.txt:11"),
            ("侨誉凭侨汇", "侨眷凭侨汇", "workbench/ocr/paddle_ocr/中/part02/page_0377.txt:52"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_中册.html"),
        "replacements": [
            ("侨券中担任", "侨眷中担任", "workbench/ocr/paddle_ocr/中/part02/page_0455.txt:11"),
            ("侨誉凭侨汇", "侨眷凭侨汇", "workbench/ocr/paddle_ocr/中/part02/page_0377.txt:52"),
        ],
    },
]

BAD = [old for task in TASKS for old, _, _ in task["replacements"]]


def main():
    changes = []
    for task in TASKS:
        path = ROOT / task["path"]
        text = path.read_text(encoding="utf-8")
        file_changes = []
        for old, new, evidence in task["replacements"]:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            file_changes.append({"old": old, "new": new, "count": count, "evidence": evidence})
        path.write_text(text, encoding="utf-8", newline="")
        changes.append({"path": str(task["path"]), "changes": file_changes})

    residuals = {}
    for rel in sorted({str(task["path"]) for task in TASKS}):
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        hits = {bad: text.count(bad) for bad in BAD if text.count(bad)}
        if hits:
            residuals[rel] = hits

    total = sum(item["count"] for file in changes for item in file["changes"])
    report_md = ROOT / "output/reports/middle_overseas_chinese_followup_batch258_20260707.md"
    report_json = ROOT / "output/reports/middle_overseas_chinese_followup_batch258_20260707.json"
    lines = [
        "# 中册侨眷残留补修 batch258",
        "",
        f"- 修复总数：{total}",
        "- 范围：中册商业侨汇段和统战侨务段源稿、当前中册阅读稿。",
        "- 原则：只处理页级 PaddleOCR 明确为 `侨眷` 的短语；线性表格残留 `归侨侨誉` 暂不改。",
        "",
        "## 替换明细",
    ]
    for file in changes:
        lines.append(f"\n### {file['path']}")
        for item in file["changes"]:
            lines.append(f"- `{item['old']}` -> `{item['new']}`；次数 {item['count']}；证据 `{item['evidence']}`")
    lines.extend(["", "## 残留计数", ""])
    if residuals:
        for rel, hits in residuals.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批坏短语在目标文件中均为 0。")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps({"total": total, "changes": changes, "residuals": residuals}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
