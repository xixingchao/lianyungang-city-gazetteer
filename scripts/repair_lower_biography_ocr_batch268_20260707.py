from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

ALL_TARGETS = [
    "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
    "output/final_reader/连云港市志_全书.html",
    "output/final_reader/连云港市志_下册.html",
]

REPLACEMENTS = [
    {
        "old": "作文劲刚健",
        "new": "作文遒劲刚健",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:9",
        "targets": ALL_TARGETS,
    },
    {
        "old": "太子中充",
        "new": "太子中允",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:13",
        "targets": ALL_TARGETS,
    },
    {
        "old": "朱仁宗赞赏",
        "new": "宋仁宗赞赏",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:14",
        "targets": ALL_TARGETS,
    },
    {
        "old": "徽献阁待制",
        "new": "徽猷阁待制",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:17,32",
        "targets": ALL_TARGETS,
    },
    {
        "old": "屯驻水军三于备战",
        "new": "屯驻水军三千备战",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:33",
        "targets": ALL_TARGETS,
    },
    {
        "old": "兵士人卫京师",
        "new": "兵士入卫京师",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:22-23",
        "targets": ALL_TARGETS,
    },
    {
        "old": "随徽宗、钦宗被携。北上",
        "new": "随徽宗、钦宗被掳。北上",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:24",
        "targets": ALL_TARGETS,
    },
    {
        "old": "扼皖而死",
        "new": "扼吭而死",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:25",
        "targets": ALL_TARGETS,
    },
    {
        "old": "魏胜（1120～1165）学彦威",
        "new": "魏胜（1120～1165）字彦威",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0345.txt:12",
        "targets": ALL_TARGETS,
    },
    {
        "old": "南朱绍兴三十一年",
        "new": "南宋绍兴三十一年",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0158.txt:28; workbench/ocr/paddle_ocr/下/part02/page_0345.txt:12",
        "targets": ALL_TARGETS,
    },
    {
        "old": "三干义士",
        "new": "三千义士",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0345.txt:13",
        "targets": ALL_TARGETS,
    },
    {
        "old": "收复水，攻克海州",
        "new": "收复涟水，攻克海州",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0345.txt:13",
        "targets": ALL_TARGETS,
    },
    {
        "old": "派十兵攻海州",
        "new": "派十万兵攻海州",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0345.txt:14",
        "targets": ALL_TARGETS,
    },
    {
        "old": "魏巍\n胜名声大振",
        "new": "魏\n胜名声大振",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0345.txt:14-15",
        "targets": ALL_TARGETS,
    },
    {
        "old": "魏巍</p><p>胜名声大振",
        "new": "魏</p><p>胜名声大振",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0345.txt:14-15",
        "targets": ALL_TARGETS,
    },
    {
        "old": "先派兵数方攻打海州",
        "new": "先派兵数万攻打海州",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0345.txt:16",
        "targets": ALL_TARGETS,
    },
    {
        "old": "后金劝降巍胜",
        "new": "后金劝降魏胜",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0345.txt:17",
        "targets": ALL_TARGETS,
    },
    {
        "old": "可载\n辙重",
        "new": "可载\n辎重",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0345.txt:18-19",
        "targets": ALL_TARGETS,
    },
    {
        "old": "可载</p><p>辙重",
        "new": "可载</p><p>辎重",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0345.txt:18-19",
        "targets": ALL_TARGETS,
    },
    {
        "old": "车发射，可射200步远",
        "new": "弩车发射，可射200步远",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0345.txt:19",
        "targets": ALL_TARGETS,
    },
    {
        "old": "龙直、四队撤乡建镇",
        "new": "龙苴、四队撤乡建镇",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0019.txt:36",
        "targets": ALL_TARGETS,
    },
    {
        "old": "白塔璋、温泉、桃林",
        "new": "白塔埠、温泉、桃林",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0019.txt:38-39",
        "targets": ALL_TARGETS,
    },
    {
        "old": "杨集、龙、四队共16个镇",
        "new": "杨集、龙苴、四队共16个镇",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0019.txt:39",
        "targets": ALL_TARGETS,
    },
    {
        "old": "莱芜、孟良周、济南",
        "new": "莱芜、孟良崮、济南",
        "evidence": "workbench/ocr/paddle_ocr/下/part01/page_0021.txt:19",
        "targets": ALL_TARGETS,
    },
    {
        "old": "沙雍积沸，南溃北决",
        "new": "沙壅积滞，南溃北决",
        "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0346.txt:34",
        "targets": ALL_TARGETS,
    },
]

BAD_PATTERNS = [item["old"] for item in REPLACEMENTS if item["old"] != "车发射，可射200步远"] + [
    "在后，车发射，可射200步远",
    "在后，车发射，可射",
]
CHECK_TARGETS = ALL_TARGETS


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
        "batch": 268,
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "skipped": [
            {
                "text": "张敌万",
                "reason": "page-level OCR still reads 张敌万; no source-backed correction was available in this batch.",
                "evidence": "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:39",
            }
        ],
    }

    report_md = ROOT / "output/reports/lower_biography_ocr_batch268_20260707.md"
    report_json = ROOT / "output/reports/lower_biography_ocr_batch268_20260707.json"
    lines = [
        "# 下册人物传略与民政源证据 OCR 残留补修 batch268",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册张叔夜、石延年、胡松年、魏胜传略，以及民政乡镇名、拥军支前、江之范段的少量源证据残留。",
        "- 原则：只处理页级 PaddleOCR 已给出明确读法的精确短语；未证实的 `张敌万` 未改。",
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
        "- `张敌万`：`workbench/ocr/paddle_ocr/下/part02/page_0344.txt:39` 仍读作 `张敌万`，本批没有更强证据，暂不修改。",
    ])
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
