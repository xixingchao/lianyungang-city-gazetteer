from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/上/第十卷至第十六卷（part03）.md"),
        "replacements": [
            ("射人盐浆泵", "射入盐浆泵", "workbench/ocr/paddle_ocr/上/part03/page_0142.txt:34"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_上册_正文汇总.md"),
        "replacements": [
            ("射人盐浆泵", "射入盐浆泵", "workbench/ocr/paddle_ocr/上/part03/page_0142.txt:34"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第十七卷至第二十九卷（中part01）.md"),
        "replacements": [
            ("换人SJL3200", "换入SJL-3200", "workbench/ocr/paddle_ocr/中/part01/page_0350.txt:32"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("射人盐浆泵", "射入盐浆泵", "workbench/ocr/paddle_ocr/上/part03/page_0142.txt:34"),
            ("换人SJL3200", "换入SJL-3200", "workbench/ocr/paddle_ocr/中/part01/page_0350.txt:32"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_中册.html"),
        "replacements": [
            ("换人SJL3200", "换入SJL-3200", "workbench/ocr/paddle_ocr/中/part01/page_0350.txt:32"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_全书.html"),
        "replacements": [
            ("换人SJL3200", "换入SJL-3200", "workbench/ocr/paddle_ocr/中/part01/page_0350.txt:32"),
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
    report_md = ROOT / "output/reports/into_residues_batch251_20260707.md"
    report_json = ROOT / "output/reports/into_residues_batch251_20260707.json"
    lines = [
        "# 入字残留修复 batch251",
        "",
        f"- 修复总数：{total}",
        "- 范围：上册盐业源稿/汇总、中册电力源稿、全书汇总及当前中册/全书阅读稿。",
        "- 原则：仅修页级 PaddleOCR 明确支持的 `射人/换人` 具体短语，不处理 `轮换人员`、`可转入` 等合法跨词命中。",
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
