from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/第三十卷至第四十二卷（中part02）.md"),
        "replacements": [
            ("业务进人稳步发展", "业务进入稳步发展", "workbench/ocr/paddle_ocr/中/part02/page_0080.txt:15"),
            ("连云港市进人全国自动转报网", "连云港市进入全国自动转报网", "workbench/ocr/paddle_ocr/中/part02/page_0080.txt:24"),
            ("进人全国自动网", "进入全国自动网", "workbench/ocr/paddle_ocr/中/part02/page_0084.txt:9"),
            ("进人市话网", "进入市话网", "workbench/ocr/paddle_ocr/中/part02/page_0086.txt:22"),
            ("进人社会主义建设时期", "进入社会主义建设时期", "workbench/ocr/paddle_ocr/中/part02/page_0121.txt:18"),
            ("进人市场", "进入市场", "workbench/ocr/paddle_ocr/中/part02/page_0144.txt:9;page_0174.txt:9;page_0261.txt:16;page_0271.txt:18"),
            ("进人大市场", "进入大市场", "workbench/ocr/paddle_ocr/中/part02/page_0258.txt:14;page_0260.txt:31"),
            ("进人20世纪80年代", "进入20世纪80年代", "workbench/ocr/paddle_ocr/中/part02/page_0443.txt:33;page_0444.txt:41"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"),
        "replacements": [
            ("进人人防工事", "进入人防工事", "workbench/ocr/paddle_ocr/下/part01/page_0188.txt:36"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("市长途自动联网成功并进人全国自动网", "市长途自动联网成功并进入全国自动网", "workbench/ocr/paddle_ocr/中/part02/page_0084.txt:9"),
            ("进人市话网", "进入市话网", "workbench/ocr/paddle_ocr/中/part02/page_0086.txt:22"),
            ("进人社会主义建设时期", "进入社会主义建设时期", "workbench/ocr/paddle_ocr/中/part02/page_0121.txt:18"),
            ("进人市场", "进入市场", "workbench/ocr/paddle_ocr/中/part02/page_0144.txt:9;page_0174.txt:9;page_0261.txt:16;page_0271.txt:18"),
            ("进人大市场", "进入大市场", "workbench/ocr/paddle_ocr/中/part02/page_0258.txt:14;page_0260.txt:31"),
            ("进人人防工事", "进入人防工事", "workbench/ocr/paddle_ocr/下/part01/page_0188.txt:36"),
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
    report_md = ROOT / "output/reports/source_enter_residues_batch248_20260707.md"
    report_json = ROOT / "output/reports/source_enter_residues_batch248_20260707.json"
    lines = [
        "# 源稿进入残留修复 batch248",
        "",
        f"- 修复总数：{total}",
        "- 范围：中册邮电/商业/物资/党务源稿、下册人防源稿及全书正文汇总。当前阅读稿对应短语无残留。",
        "- 原则：仅修页级 PaddleOCR 明确支持的具体短语；大事记 `市话进人全国自动网` 与 `进人新的建设与发展时期` 证据不足，暂未处理。",
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
