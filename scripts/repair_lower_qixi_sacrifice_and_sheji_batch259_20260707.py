from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"),
        "replacements": [
            ("栖牲", "牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0089.txt:17;page_0377.txt:23-24;page_0401.txt:126-134;page_0404.txt:77-130;page_0406.txt:97-123;page_0407.txt:25-31;page_0408.txt:131-136"),
            ("舍已救人", "舍己救人", "workbench/ocr/paddle_ocr/下/part02/page_0089.txt:19;page_0378.txt:28-30"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"),
        "replacements": [
            ("舍已救人", "舍己救人", "output/final_reader/连云港市志_全书.html:20899;杨佃池同段为英雄少年舍己救人固定语"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("栖牲", "牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0089.txt:17;page_0377.txt:23-24;page_0401.txt:126-134;page_0404.txt:77-130;page_0406.txt:97-123;page_0407.txt:25-31;page_0408.txt:131-136"),
            ("舍已救人", "舍己救人", "workbench/ocr/paddle_ocr/下/part02/page_0089.txt:19;page_0378.txt:28-30;output/final_reader/连云港市志_全书.html:20899"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_下册.html"),
        "replacements": [
            ("栖牲", "牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0089.txt:17;page_0377.txt:23-24;page_0401.txt:126-134;page_0404.txt:77-130;page_0406.txt:97-123;page_0407.txt:25-31;page_0408.txt:131-136"),
            ("舍已救人", "舍己救人", "workbench/ocr/paddle_ocr/下/part02/page_0089.txt:19;page_0378.txt:28-30;output/final_reader/连云港市志_全书.html:20899"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_全书.html"),
        "replacements": [
            ("舍已救人", "舍己救人", "workbench/ocr/paddle_ocr/下/part02/page_0089.txt:19;page_0378.txt:28-30;output/final_reader/连云港市志_全书.html:20899"),
        ],
    },
]

BAD = ["栖牲", "舍已救人"]


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
    report_md = ROOT / "output/reports/lower_qixi_sacrifice_and_sheji_batch259_20260707.md"
    report_json = ROOT / "output/reports/lower_qixi_sacrifice_and_sheji_batch259_20260707.json"
    lines = [
        "# 下册栖牲与舍已残留修复 batch259",
        "",
        f"- 修复总数：{total}",
        "- 范围：当前下册阅读稿、当前全书阅读稿、下册正文源稿、全书正文汇总。",
        "- 原则：仅处理可由页级 PaddleOCR 或同一人物同一事迹语境支撑的固定残留；不触碰 obsolete 旧文件。",
        "- 图片处理：未打开、展示或嵌入图片。",
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
