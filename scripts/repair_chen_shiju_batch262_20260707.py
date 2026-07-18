from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/上/总述与大事记.md"),
        "replacements": [
            ("陈士渠司令员", "陈士榘司令员", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243"),
            ("司令员陈士渠将", "司令员陈士榘将", "workbench/body_chapters/paddle_上/总述与大事记.md:1261"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_上册_正文汇总.md"),
        "replacements": [
            ("陈士渠司令员", "陈士榘司令员", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243"),
            ("司令员陈士渠将", "司令员陈士榘将", "workbench/body_chapters/paddle_上/总述与大事记.md:1261"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第三十卷至第四十二卷（中part02）.md"),
        "replacements": [
            ("司令员陈士渠指挥赣榆战役", "司令员陈士榘指挥赣榆战役", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243 同人同役"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"),
        "replacements": [
            ("滨海军区司令员陈士、政治委员符竹庭指挥", "滨海军区司令员陈士榘、政治委员符竹庭指挥", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243 同一赣榆战役司令员"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md"),
        "replacements": [
            ("陈士渠题词", "陈士榘题词", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243;同一滨海军区司令员姓名"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("陈士渠司令员", "陈士榘司令员", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243"),
            ("司令员陈士渠将", "司令员陈士榘将", "workbench/body_chapters/paddle_上/总述与大事记.md:1261"),
            ("司令员陈士渠指挥赣榆战役", "司令员陈士榘指挥赣榆战役", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243 同人同役"),
            ("滨海军区司令员陈士、政治委员符竹庭指挥", "滨海军区司令员陈士榘、政治委员符竹庭指挥", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243 同一赣榆战役司令员"),
            ("陈士渠题词", "陈士榘题词", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243;同一滨海军区司令员姓名"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_全书.html"),
        "replacements": [
            ("陈士渠司令员", "陈士榘司令员", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243"),
            ("司令员陈士渠将", "司令员陈士榘将", "workbench/body_chapters/paddle_上/总述与大事记.md:1261"),
            ("司令员陈士渠指挥赣榆战役", "司令员陈士榘指挥赣榆战役", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243 同人同役"),
            ("滨海军区司令员陈士、政治委员符竹庭指挥", "滨海军区司令员陈士榘、政治委员符竹庭指挥", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243 同一赣榆战役司令员"),
            ("陈士渠题词", "陈士榘题词", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243;同一滨海军区司令员姓名"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_中册.html"),
        "replacements": [
            ("司令员陈士渠指挥赣榆战役", "司令员陈士榘指挥赣榆战役", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243 同人同役"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_下册.html"),
        "replacements": [
            ("滨海军区司令员陈士、政治委员符竹庭指挥", "滨海军区司令员陈士榘、政治委员符竹庭指挥", "workbench/body_chapters/paddle_上/总述与大事记.md:1242-1243 同一赣榆战役司令员"),
        ],
    },
]

BAD = ["陈士渠", "陈士、政治委员"]


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
    report_md = ROOT / "output/reports/chen_shiju_batch262_20260707.md"
    report_json = ROOT / "output/reports/chen_shiju_batch262_20260707.json"
    lines = [
        "# 陈士榘姓名残留定点修复 batch262",
        "",
        f"- 修复总数：{total}",
        "- 范围：上册大事记源稿、上册/全书汇总、中册政府源稿、下册军事/人物源稿及当前全书/中册/下册阅读稿。",
        "- 原则：依据上册 PaddleOCR 正文汇总中同一人物、同一赣榆战役和同一滨海军区司令员语境，定点修复 `陈士渠` 与漏字 `陈士、政治委员`。",
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
