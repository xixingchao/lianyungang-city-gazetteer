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
        "old": "魏胜军人城",
        "new": "魏胜军入城",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0158.txt:34",
    },
    {
        "old": "长驱直人，所向披靡",
        "new": "长驱直入，所向披靡",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0158.txt:34",
    },
    {
        "old": "蒙恬镇国领兵余攻海州",
        "new": "蒙恬镇国领兵万余攻海州",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0158.txt:36",
    },
    {
        "old": "落人重围",
        "new": "落入重围",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0158.txt:39",
    },
    {
        "old": "身先土卒",
        "new": "身先士卒",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0158.txt:39",
    },
    {
        "old": "冲人敌阵",
        "new": "冲入敌阵",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0158.txt:39",
    },
    {
        "old": "直人海州境",
        "new": "直入海州境",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:19",
    },
    {
        "old": "苏\n中抗甘根据地",
        "new": "苏\n中抗日根据地",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0367.txt:16",
    },
    {
        "old": "谈判桌上签学",
        "new": "谈判桌上签字",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0367.txt:19",
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
        "batch": 269,
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "skipped": [
            {
                "text": "热忧",
                "reason": "No page-level OCR evidence was located in this pass; not changed.",
            },
            {
                "text": "三野十兵团 / 十兵团",
                "reason": "Likely shorthand for 第十兵团; not changed without source contradiction.",
            },
        ],
    }

    report_md = ROOT / "output/reports/lower_source_backed_residues_batch269_20260707.md"
    report_json = ROOT / "output/reports/lower_source_backed_residues_batch269_20260707.json"
    lines = [
        "# 下册军事与人物源证据残留补修 batch269",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册军事卷魏胜抗金段、人物传略张叔夜/惠浴宇段。",
        "- 原则：只处理页级 PaddleOCR 已给出明确读法的精确短语；未证实项暂留。",
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
        "- `热忧`：本轮未定位到页级 OCR 证据，暂不修改。",
        "- `三野十兵团` / `十兵团`：可能是第十兵团简称，无源证据矛盾，暂不修改。",
    ])
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
