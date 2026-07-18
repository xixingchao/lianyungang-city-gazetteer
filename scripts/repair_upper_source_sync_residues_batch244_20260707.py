from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

TASKS = [
    {
        "path": Path("workbench/body_chapters/连云港市志_全书_正文汇总.md"),
        "replacements": [
            ("防汛防阜指挥部改称市防汛抗阜指挥部", "防汛防旱指挥部改称市防汛抗旱指挥部", "workbench/ocr/paddle_ocr/上/part03/page_0060.txt"),
            ("防汛防阜总队部改称防汛防阜指挥部", "防汛防旱总队部改称防汛防旱指挥部", "workbench/ocr/paddle_ocr/上/part03/page_0059.txt:27"),
            ("三县防汛防阜指挥部", "三县防汛防旱指挥部", "workbench/ocr/paddle_ocr/上/part03/page_0060.txt"),
            ("全市防汛防阜工作全面加强", "全市防汛防旱工作全面加强", "workbench/ocr/paddle_ocr/上/part03/page_0060.txt"),
            ("市防汛抗阜办公室", "市防汛抗旱办公室", "workbench/ocr/paddle_ocr/上/part03/page_0060.txt"),
            ("发现隐惠则限期修", "发现隐患则限期修", "workbench/ocr/paddle_ocr/上/part03/page_0060.txt"),
            ("市防汛抗阜指挥部", "市防汛抗旱指挥部", "workbench/ocr/paddle_ocr/上/part03/page_0060.txt"),
            ("确定：新述河安全行", "确定：新沭河安全行", "workbench/ocr/paddle_ocr/上/part03/page_0144.txt"),
            ("对新述河和石梁河", "对新沭河和石梁河", "workbench/ocr/paddle_ocr/上/part03/page_0144.txt"),
            ("塑苦化，生产进人稳产优质时期", "塑苫化，生产进入稳产优质时期", "workbench/ocr/paddle_ocr/上/part03/page_0144.txt:5"),
            ("准北盐业受到限产", "淮北盐业受到限产", "workbench/ocr/paddle_ocr/上/part03/page_0144.txt:5"),
            ("日本人侵准北盐区", "日本入侵淮北盐区", "workbench/ocr/paddle_ocr/上/part03/page_0154.txt:16"),
            ("输人日本国淮盐", "输入日本国淮盐", "workbench/ocr/paddle_ocr/上/part03/page_0154.txt:16"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/上/第十卷至第十六卷（part03）.md"),
        "replacements": [
            ("塑苦化，生产进入稳产优质时期", "塑苫化，生产进入稳产优质时期", "workbench/ocr/paddle_ocr/上/part03/page_0144.txt:5"),
            ("日本人侵淮北盐区", "日本入侵淮北盐区", "workbench/ocr/paddle_ocr/上/part03/page_0154.txt:16"),
        ],
    },
    {
        "path": Path("workbench/body_chapters/连云港市志_上册_正文汇总.md"),
        "replacements": [
            ("塑苦化，生产进入稳产优质时期", "塑苫化，生产进入稳产优质时期", "workbench/ocr/paddle_ocr/上/part03/page_0144.txt:5"),
            ("日本人侵淮北盐区", "日本入侵淮北盐区", "workbench/ocr/paddle_ocr/上/part03/page_0154.txt:16"),
        ],
    },
]


def main():
    changes = []
    for task in TASKS:
        path = ROOT / task["path"]
        text = path.read_text(encoding="utf-8")
        original = text
        hits = []
        for old, new, evidence in task["replacements"]:
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                hits.append({"old": old, "new": new, "count": count, "evidence": evidence})
        if text != original:
            path.write_text(text, encoding="utf-8", newline="")
        changes.append({"path": str(task["path"]), "changes": hits})

    total = sum(c["count"] for f in changes for c in f["changes"])
    report_md = ROOT / "output/reports/upper_source_sync_residues_batch244_20260707.md"
    report_json = ROOT / "output/reports/upper_source_sync_residues_batch244_20260707.json"
    lines = [
        "# 上册源稿全书汇总漏同步残留修复 batch244",
        "",
        f"- 修复总数：{total}",
        "- 范围：上册第十卷至第十六卷源稿、全书正文汇总。当前全书 HTML 对应段落已为正确文本。",
        "- 原则：仅补页级 PaddleOCR 明确支持的源稿/汇总漏同步残留，不改 OCR 原始层。",
        "",
        "## 替换明细",
    ]
    for file in changes:
        if not file["changes"]:
            continue
        lines.append(f"\n### {file['path']}")
        for item in file["changes"]:
            lines.append(f"- `{item['old']}` -> `{item['new']}`；次数 {item['count']}；证据 `{item['evidence']}`")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps({"total": total, "changes": changes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(total)
    for file in changes:
        if file["changes"]:
            print(file["path"])


if __name__ == "__main__":
    main()
