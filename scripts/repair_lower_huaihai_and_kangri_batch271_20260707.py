from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
    "output/final_reader/连云港市志_全书.html",
    "output/final_reader/连云港市志_下册.html",
]

REPLACEMENTS = [
    {
        "old": "准海大学",
        "new": "淮海大学",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0199.txt:57; page_0201.txt:7; page_0395.txt:9,77",
    },
    {
        "old": "准海日报",
        "new": "淮海日报",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0332.txt:12",
    },
    {
        "old": "准海区",
        "new": "淮海区",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0163.txt:35; 下/part02/page_0352.txt:40; page_0373.txt:23; page_0377.txt:18",
    },
    {
        "old": "抗甘民族统一战线政策",
        "new": "抗日民族统一战线政策",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0363.txt:20",
    },
    {
        "old": "苏\n中抗甘根据地",
        "new": "苏\n中抗日根据地",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0367.txt:16",
    },
    {
        "old": "苏</p><p>中抗甘根据地",
        "new": "苏</p><p>中抗日根据地",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0367.txt:16",
    },
]

BAD_PATTERNS = [item["old"] for item in REPLACEMENTS]


def main():
    changes = []
    for item in REPLACEMENTS:
        for rel in TARGETS:
            path = ROOT / rel
            text = path.read_text(encoding="utf-8", errors="ignore")
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
                path.write_text(text, encoding="utf-8", newline="")
            changes.append({
                "path": rel,
                "old": item["old"],
                "new": item["new"],
                "count": count,
                "evidence": item["evidence"],
            })

    residuals = {}
    for rel in TARGETS:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        hits = {bad: text.count(bad) for bad in BAD_PATTERNS if text.count(bad)}
        if hits:
            residuals[rel] = hits

    total = sum(row["count"] for row in changes)
    report = {
        "batch": 271,
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "skipped": [
            {
                "text": "抗甘薯黑斑病",
                "reason": "Legitimate agriculture term; not changed.",
            },
            {
                "text": "准北盐...",
                "reason": "Likely 淮北 in many contexts, but broad replacement needs page-by-page evidence; not changed in this batch.",
            },
            {
                "text": "热忧 / 热枕",
                "reason": "No same-page OCR evidence located in this pass; not changed.",
            },
        ],
    }

    report_md = ROOT / "output/reports/lower_huaihai_and_kangri_batch271_20260707.md"
    report_json = ROOT / "output/reports/lower_huaihai_and_kangri_batch271_20260707.json"
    lines = [
        "# 下册淮海与抗日源证据残留补修 batch271",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册军事/干部/妇女/人物传略相关源稿、全书正文汇总及当前正式阅读稿。",
        "- 原则：只处理页级 PaddleOCR 明确支持的 `准海 -> 淮海` 和政治语境 `抗甘 -> 抗日`；保留农业术语 `抗甘薯黑斑病`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for row in changes:
        if row["count"]:
            old = row["old"].replace("\n", "\\n")
            new = row["new"].replace("\n", "\\n")
            lines.append(f"- `{row['path']}`：`{old}` -> `{new}`；次数 {row['count']}；证据 `{row['evidence']}`")
    lines.extend(["", "## 残留计数", ""])
    if residuals:
        for rel, hits in residuals.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批坏短语在目标文件中均为 0。")
    lines.extend([
        "",
        "## 未处理项",
        "",
        "- `抗甘薯黑斑病`：农业病害术语，保持不动。",
        "- `准北盐...`：多处疑似应为 `淮北盐...`，但涉及篇幅大，本批不做泛替换。",
        "- `热忧` / `热枕`：尚未定位到同页 OCR 证据，暂不凭语感修改。",
    ])
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
