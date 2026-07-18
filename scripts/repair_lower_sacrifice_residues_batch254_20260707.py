from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"),
        "replacements": [
            ("团长宋耀南牺性", "团长宋耀南牺牲", "workbench/ocr/paddle_ocr/下/part01/page_0173.txt:37-40"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"),
        "replacements": [
            ("在李\n捻战斗中牺性", "在李\n埝战斗中牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0358.txt:23-24"),
            ("田守尧和爱人陈洛涟同时牺性", "田守尧和爱人陈洛涟同时牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0371.txt:36"),
            ("牺性时所在", "牺牲时所在", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:19;page_0403.txt:13"),
            ("牺性时间、", "牺牲时间、", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:20;page_0403.txt:14"),
            ("战役牺性", "战役牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0406.txt:30-40"),
            ("战场牺性", "战场牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:121;page_0403.txt:33"),
            ("战斗牺性", "战斗牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:63-92;page_0402.txt:31-145"),
            ("因公牺性", "因公牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0404.txt:84-98;page_0407.txt:72"),
            ("被捕牺性", "被捕牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:101;page_0402.txt:155"),
            ("参战牺性", "参战牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0405.txt:154"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("团长宋耀南牺性", "团长宋耀南牺牲", "workbench/ocr/paddle_ocr/下/part01/page_0173.txt:37-40"),
            ("在李\n捻战斗中牺性", "在李\n埝战斗中牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0358.txt:23-24"),
            ("田守尧和爱人陈洛涟同时牺性", "田守尧和爱人陈洛涟同时牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0371.txt:36"),
            ("牺性时所在", "牺牲时所在", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:19;page_0403.txt:13"),
            ("牺性时间、", "牺牲时间、", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:20;page_0403.txt:14"),
            ("战役牺性", "战役牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0406.txt:30-40"),
            ("战场牺性", "战场牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:121;page_0403.txt:33"),
            ("战斗牺性", "战斗牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:63-92;page_0402.txt:31-145"),
            ("因公牺性", "因公牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0404.txt:84-98;page_0407.txt:72"),
            ("被捕牺性", "被捕牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:101;page_0402.txt:155"),
            ("参战牺性", "参战牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0405.txt:154"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_下册.html"),
        "replacements": [
            ("团长宋耀南牺性", "团长宋耀南牺牲", "workbench/ocr/paddle_ocr/下/part01/page_0173.txt:37-40"),
            ("在李</p><p>捻战斗中牺性", "在李</p><p>埝战斗中牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0358.txt:23-24"),
            ("田守尧和爱人陈洛涟同时牺性", "田守尧和爱人陈洛涟同时牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0371.txt:36"),
            ("牺性时所在", "牺牲时所在", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:19;page_0403.txt:13"),
            ("牺性时间、", "牺牲时间、", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:20;page_0403.txt:14"),
            ("战役牺性", "战役牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0406.txt:30-40"),
            ("战场牺性", "战场牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:121;page_0403.txt:33"),
            ("战斗牺性", "战斗牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:63-92;page_0402.txt:31-145"),
            ("因公牺性", "因公牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0404.txt:84-98;page_0407.txt:72"),
            ("被捕牺性", "被捕牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:101;page_0402.txt:155"),
            ("参战牺性", "参战牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0405.txt:154"),
        ],
    },
]

BAD = [old for task in TASKS for old, _, _ in task["replacements"]]


def main():
    changes = []
    for task in TASKS:
        path = ROOT / task["path"]
        text = path.read_text(encoding="utf-8")
        file_changes = []
        for old, new, evidence in task["replacements"]:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
            file_changes.append({"old": old, "new": new, "count": count, "evidence": evidence})
        path.write_text(text, encoding="utf-8", newline="")
        changes.append({"path": str(task["path"]), "changes": file_changes})

    target_paths = sorted({str(task["path"]) for task in TASKS})
    residuals = {}
    for rel in target_paths:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        hits = {bad: text.count(bad) for bad in BAD if text.count(bad)}
        if hits:
            residuals[rel] = hits

    total = sum(item["count"] for file in changes for item in file["changes"])
    report_md = ROOT / "output/reports/lower_sacrifice_residues_batch254_20260707.md"
    report_json = ROOT / "output/reports/lower_sacrifice_residues_batch254_20260707.json"
    lines = [
        "# 下册牺牲残留修复 batch254",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册军事/人物传记、革命烈士简况表残留短语、全书正文汇总及当前下册阅读稿。",
        "- 原则：只处理页级 PaddleOCR 明确为 `牺牲` 的短语；不对烈士名录错位行做整页重构。",
        "",
        "## 替换明细",
    ]
    for file in changes:
        lines.append(f"\n### {file['path']}")
        for item in file["changes"]:
            lines.append(f"- `{item['old']}` -> `{item['new']}`；次数 {item['count']}；证据 `{item['evidence']}`")
    lines.extend(["", "## 残留计数", ""])
    if residuals:
        for rel, hits in residuals.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批坏短语在目标文件中均为 0。")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps({"total": total, "changes": changes, "residuals": residuals}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
