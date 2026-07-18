from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
]

REPLACEMENTS = [
    {
        "old": "准北盐务局成立盐业情报中心站",
        "new": "淮北盐务局成立盐业情报中心站",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0429.txt:19",
    },
    {
        "old": "准北盐场女子篮球代表队",
        "new": "淮北盐场女子篮球代表队",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0234.txt:18-20",
    },
    {
        "old": "准北盐场举办过两届田径运动会",
        "new": "淮北盐场举办过两届田径运动会",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0234.txt:31-33",
    },
    {
        "old": "超过全准北盐场头号滩",
        "new": "超过全淮北盐场头号滩",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0377.txt:32",
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
        "batch": 273,
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "notes": [
            "This batch only fixes source-layer phrases backed by page-level PaddleOCR.",
            "Current final-reader HTML had no 准北盐... hits for these phrases before the batch.",
            "No broad 准北 -> 淮北 replacement was performed.",
        ],
    }

    report_md = ROOT / "output/reports/lower_huaibei_salt_source_batch273_20260707.md"
    report_json = ROOT / "output/reports/lower_huaibei_salt_source_batch273_20260707.json"
    lines = [
        "# 下册淮北盐务盐场源层残留补修 batch273",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册科技、体育、人物传略源稿及全书正文汇总。当前正式阅读稿未命中这些 `准北盐...` 短语，本批主要防止源层回流。",
        "- 原则：只处理页级 PaddleOCR 明确读作 `淮北` 的完整短语；不做 `准北 -> 淮北` 泛替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for row in changes:
        if row["count"]:
            lines.append(f"- `{row['path']}`：`{row['old']}` -> `{row['new']}`；次数 {row['count']}；证据 `{row['evidence']}`")
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
        "- 其它 `准北盐...` 残留仍需逐页定位 OCR 证据后再处理，本批不扩大范围。",
    ])
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
