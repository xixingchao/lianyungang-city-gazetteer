from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    {
        "old": "为使烈士英名流传方世，为千百万人民瞻仰敬\n战五周年之际",
        "new": "为使烈士英名流传万世，为千百万人民瞻仰敬礼。抗\n战五周年之际",
        "targets": [
            "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
        ],
        "evidence": "output/final_reader/连云港市志_全书.html:26027 同段已校为 `流传万世，为千百万人民瞻仰敬礼。抗战五周年之际`",
    },
    {
        "old": "为使烈士英名流传方世，为千百万人民瞻仰敬</p><p>战五周年之际",
        "new": "为使烈士英名流传万世，为千百万人民瞻仰敬礼。抗</p><p>战五周年之际",
        "targets": [
            "output/final_reader/连云港市志_下册.html",
        ],
        "evidence": "output/final_reader/连云港市志_全书.html:26027 同段已校为 `流传万世，为千百万人民瞻仰敬礼。抗战五周年之际`",
    },
]

BAD_PATTERNS = ["流传方世", "瞻仰敬</p><p>战五周年", "瞻仰敬\n战五周年"]
CHECK_TARGETS = sorted({target for item in REPLACEMENTS for target in item["targets"]} | {"output/final_reader/连云港市志_全书.html"})


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
    report = {"batch": 267, "total": total, "changes": changes, "residuals": residuals}

    report_md = ROOT / "output/reports/lower_liuchuan_wanshi_batch267_20260707.md"
    report_json = ROOT / "output/reports/lower_liuchuan_wanshi_batch267_20260707.json"
    lines = [
        "# 下册流传万世跨层一致性补修 batch267",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册人物附录抗日烈士纪念塔序文同段。",
        "- 原则：当前全书 HTML 已有同段校正文，本批将下册 HTML、下册源稿和全书正文汇总追平；页级 OCR 未命中完整短语，因此不扩大处理。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for row in changes:
        if row["count"]:
            old = row["old"].replace("\n", "\\n")
            new = row["new"].replace("\n", "\\n")
            lines.append(f"- `{row['path']}`：`{old}` -> `{new}`；次数 {row['count']}；依据 `{row['evidence']}`")
    lines.extend(["", "## 残留计数", ""])
    if residuals:
        for rel, hits in residuals.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批坏短语在目标文件和当前全书 HTML 中均为 0。")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
