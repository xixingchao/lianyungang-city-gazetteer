from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    {
        "old": "新华社北盐场支社",
        "new": "新华社淮北盐场支社",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0135.txt:87",
        "targets": [
            "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_下册.html",
        ],
    },
    {
        "old": "全国黄军校同学会",
        "new": "全国黄埔军校同学会",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0346.txt:15-17",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_全书.html",
            "output/final_reader/连云港市志_下册.html",
        ],
    },
    {
        "old": "越级进人一级战备",
        "new": "越级进入一级战备",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0188.txt:35",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
        ],
    },
    {
        "old": "人口蔬散",
        "new": "人口疏散",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0186.txt:25,30-33; page_0188.txt:35",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_下册.html",
        ],
    },
    {
        "old": "建立-处经营性骨灰公墓",
        "new": "建立一处经营性骨灰公墓",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0055.txt:27",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_全书.html",
            "output/final_reader/连云港市志_下册.html",
        ],
    },
]

CHECK_TARGETS = sorted({target for item in REPLACEMENTS for target in item["targets"]})
BAD_PATTERNS = [item["old"] for item in REPLACEMENTS]


def main():
    changes = []
    for item in REPLACEMENTS:
        for rel in item["targets"]:
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
    for rel in CHECK_TARGETS:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        hits = {bad: text.count(bad) for bad in BAD_PATTERNS if text.count(bad)}
        if hits:
            residuals[rel] = hits

    total = sum(row["count"] for row in changes)
    report = {
        "batch": 266,
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "skipped": [
            {
                "text": "组扩编人防专业队伍",
                "reason": "同页 OCR 仍读为该短语，可能为组建/扩编压缩表述；本批不凭语感修改。",
                "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0188.txt:36",
            }
        ],
    }

    report_md = ROOT / "output/reports/lower_clear_ocr_residues_batch266_20260707.md"
    report_json = ROOT / "output/reports/lower_clear_ocr_residues_batch266_20260707.json"
    lines = [
        "# 下册明确 OCR 残留补修 batch266",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册民政、人防、社团、新闻出版相关短残留。",
        "- 原则：只处理页级 OCR 或同章术语可直接坐实的短语；不处理同页仍不明确的 `组扩编人防专业队伍`。",
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
        lines.append("- 本批坏短语在目标文件中均为 0。")
    lines.extend([
        "",
        "## 未处理项",
        "",
        "- `组扩编人防专业队伍`：`workbench/ocr/paddle_ocr/下/part01/page_0188.txt:36` 同样读作该短语，本批暂留。",
    ])
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
