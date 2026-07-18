from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    {
        "label": "新海发电厂元旦供电",
        "old": "民国38年（1949年）元且，开始向新\n海地区供电。",
        "new": "民国38年（1949年）元旦，开始向新\n海地区供电。",
        "evidence": "workbench/ocr/paddle_ocr/中/part01/page_0332.txt:34",
    },
    {
        "label": "四项事故隐患",
        "old": "四项事故隐惠为主",
        "new": "四项事故隐患为主",
        "evidence": "workbench/ocr/paddle_ocr/中/part01/page_0337.txt:31",
    },
    {
        "label": "人身事故隐患类别",
        "old": "身事故隐惠\"类别的分析统计。",
        "new": "身事故隐患”类别的分析统计。",
        "evidence": "workbench/ocr/paddle_ocr/中/part01/page_0338.txt:7",
    },
]

TARGETS = [
    Path("workbench/body_chapters/第十七卷至第二十九卷（中part01）.md"),
    Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
    Path("output/final_reader/连云港市志_中册.html"),
    Path("output/final_reader/连云港市志_全书.html"),
]


def apply() -> list[dict[str, object]]:
    changes: list[dict[str, object]] = []
    for rel in TARGETS:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        original = text
        file_hits = []
        for repl in REPLACEMENTS:
            count = text.count(repl["old"])
            if count:
                text = text.replace(repl["old"], repl["new"])
                file_hits.append({**repl, "count": count})
        if text != original:
            path.write_text(text, encoding="utf-8", newline="")
        changes.append({"path": str(rel), "changes": file_hits})
    return changes


def write_report(changes: list[dict[str, object]]) -> None:
    report_md = ROOT / "output/reports/middle_power_source_residues_batch243_20260707.md"
    report_json = ROOT / "output/reports/middle_power_source_residues_batch243_20260707.json"
    total = sum(item["count"] for file in changes for item in file["changes"])
    lines = [
        "# 中册电力章源正文残留修复 batch243",
        "",
        f"- 修复总数：{total}",
        "- 范围：中册电力章正文、全书正文汇总、当前中册/全书阅读器。",
        "- 原则：仅替换页级 PaddleOCR 已明确支持的短残留，不改 OCR 原始层。",
        "",
        "## 证据与替换",
    ]
    for file in changes:
        if not file["changes"]:
            continue
        lines.append(f"\n### {file['path']}")
        for item in file["changes"]:
            lines.append(
                f"- {item['label']}：`{item['old']}` -> `{item['new']}`；"
                f"次数 {item['count']}；证据 `{item['evidence']}`"
            )
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    import json

    report_json.write_text(
        json.dumps({"total": total, "changes": changes}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    result = apply()
    write_report(result)
    print(sum(item["count"] for file in result for item in file["changes"]))
    for file in result:
        if file["changes"]:
            print(file["path"])
