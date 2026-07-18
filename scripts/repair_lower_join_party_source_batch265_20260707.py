from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    {
        "old": "加人中国共产党",
        "new": "加入中国共产党",
        "evidence": [
            "workbench/ocr/paddle_ocr/下/part01/page_0300.txt:31",
            "workbench/ocr/paddle_ocr/下/part01/page_0321.txt:19",
            "workbench/ocr/paddle_ocr/下/part02/page_0357.txt:6",
            "workbench/ocr/paddle_ocr/下/part02/page_0359.txt:17",
            "workbench/ocr/paddle_ocr/下/part02/page_0362.txt:36",
            "workbench/ocr/paddle_ocr/下/part02/page_0365.txt:21,30",
            "workbench/ocr/paddle_ocr/下/part02/page_0366.txt:7,33",
            "workbench/ocr/paddle_ocr/下/part02/page_0369.txt:34",
            "workbench/ocr/paddle_ocr/下/part02/page_0370.txt:40",
            "workbench/ocr/paddle_ocr/下/part02/page_0371.txt:19",
            "workbench/ocr/paddle_ocr/下/part02/page_0372.txt:7",
            "workbench/ocr/paddle_ocr/下/part02/page_0373.txt:24",
            "workbench/ocr/paddle_ocr/下/part02/page_0376.txt:6",
            "workbench/ocr/paddle_ocr/下/part02/page_0379.txt:8",
            "workbench/ocr/paddle_ocr/下/part02/page_0384.txt:29",
            "workbench/ocr/paddle_ocr/下/part02/page_0387.txt:16,28",
            "workbench/ocr/paddle_ocr/下/part02/page_0390.txt:17,37",
            "workbench/ocr/paddle_ocr/下/part02/page_0391.txt:9,12,14,40",
            "workbench/ocr/paddle_ocr/下/part02/page_0392.txt:15,24",
            "workbench/ocr/paddle_ocr/下/part02/page_0395.txt:5",
            "workbench/ocr/paddle_ocr/下/part02/page_0396.txt:16",
            "workbench/ocr/paddle_ocr/下/part02/page_0397.txt:9,17",
            "workbench/ocr/paddle_ocr/下/part02/page_0398.txt:41",
            "workbench/ocr/paddle_ocr/下/part02/page_0399.txt:13,37",
        ],
    },
    {
        "old": "加人中国共产主义青年团",
        "new": "加入中国共产主义青年团",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0378.txt:25"],
    },
    {
        "old": "加人中国国民党",
        "new": "加入中国国民党",
        "evidence": ["workbench/ocr/paddle_ocr/下/part02/page_0354.txt:26"],
    },
]

TARGETS = [
    "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
]

READERS = [
    "output/final_reader/连云港市志_全书.html",
    "output/final_reader/连云港市志_下册.html",
]


def main():
    changes = []
    for rel in TARGETS:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8", errors="ignore")
        file_changes = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            file_changes.append({
                "old": item["old"],
                "new": item["new"],
                "count": count,
                "evidence": item["evidence"],
            })
        path.write_text(text, encoding="utf-8", newline="")
        changes.append({"path": rel, "changes": file_changes})

    bad = [item["old"] for item in REPLACEMENTS]
    residuals = {}
    for rel in TARGETS + READERS:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        hits = {pat: text.count(pat) for pat in bad if text.count(pat)}
        if hits:
            residuals[rel] = hits

    total = sum(item["count"] for file in changes for item in file["changes"])
    report = {
        "batch": 265,
        "total": total,
        "changes": changes,
        "residuals": residuals,
        "scope_note": "Only complete phrases were replaced; generic 加人/进人 were not touched.",
    }

    report_md = ROOT / "output/reports/lower_join_party_source_batch265_20260707.md"
    report_json = ROOT / "output/reports/lower_join_party_source_batch265_20260707.json"
    lines = [
        "# 下册入党入团入国民党源层残留补修 batch265",
        "",
        f"- 修复总数：{total}",
        "- 范围：下册源稿和全书正文汇总中的完整短语 `加人中国共产党`、`加人中国共产主义青年团`、`加人中国国民党`。",
        "- 原则：只替换完整组织加入短语；不处理普通 `加人`、`进人`、`编人`。当前正式读者对应短语已为 `加入`，本批主要追平源层。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for file in changes:
        lines.append(f"\n### {file['path']}")
        for item in file["changes"]:
            if item["count"]:
                evidence = "；".join(f"`{e}`" for e in item["evidence"][:8])
                if len(item["evidence"]) > 8:
                    evidence += f"；等 {len(item['evidence'])} 处页级 OCR 证据"
                lines.append(f"- `{item['old']}` -> `{item['new']}`；次数 {item['count']}；证据 {evidence}")
    lines.extend(["", "## 残留计数", ""])
    if residuals:
        for rel, hits in residuals.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批坏短语在目标源稿、全书汇总及当前全书/下册阅读稿中均为 0。")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(total)
    print(json.dumps(residuals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
