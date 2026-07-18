from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md",
]
REPLACEMENTS = [
    {"old": "准海剧团", "new": "淮海剧团", "evidence": "淮海戏、淮海剧团段落中准/淮形近误识。"},
]


def apply_changes():
    changes = []
    for path in TARGETS:
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
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
    for path in TARGETS:
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = {item["old"]: text.count(item["old"]) for item in REPLACEMENTS if text.count(item["old"])}
        if hits:
            found[rel] = hits
    return found


def write_report(changes, left):
    total = sum(item["count"] for row in changes for item in row["items"])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = ROOT / "output/reports/huaihai_troupe_batch290_20260707.md"
    js = ROOT / "output/reports/huaihai_troupe_batch290_20260707.json"
    report = {"batch": 290, "time": now, "total": total, "changes": changes, "residuals": left, "notes": ["Narrow source-layer correction for 淮海剧团.", "No image display was used."]}
    lines = [
        "# 淮海剧团源层残字补修 batch290",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：下册文化源稿。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for row in changes:
        for item in row["items"]:
            if item["count"]:
                lines.append(f"- `{row['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    lines.extend(["", "## 残留计数", ""])
    lines.append("- 本批目标短语在当前检查范围中均为 0。" if not left else json.dumps(left, ensure_ascii=False))
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md, total


def append_progress(report_md, total):
    progress = ROOT / "output/reports/progress/20260707_淮海剧团源层残字补修第二百九十批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 淮海剧团源层残字补修第二百九十批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据下册文化源稿淮海戏/淮海剧团上下文，定点修复 `准海剧团 -> 淮海剧团` 源层漏项，共 {total} 处。
- 报告：`output/reports/huaihai_troupe_batch290_20260707.md`；进度：`output/reports/progress/20260707_淮海剧团源层残字补修第二百九十批.md`。
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
