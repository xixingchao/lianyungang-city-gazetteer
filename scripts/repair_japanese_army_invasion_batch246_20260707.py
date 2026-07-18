from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OLD = "日军人侵"
NEW = "日军入侵"

EVIDENCE = [
    "workbench/ocr/paddle_ocr/中/part02/page_0032.txt:102",
    "workbench/ocr/paddle_ocr/上/part03/page_0061.txt:55",
    "workbench/ocr/paddle_ocr/上/part03/page_0130.txt:23",
    "workbench/ocr/paddle_ocr/上/part03/page_0207.txt:4",
    "workbench/ocr/paddle_ocr/下/part01/page_0112.txt:26",
    "workbench/ocr/paddle_ocr/下/part01/page_0283.txt:18",
]

TARGETS = [
    Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
    Path("workbench/body_chapters/第三十卷至第四十二卷（中part02）.md"),
    Path("workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"),
    Path("workbench/body_chapters/上/第十卷至第十六卷（part03）.md"),
    Path("workbench/body_chapters/连云港市志_上册_正文汇总.md"),
    Path("output/final_reader/连云港市志_全书.html"),
    Path("output/final_reader/连云港市志_中册.html"),
    Path("output/final_reader/连云港市志_下册.html"),
]


def main():
    changes = []
    for rel_path in TARGETS:
        path = ROOT / rel_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        count = text.count(OLD)
        if count:
            path.write_text(text.replace(OLD, NEW), encoding="utf-8", newline="")
        changes.append({"path": str(rel_path), "old": OLD, "new": NEW, "count": count})

    total = sum(item["count"] for item in changes)
    report_md = ROOT / "output/reports/japanese_army_invasion_batch246_20260707.md"
    report_json = ROOT / "output/reports/japanese_army_invasion_batch246_20260707.json"

    lines = [
        "# 日军入侵残留修复 batch246",
        "",
        f"- 修复总数：{total}",
        "- 范围：当前正文源稿、分册汇总、全书汇总及当前中册/下册/全书阅读稿。",
        "- 原则：仅替换页级 PaddleOCR 明确支持的短语 `日军人侵`，不扩展到其他 `人侵` 形态，不处理 obsolete。",
        "",
        "## 证据",
    ]
    for item in EVIDENCE:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("## 替换明细")
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}")

    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps({"total": total, "evidence": EVIDENCE, "changes": changes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    for item in changes:
        if item["count"]:
            print(item["path"])


if __name__ == "__main__":
    main()
