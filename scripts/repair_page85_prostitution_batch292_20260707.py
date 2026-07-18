from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]
SOURCE_EVIDENCE = [
    "workbench/ocr/paddle_ocr/下/part01/page_0085.txt",
    "workbench/ocr/raw/下/part01/page_0085.txt",
]

REPLACEMENTS = [
    {"old": "1990年14月", "new": "1990年1~4月", "evidence": "Paddle 页级 OCR page_0085 明确为 1990年1~4月。"},
    {"old": "卖</p><p>婚人员", "new": "卖</p><p>淫嫖娼人员", "evidence": "Paddle 页级 OCR page_0085 为 查获24名卖淫嫖娼人员。"},
    {"old": "卖\n婚人员", "new": "卖\n淫嫖娼人员", "evidence": "Paddle 页级 OCR page_0085 为 查获24名卖淫嫖娼人员。"},
    {"old": "卖 婚人员", "new": "卖淫嫖娼人员", "evidence": "Paddle 页级 OCR page_0085 为 查获24名卖淫嫖娼人员。"},
    {"old": "卖婚人员", "new": "卖淫嫖娼人员", "evidence": "Paddle 页级 OCR page_0085 为 查获24名卖淫嫖娼人员。"},
    {"old": "流 传传播到市内", "new": "流 传到市内", "evidence": "上下文为水怪谣言流传到市内；传播二字重复。"},
    {"old": "流传传播到市内", "new": "流传到市内", "evidence": "上下文为水怪谣言流传到市内；传播二字重复。"},
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
        "batch": 292,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "source_evidence": SOURCE_EVIDENCE,
        "notes": [
            "Page-backed cleanup for 下册 page_0085 查禁卖淫嫖娼段落.",
            "Raw OCR still has 1990年14月, but Paddle page OCR resolves it as 1990年1~4月.",
            "No OCR source files, backups, obsolete files, package files, or historical outputs were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/page85_prostitution_batch292_20260707.md"
    js = ROOT / "output/reports/page85_prostitution_batch292_20260707.json"
    lines = [
        "# 下册第85页查禁卖淫嫖娼段落回源补修 batch292",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。",
        "- 页级证据：`workbench/ocr/paddle_ocr/下/part01/page_0085.txt`；对照：`workbench/ocr/raw/下/part01/page_0085.txt`。",
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
    progress = ROOT / "output/reports/progress/20260707_下册第85页查禁卖淫嫖娼段落回源补修第二百九十二批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 下册第85页查禁卖淫嫖娼段落回源补修第二百九十二批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据页级 OCR `workbench/ocr/paddle_ocr/下/part01/page_0085.txt`，对照 raw OCR `workbench/ocr/raw/下/part01/page_0085.txt`，补修下册第85页查禁卖淫嫖娼段落：`1990年14月 -> 1990年1~4月`，跨段落 `卖/婚人员 -> 卖淫嫖娼人员`，以及 `流传传播到市内 -> 流传到市内`，共 {total} 处。
- 报告：`output/reports/page85_prostitution_batch292_20260707.md`；进度：`output/reports/progress/20260707_下册第85页查禁卖淫嫖娼段落回源补修第二百九十二批.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
