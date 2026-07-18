from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"),
        "replacements": [
            ("好版面一一等奖", "好版面一等奖", "workbench/ocr/paddle_ocr/下/part02/page_0137.txt:21-22"),
            ("刘备着属", "刘备眷属", "workbench/body_chapters/连云港市志_全书_正文汇总.md:113420 同段已校为眷属"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("好版面一一等奖", "好版面一等奖", "workbench/ocr/paddle_ocr/下/part02/page_0137.txt:21-22"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_下册.html"),
        "replacements": [
            ("好版面一一等奖", "好版面一等奖", "workbench/ocr/paddle_ocr/下/part02/page_0137.txt:21-22"),
        ],
    },
]

BAD = ["好版面一一等奖", "刘备着属"]


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

    target_paths = sorted({str(task["path"]) for task in TASKS})
    residuals = {}
    for rel in target_paths:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        hits = {bad: text.count(bad) for bad in BAD if text.count(bad)}
        if hits:
            residuals[rel] = hits

    total = sum(item["count"] for file in changes for item in file["changes"])
    report_md = ROOT / "output/reports/lower_source_award_and_juanshu_batch260_20260707.md"
    report_json = ROOT / "output/reports/lower_source_award_and_juanshu_batch260_20260707.json"
    lines = [
        "# 下册获奖等级与眷属源层残留修复 batch260",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册报刊广播电视段、下册人物糜竺传源层、全书正文汇总及当前下册阅读稿。",
        "- 原则：只处理页级 PaddleOCR 或当前全书同段已校文本可支撑的定点残留。",
        "- 图片处理：未打开、展示或嵌入图片。",
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
