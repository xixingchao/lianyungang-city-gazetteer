from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "workbench/body_chapters/上/第一卷_自然环境.md",
    "workbench/body_chapters/上/第三卷_区县概况.md",
    "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
    "workbench/body_chapters/连云港市志_上册_正文汇总.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
    "output/final_reader/连云港市志_全书.html",
    "output/final_reader/连云港市志_下册.html",
]

REPLACEMENTS = [
    {
        "old": "县财政入1957年前主要是农业税",
        "new": "县财政收入1957年前主要是农业税",
        "evidence": "上下文同段多次出现财政收入；merged OCR 及当前正文均为漏字形态，属收入一词 OCR 漏字。",
    },
    {
        "old": "遇有重大大灾害性天气",
        "new": "遇有重大灾害性天气",
        "evidence": "气象业务固定搭配；merged OCR 及当前正文均为重复字形态。",
    },
    {
        "old": "另一一栏为",
        "new": "另一栏为",
        "evidence": "同句为离婚申请书栏目说明，重复“一”为 OCR 重字。",
    },
]

BAD_PATTERNS = [item["old"] for item in REPLACEMENTS]


def replace_all():
    changes = []
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            changes.append({
                "path": rel,
                "old": item["old"],
                "new": item["new"],
                "count": count,
                "evidence": item["evidence"],
            })
        if text != original:
            path.write_text(text, encoding="utf-8", newline="")
    return changes


def residuals():
    found = {}
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = {bad: text.count(bad) for bad in BAD_PATTERNS if text.count(bad)}
        if hits:
            found[rel] = hits
    return found


def write_report(changes, left):
    total = sum(row["count"] for row in changes)
    report = {
        "batch": 274,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "changes": changes,
        "residuals": left,
        "principle": "Only high-confidence context/OCR typo repairs; no broad replacements; no image display.",
    }
    md = ROOT / "output/reports/reader_source_context_typos_batch274_20260707.md"
    js = ROOT / "output/reports/reader_source_context_typos_batch274_20260707.json"
    lines = [
        "# 上下册正文高置信上下文错字补修 batch274",
        "",
        f"- 生成时间：{report['time']}",
        f"- 修复总数：{total}",
        "- 范围：上册第一卷/第三卷源稿、下册民政源稿、上册/全书正文汇总及当前全书/下册 HTML。",
        "- 原则：只修上下文闭合的漏字、重字、重复字；不处理可通旧用法或缺少证据的疑似项。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for row in changes:
        if row["count"]:
            lines.append(f"- `{row['path']}`：`{row['old']}` -> `{row['new']}`；次数 {row['count']}；依据：{row['evidence']}")
    lines.extend(["", "## 残留计数", ""])
    if left:
        for rel, hits in left.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批坏短语在目标文件中均为 0。")
    lines.extend([
        "",
        "## 暂不处理",
        "",
        "- `图象` 属于可通旧用法，本批不改。",
        "- `社会文教科费` 可能为原书财政科目表述，本批不凭现代用词改写。",
        "- `即有记载` 未取得强证据，本批不改为 `即使有记载`。",
    ])
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md, js, total


def append_progress(report_md):
    progress = ROOT / "output/reports/progress/20260707_上下册正文高置信上下文错字补修第二百七十四批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")

    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 上下册正文高置信上下文错字补修第二百七十四批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        old = old.rstrip() + "\n\n" + marker + "\n\n"
        old += "- 依据当前主交付可读性风险报告、合并 PaddleOCR 与正文上下文，定点修复 3 组高置信漏字/重字：`县财政入1957年前 -> 县财政收入1957年前`、`重大大灾害性天气 -> 重大灾害性天气`、`另一一栏 -> 另一栏`。\n"
        old += "- 同步范围：上册第一卷/第三卷源稿、下册民政源稿、上册/全书正文汇总及当前全书/下册 HTML；不处理 `图象`、`社会文教科费`、`即有记载` 等证据不足或可通旧用法。\n"
        old += "- 报告：`output/reports/reader_source_context_typos_batch274_20260707.md`；进度：`output/reports/progress/20260707_上下册正文高置信上下文错字补修第二百七十四批.md`；未打开、展示或嵌入图片。\n"
        memory.write_text(old + "\n", encoding="utf-8")


def main():
    changes = replace_all()
    left = residuals()
    md, js, total = write_report(changes, left)
    append_progress(md)
    print(f"total={total}")
    print(f"residuals={json.dumps(left, ensure_ascii=False)}")
    print(f"report={md}")


if __name__ == "__main__":
    main()
