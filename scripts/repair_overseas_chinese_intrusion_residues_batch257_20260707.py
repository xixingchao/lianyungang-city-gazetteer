from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

OVERSEAS_REPLACEMENTS = [
    ("侨着", "侨眷", "workbench/ocr/paddle_ocr/下/part01/page_0297.txt:26;page_0298.txt:16-28;page_0299.txt:13-33;page_0300.txt:4-39;中/part02/page_0474.txt:11-13"),
    ("侨卷", "侨眷", "workbench/ocr/paddle_ocr/下/part01/page_0284.txt:27;page_0299.txt:13-14"),
    ("侨券", "侨眷", "workbench/ocr/paddle_ocr/下/part01/page_0298.txt:20-28;page_0299.txt:13-14"),
    ("侨誉", "侨眷", "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:21-22"),
    ("着属", "眷属", "workbench/ocr/paddle_ocr/下/part01/page_0298.txt:21;page_0299.txt:21"),
    ("三、侨\n", "三、侨眷\n", "workbench/ocr/paddle_ocr/下/part01/page_0298.txt:20"),
    ("三、侨</p>", "三、侨眷</p>", "workbench/ocr/paddle_ocr/下/part01/page_0298.txt:20"),
    ("侨寻亲", "侨眷寻亲", "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:27"),
    ("归侨、\n侨和旅外", "归侨、\n侨眷和旅外", "workbench/ocr/paddle_ocr/下/part01/page_0299.txt:32"),
    ("侨的合法权益", "侨眷的合法权益", "workbench/ocr/paddle_ocr/中/part02/page_0474.txt:11"),
]

GEO_REPLACEMENTS = [
    ("慢入岩", "侵入岩", "workbench/body_chapters/paddle_上/第一卷_自然环境.md:479"),
    ("侵人岩", "侵入岩", "workbench/body_chapters/paddle_上/第一卷_自然环境.md:479-480;493"),
    ("侵人于", "侵入于", "workbench/body_chapters/paddle_上/第一卷_自然环境.md:480"),
]

TASKS = [
    {
        "path": Path("workbench/body_chapters/第三十卷至第四十二卷（中part02）.md"),
        "replacements": [
            ("侨着", "侨眷", "workbench/ocr/paddle_ocr/中/part02/page_0474.txt:13"),
            ("侨的合法权益", "侨眷的合法权益", "workbench/ocr/paddle_ocr/中/part02/page_0474.txt:11"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"),
        "replacements": OVERSEAS_REPLACEMENTS,
    },
    {
        "path": Path("workbench/body_chapters/上/第一卷_自然环境.md"),
        "replacements": GEO_REPLACEMENTS,
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": OVERSEAS_REPLACEMENTS + GEO_REPLACEMENTS,
    },
    {
        "path": Path("output/final_reader/连云港市志_中册.html"),
        "replacements": [
            ("侨着", "侨眷", "workbench/ocr/paddle_ocr/中/part02/page_0474.txt:13"),
            ("侨的合法权益", "侨眷的合法权益", "workbench/ocr/paddle_ocr/中/part02/page_0474.txt:11"),
        ],
    },
    {
        "path": Path("output/final_reader/连云港市志_下册.html"),
        "replacements": OVERSEAS_REPLACEMENTS + GEO_REPLACEMENTS,
    },
    {
        "path": Path("output/final_reader/连云港市志_全书.html"),
        "replacements": [
            ("侨的合法权益", "侨眷的合法权益", "workbench/ocr/paddle_ocr/中/part02/page_0474.txt:11"),
        ],
    },
]

BAD = sorted({old for task in TASKS for old, _, _ in task["replacements"]})


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
    report_md = ROOT / "output/reports/overseas_chinese_intrusion_residues_batch257_20260707.md"
    report_json = ROOT / "output/reports/overseas_chinese_intrusion_residues_batch257_20260707.json"
    lines = [
        "# 侨眷与侵入岩残留修复 batch257",
        "",
        f"- 修复总数：{total}",
        "- 范围：中册致公党段、下册侨务段、上册自然环境地质段、全书正文汇总及当前阅读稿。",
        "- 原则：只处理页级 PaddleOCR 或 PaddleOCR 正文汇总明确支持的 `侨眷/眷属/侵入` 残留，不做单字泛替换。",
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
