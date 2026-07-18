from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "output/final_reader/连云港市志_下册.html",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
]

REPLACEMENTS = [
    {"old": "个体行医管理</p><p>第节</p>", "new": "第一节个体行医管理</p>", "evidence": "分册 HTML 与全书 HTML、分段源稿结构对齐。"},
    {"old": "第四章 个体行医管理 第节", "new": "第四章 个体行医管理 第一节", "evidence": "全书正文汇总中医政药政第四章开篇节标题。"},
]


def apply_changes():
    changes = []
    for rel in TARGETS:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        if text != original:
            path.write_text(text, encoding="utf-8", newline="")
        changes.append({"path": rel, "items": items})
    return changes


def residuals():
    found = {}
    for rel in TARGETS:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = {item["old"]: text.count(item["old"]) for item in REPLACEMENTS if text.count(item["old"])}
        if hits:
            found[rel] = hits
    return found


def write_report(changes, left):
    total = sum(item["count"] for row in changes for item in row["items"])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = {
        "batch": 287,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "Follow-up structural heading sync for 个体行医管理.",
            "No OCR merged files, backups, obsolete files, or historical packages were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/structural_heading_followup_batch287_20260707.md"
    js = ROOT / "output/reports/structural_heading_followup_batch287_20260707.json"
    lines = [
        "# 结构性标题残字补修 follow-up batch287",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：下册正式 HTML、全书正文汇总。",
        "- 原则：与全书 HTML 和分段源稿中的 `第一节个体行医管理` 结构对齐。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for row in changes:
        for item in row["items"]:
            if item["count"]:
                lines.append(f"- `{row['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    lines.extend(["", "## 残留计数", ""])
    if left:
        for rel, hits in left.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批目标短语残留为 0。")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md, total


def append_progress(report_md, total):
    progress = ROOT / "output/reports/progress/20260707_结构性标题残字补修第二百八十七批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 结构性标题残字补修第二百八十七批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 复查 batch286 后，同步下册正式 HTML 与全书正文汇总中的 `个体行医管理` 开篇节标题为 `第一节个体行医管理`，共 {total} 处。
- 报告：`output/reports/structural_heading_followup_batch287_20260707.md`；进度：`output/reports/progress/20260707_结构性标题残字补修第二百八十七批.md`。
- 未处理 OCR merged、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
        memory.write_text(old.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")


def main():
    changes = apply_changes()
    left = residuals()
    md, total = write_report(changes, left)
    append_progress(md, total)
    print(f"total={total}")
    print(f"residuals={json.dumps(left, ensure_ascii=False)}")
    print(f"report={md}")


if __name__ == "__main__":
    main()
