from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

OLD = "现有隐惠，及时建议和协助监管场所消除隐惠"
NEW = "现有隐患，及时建议和协助监管场所消除隐患"
EVIDENCE = "workbench/ocr/paddle_ocr/下/part01/page_0110.txt:37"

TARGETS = [
    Path("workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md"),
    Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
    Path("output/final_reader/连云港市志_下册.html"),
    Path("output/final_reader/连云港市志_全书.html"),
]


def main():
    changes = []
    for rel_path in TARGETS:
        path = ROOT / rel_path
        text = path.read_text(encoding="utf-8")
        count = text.count(OLD)
        if count:
            text = text.replace(OLD, NEW)
            path.write_text(text, encoding="utf-8", newline="")
        changes.append({"path": str(rel_path), "old": OLD, "new": NEW, "count": count, "evidence": EVIDENCE})

    total = sum(item["count"] for item in changes)
    report_md = ROOT / "output/reports/lower_supervision_hidden_danger_batch245_20260707.md"
    report_json = ROOT / "output/reports/lower_supervision_hidden_danger_batch245_20260707.json"

    lines = [
        "# 下册监所检察隐患残留修复 batch245",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册监所检察段正文源稿、全书正文汇总及当前下册/全书阅读稿。",
        "- 原则：仅按页级 PaddleOCR 明确支持的单句残留修复，不改 OCR 原始层，不处理 obsolete 旧阅读稿。",
        "",
        "## 证据",
        "",
        f"- `{EVIDENCE}`：`1964年，监所检察发现有隐患，及时建议和协助监管场所消除隐患，未发生在押犯逃跑、自杀等事件。`",
        "",
        "## 替换明细",
    ]
    for item in changes:
        lines.append(f"- `{item['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}")

    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps({"total": total, "changes": changes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    for item in changes:
        if item["count"]:
            print(item["path"])


if __name__ == "__main__":
    main()
