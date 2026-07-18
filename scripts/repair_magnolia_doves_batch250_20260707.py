from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OLD = "方头乳鸽"
NEW = "万头乳鸽"
EVIDENCE = "workbench/ocr/paddle_ocr/中/part02/page_0103.txt:30"

TARGETS = [
    Path("workbench/body_chapters/第三十卷至第四十二卷（中part02）.md"),
    Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
    Path("output/final_reader/连云港市志_中册.html"),
    Path("output/final_reader/连云港市志_全书.html"),
]


def main():
    changes = []
    for rel_path in TARGETS:
        path = ROOT / rel_path
        text = path.read_text(encoding="utf-8")
        count = text.count(OLD)
        if count:
            path.write_text(text.replace(OLD, NEW), encoding="utf-8", newline="")
        changes.append({"path": str(rel_path), "old": OLD, "new": NEW, "count": count, "evidence": EVIDENCE})

    total = sum(item["count"] for item in changes)
    report_md = ROOT / "output/reports/magnolia_doves_batch250_20260707.md"
    report_json = ROOT / "output/reports/magnolia_doves_batch250_20260707.json"
    lines = [
        "# 东磊玉兰万头乳鸽残留修复 batch250",
        "",
        f"- 修复总数：{total}",
        "- 范围：中册风景名胜源稿、全书正文汇总及当前中册/全书阅读稿。",
        "- 原则：仅修页级 PaddleOCR 明确支持的短语，不处理合法 `方头鱼`、`地方头人`。",
        "",
        "## 证据",
        f"- `{EVIDENCE}`：`的花朵如同万头乳鸽栖息林头`",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps({"total": total, "changes": changes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(total)
    for item in changes:
        if item["count"]:
            print(item["path"])


if __name__ == "__main__":
    main()
