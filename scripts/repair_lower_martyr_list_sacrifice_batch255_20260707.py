from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"),
        "replacements": [
            ("斗牺性", "斗牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:63"),
            ("援朝战争牺性在", "援朝战争牺牲在", "workbench/ocr/paddle_ocr/下/part02/page_0403.txt:144"),
            ("台乡赵巷\n牺性", "台乡赵巷\n牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0404.txt:154-160"),
            ("王维林\n1910\n1930\n牺性", "王维林\n1910\n1930\n牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0404.txt:172-176"),
            ("徐殿喜\n1894\n1929\n台乡薄巷\n牺性", "徐殿喜\n1894\n1929\n台乡薄巷\n牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0405.txt:49-55"),
            ("司务长\n牺性", "司务长\n牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0405.txt:126-133"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("斗牺性", "斗牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:63"),
            ("援朝战争牺性在", "援朝战争牺牲在", "workbench/ocr/paddle_ocr/下/part02/page_0403.txt:144"),
            ("台乡赵巷\n牺性", "台乡赵巷\n牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0404.txt:154-160"),
            ("王维林\n1910\n1930\n牺性", "王维林\n1910\n1930\n牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0404.txt:172-176"),
            ("徐殿喜\n1894\n1929\n台乡薄巷\n牺性", "徐殿喜\n1894\n1929\n台乡薄巷\n牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0405.txt:49-55"),
            ("司务长\n牺性", "司务长\n牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0405.txt:126-133"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_下册.html"),
        "replacements": [
            ("斗牺性", "斗牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0401.txt:63"),
            ("援朝战争牺性在", "援朝战争牺牲在", "workbench/ocr/paddle_ocr/下/part02/page_0403.txt:144"),
            ("台乡赵巷</p><p>牺性", "台乡赵巷</p><p>牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0404.txt:154-160"),
            ("王维林</p><p>1910</p><p>1930</p><p>牺性", "王维林</p><p>1910</p><p>1930</p><p>牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0404.txt:172-176"),
            ("徐殿喜</p><p>1894</p><p>1929</p><p>台乡薄巷</p><p>牺性", "徐殿喜</p><p>1894</p><p>1929</p><p>台乡薄巷</p><p>牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0405.txt:49-55"),
            ("司务长</p><p>牺性", "司务长</p><p>牺牲", "workbench/ocr/paddle_ocr/下/part02/page_0405.txt:126-133"),
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

    residuals = {}
    for rel in sorted({str(task["path"]) for task in TASKS}):
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        hits = {bad: text.count(bad) for bad in BAD if text.count(bad)}
        if hits:
            residuals[rel] = hits

    total = sum(item["count"] for file in changes for item in file["changes"])
    report_md = ROOT / "output/reports/lower_martyr_list_sacrifice_batch255_20260707.md"
    report_json = ROOT / "output/reports/lower_martyr_list_sacrifice_batch255_20260707.json"
    lines = [
        "# 下册烈士名录牺牲残留修复 batch255",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册革命烈士简况表残留短语、全书正文汇总及当前下册阅读稿。",
        "- 原则：只处理页级 PaddleOCR 在同页同名录中明确为 `牺牲` 的残留；铭文 `牺性精神` 暂不改。",
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
