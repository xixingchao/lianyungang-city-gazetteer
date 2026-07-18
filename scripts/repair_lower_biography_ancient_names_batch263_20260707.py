from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    ("钟离味", "钟离昧", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:8,10-15"),
    ("荣阳东", "荥阳东", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:9"),
    ("以方金买通说客", "以万金买通说客", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:10"),
    ("反间手楚军中", "反间于楚军中", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:10"),
    ("龙直周殷", "龙苴、周殷", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:10-11"),
    ("龙直周\n殷", "龙苴、周\n殷", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:10-11"),
    ("龙直周</p><p>殷", "龙苴、周</p><p>殷", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:10-11"),
    ("诸候于陈地", "诸侯于陈地", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:13"),
    ("将钟离昧速\n捕", "将钟离昧逮\n捕", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:12-13"),
    ("把我杀了去见\n：汉王", "把我杀了去见\n汉王", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:14-15"),
    ("遂自匆", "遂自刎", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:15"),
    ("下邸", "下邳", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:19"),
    ("和内疚", "和内疚", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:24"),
    ("和内，", "和内疚，", "workbench/ocr/paddle_ocr/下/part02/page_0343.txt:24"),
    ("出任袜陵令", "出任秣陵令", "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:4"),
    ("刘子项的前军参军", "刘子顼的前军参军", "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:4"),
    ("子响应", "子顼响应", "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:5"),
    ("《来书》、《南史》", "《宋书》、《南史》", "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:6"),
    ("诗赋和文，尤善乐府", "诗赋和骈文，尤善乐府", "workbench/ocr/paddle_ocr/下/part02/page_0344.txt:6"),
]

TASKS = [
    Path("workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"),
    Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
    Path("output/final_reader/连云港市志_全书.html"),
    Path("output/final_reader/连云港市志_下册.html"),
]

BAD = [old for old, _, _ in REPLACEMENTS if old != "和内疚"]


def main():
    changes = []
    for rel in TASKS:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        file_changes = []
        for old, new, evidence in REPLACEMENTS:
            count = text.count(old)
            if count and old != new:
                text = text.replace(old, new)
            file_changes.append({"old": old, "new": new, "count": count, "evidence": evidence})
        path.write_text(text, encoding="utf-8", newline="")
        changes.append({"path": str(rel), "changes": file_changes})

    residuals = {}
    for rel in TASKS:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        hits = {bad: text.count(bad) for bad in BAD if text.count(bad)}
        if hits:
            residuals[str(rel)] = hits

    total = sum(item["count"] for file in changes for item in file["changes"] if item["old"] != item["new"])
    report_md = ROOT / "output/reports/lower_biography_ancient_names_batch263_20260707.md"
    report_json = ROOT / "output/reports/lower_biography_ancient_names_batch263_20260707.json"
    lines = [
        "# 下册人物传略古代人名与史籍残留修复 batch263",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册第六十卷人物传略钟离昧、糜竺、鲍照段，下册源稿、全书汇总及当前全书/下册阅读稿。",
        "- 原则：只处理 `page_0343`、`page_0344` 页级 PaddleOCR 明确读出的字词。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for file in changes:
        lines.append(f"\n### {file['path']}")
        for item in file["changes"]:
            if item["old"] == item["new"]:
                continue
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
