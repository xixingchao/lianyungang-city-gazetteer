from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]

REPLACEMENTS = [
    {"old": "卖婚人员", "new": "卖淫人员", "evidence": "查禁卖淫嫖娼段落中查获人员语境。"},
    {"old": "客留、胁迫卖淫娟旅店", "new": "客留、胁迫卖淫嫖娼旅店", "evidence": "旅店容留、胁迫卖淫嫖娼语境；仅修嫖娼残字。"},
    {"old": "客留、胁迫卖淫嫖娼旅店", "new": "容留、胁迫卖淫嫖娼旅店", "evidence": "治安司法取缔容留、胁迫卖淫嫖娼旅店固定表述。"},
    {"old": "流 传传播到市内", "new": "流 传到市内", "evidence": "水怪谣言流传到市内，传播二字重复。"},
    {"old": "流传传播到市内", "new": "流传到市内", "evidence": "水怪谣言流传到市内，传播二字重复。"},
    {"old": "准阴", "new": "淮阴", "evidence": "淮阴地区、淮阴航运局、淮阴方向、淮阴电网等地名/机构语境。"},
]

EXCLUDED_PARTS = ["/backup", "backup_", "/obsolete/", "/package/", "/paddle_", "PaddleOCR", ".bak"]


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
        "batch": 291,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "High-confidence justice-section typo cleanup and source-layer 淮阴 place-name cleanup.",
            "1990年14月 was intentionally left unchanged pending source-page review.",
            "No OCR merged files, backups, obsolete files, package files, or historical outputs were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/high_conf_terms_batch291_20260707.md"
    js = ROOT / "output/reports/high_conf_terms_batch291_20260707.json"
    lines = [
        "# 高置信正文残字补修 batch291",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。",
        "- 原则：处理治安司法段落固定语境残字，以及源层 `准阴 -> 淮阴` 地名/机构防回流。",
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
    progress = ROOT / "output/reports/progress/20260707_高置信正文残字补修第二百九十一批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 高置信正文残字补修第二百九十一批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文定点修复当前正式阅读 HTML 与正式正文源稿/汇总中的高置信残字：治安司法段落 `卖婚人员 -> 卖淫人员`、`客留/卖淫娟 -> 容留/卖淫嫖娼`、`流传传播到市内 -> 流传到市内`，并在源层防回流修复地名/机构 `准阴 -> 淮阴`，共 {total} 处。
- 报告：`output/reports/high_conf_terms_batch291_20260707.md`；进度：`output/reports/progress/20260707_高置信正文残字补修第二百九十一批.md`。
- `1990年14月` 日期疑点未回源前不处理；未处理 OCR merged、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
