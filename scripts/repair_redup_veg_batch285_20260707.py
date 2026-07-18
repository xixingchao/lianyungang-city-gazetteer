from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]

REPLACEMENTS = [
    {"old": "统一一", "new": "统一", "evidence": "统一安排、统一管理、统一分配、统一计划等固定搭配中多出一字。"},
    {"old": "一一定", "new": "一定", "evidence": "一定条件、一定生产规模、一定作用等固定搭配中多出一字。"},
    {"old": "摸模清", "new": "摸清", "evidence": "户口整顿中摸清暂住人口语境。"},
    {"old": "白莱", "new": "白菜", "evidence": "大白菜、白菜高产栽培和大白菜萝卜采购语境。"},
    {"old": "红萝下139", "new": "红萝卜139", "evidence": "蔬菜收购量中红萝卜、雪里蕻等菜名并列。"},
    {"old": "雪里6万", "new": "雪里蕻6万", "evidence": "蔬菜收购量中雪里蕻菜名。"},
]

EXCLUDED_PARTS = ["/backup", "backup_", "/obsolete/", "/paddle_", "PaddleOCR", ".bak"]


def iter_targets():
    seen = set()
    for base in TARGET_ROOTS:
        for path in sorted(base.rglob("*")):
            if path.suffix.lower() not in {".html", ".md"}:
                continue
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            if any(part in rel for part in EXCLUDED_PARTS) or rel in seen:
                continue
            seen.add(rel)
            yield rel, path


def apply_changes():
    changes = []
    for rel, path in iter_targets():
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
    for rel, path in iter_targets():
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = {item["old"]: text.count(item["old"]) for item in REPLACEMENTS if text.count(item["old"])}
        if hits:
            found[rel] = hits
    return found


def write_report(changes, left):
    total = sum(item["count"] for row in changes for item in row["items"])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = {
        "batch": 285,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "High-confidence repeated-character and vegetable-name typo cleanup.",
            "代于 and 了若指掌 were intentionally left unchanged because context is not high-confidence typo evidence.",
            "No OCR merged files, backups, obsolete files, or historical packages were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/redup_veg_batch285_20260707.md"
    js = ROOT / "output/reports/redup_veg_batch285_20260707.json"
    lines = [
        "# 重字与菜名残字补修 batch285",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。",
        "- 原则：只处理上下文明确的多字重复和菜名残字；保留证据不足的 `代于`、`了若指掌`。",
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
        lines.append("- 本批目标短语在当前检查范围中均为 0。")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md, total


def append_progress(report_md, total):
    progress = ROOT / "output/reports/progress/20260707_重字与菜名残字补修第二百八十五批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 重字与菜名残字补修第二百八十五批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文定点修复多字重复和菜名残字：`统一一 -> 统一`、`一一定 -> 一定`、`摸模清 -> 摸清`、`白莱 -> 白菜`、`红萝下139 -> 红萝卜139`、`雪里6万 -> 雪里蕻6万`，共 {total} 处。
- 报告：`output/reports/redup_veg_batch285_20260707.md`；进度：`output/reports/progress/20260707_重字与菜名残字补修第二百八十五批.md`。
- `代于`、`了若指掌` 等证据不足项未处理；未处理 OCR merged、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
