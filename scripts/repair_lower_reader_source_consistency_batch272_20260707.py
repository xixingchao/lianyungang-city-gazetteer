from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
    "output/final_reader/连云港市志_下册.html",
]

REPLACEMENTS = [
    {
        "old": "兵士人卫京师",
        "new": "兵士入卫京师",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:22-23; output/final_reader/连云港市志_全书.html:25052",
    },
    {
        "old": "兵士人卫</p><p>京师",
        "new": "兵士入卫</p><p>京师",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:22-23; output/final_reader/连云港市志_全书.html:25052",
    },
    {
        "old": "兵士人卫\n京师",
        "new": "兵士入卫\n京师",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:22-23; output/final_reader/连云港市志_全书.html:25052",
    },
    {
        "old": "对修志工作表现出极大的热枕",
        "new": "对修志工作表现出极大的热忱",
        "evidence": "output/final_reader/连云港市志_全书.html:26101",
    },
    {
        "old": "对修志工作表现出极大的热忧",
        "new": "对修志工作表现出极大的热忱",
        "evidence": "output/final_reader/连云港市志_全书.html:26116",
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
        "batch": 272,
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "notes": [
            "兵士入卫京师 is backed by page-level PaddleOCR and current full reader.",
            "热忱 corrections are same-paragraph consistency sync from the current full reader, where both corresponding paragraphs are already corrected.",
        ],
    }

    report_md = ROOT / "output/reports/lower_reader_source_consistency_batch272_20260707.md"
    report_json = ROOT / "output/reports/lower_reader_source_consistency_batch272_20260707.json"
    lines = [
        "# 下册阅读稿与源层一致性补修 batch272",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册人物传略阅读稿残留，以及下册附录/跋源层与当前全书阅读稿之间的不一致。",
        "- 原则：`兵士入卫京师` 以页级 PaddleOCR 和当前全书阅读稿为证；`热忱` 以当前全书同段校正文为证，只做同段追平。",
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
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
