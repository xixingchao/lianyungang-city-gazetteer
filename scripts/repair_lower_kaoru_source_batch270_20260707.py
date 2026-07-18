from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
]

REPLACEMENTS = [
    {
        "old": "考人江苏陆军讲武堂",
        "new": "考入江苏陆军讲武堂",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0354.txt:22",
    },
    {
        "old": "考人江苏省立第八师范\n学校。民国10年",
        "new": "考入江苏省立第八师范\n学校。民国10年",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0358.txt:28-29",
    },
    {
        "old": "考人江苏省立连\n云水产学校",
        "new": "考入江苏省立连\n云水产学校",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0372.txt:15-16",
    },
    {
        "old": "考人江苏省立东海师范学校",
        "new": "考入江苏省立东海师范学校",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0372.txt:37",
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
        "batch": 270,
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "skipped": [
            {
                "text": "考人江苏省立第十一中学 / 年（1924年）秋，考人江苏省立第八师范学校",
                "reason": "The corresponding page-level OCR still reads 考人, so no correction was made in this batch.",
                "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0364.txt:24; page_0367.txt:30",
            }
        ],
    }

    report_md = ROOT / "output/reports/lower_kaoru_source_batch270_20260707.md"
    report_json = ROOT / "output/reports/lower_kaoru_source_batch270_20260707.json"
    lines = [
        "# 下册人物传略考入源层补修 batch270",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册人物传略源稿和全书正文汇总中的 `考人江苏...` 源层残留。当前正式读者对应短语已无残留，本批主要防止源层回流。",
        "- 原则：只处理页级 PaddleOCR 明确读作 `考入` 的完整短语；页级 OCR 仍读作 `考人` 的项暂留。",
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
        lines.append("- 本批坏短语在目标源稿中均为 0。")
    lines.extend([
        "",
        "## 未处理项",
        "",
        "- `考人江苏省立第十一中学`、`年（1924年）秋，考人江苏省立第八师范学校`：页级 OCR 仍读作 `考人`，本批不凭常识修改。",
    ])
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
