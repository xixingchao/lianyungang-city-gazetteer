from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    {
        "old": "第兰营部署在青口与赣榆城之间",
        "new": "第三营部署在青口与赣榆城之间",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0162.txt:35-39",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_全书.html",
            "output/final_reader/连云港市志_下册.html",
        ],
    },
    {
        "old": "1984年5月加人中国科技报研究会",
        "new": "1984年5月加入中国科技报研究会",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0137.txt:14-15",
        "targets": [
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
        ],
    },
    {
        "old": "将所得钱财为已有",
        "new": "将所得钱财攫为己有",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0128.txt:26-27",
        "targets": [
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
            "output/final_reader/连云港市志_下册.html",
        ],
    },
    {
        "old": "女爱国知名人土进行调查",
        "new": "女爱国知名人士进行调查",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0337.txt:16-18",
        "targets": [
            "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
            "workbench/body_chapters/连云港市志_全书_正文汇总.md",
        ],
    },
]

BAD_PATTERNS = [
    "第兰营",
    "加人中国科技报研究会",
    "将所得钱财为已有",
    "女爱国知名人土进行调查",
]

CHECK_TARGETS = [
    "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
    "output/final_reader/连云港市志_全书.html",
    "output/final_reader/连云港市志_下册.html",
]


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
        "batch": 264,
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "skipped": [
            {
                "text": "自已在社会中影响",
                "reason": "page-level PaddleOCR still reads 自已, so no correction was made in this batch.",
                "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0128.txt:24-27",
            }
        ],
    }

    report_md = ROOT / "output/reports/lower_source_backed_residues_batch264_20260707.md"
    report_json = ROOT / "output/reports/lower_source_backed_residues_batch264_20260707.json"
    lines = [
        "# 下册源证据残留定点补修 batch264",
        "",
        f"- 修复总数：{total}",
        "- 范围：赣榆战役部署、科技汇报入会句、连云报钱财句、妇联统战联络句。",
        "- 原则：只处理页级 PaddleOCR 已给出明确读法的残留；未证实的 `自已在社会中影响` 未改。",
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
        "- `自已在社会中影响`：`workbench/ocr/paddle_ocr/下/part02/page_0128.txt:26` 仍读作 `自已`，本批不凭常识改。",
    ])
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
