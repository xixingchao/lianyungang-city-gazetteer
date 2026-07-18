from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "workbench/body_chapters/上/总述与大事记.md",
    "workbench/body_chapters/连云港市志_上册_正文汇总.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
]

OLD = "收人"
NEW = "收入"


def apply_changes():
    changes = []
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            changes.append({"path": rel, "count": 0, "missing": True})
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        count = text.count(OLD)
        if count:
            path.write_text(text.replace(OLD, NEW), encoding="utf-8", newline="")
        changes.append({"path": rel, "count": count, "missing": False})
    return changes


def residuals():
    found = {}
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        count = path.read_text(encoding="utf-8", errors="ignore").count(OLD)
        if count:
            found[rel] = count
    return found


def final_reader_counts():
    counts = {}
    folder = ROOT / "output/final_reader"
    for path in sorted(folder.glob("*.html")):
        if path.is_file():
            counts[str(path.relative_to(ROOT)).replace("\\", "/")] = path.read_text(
                encoding="utf-8", errors="ignore"
            ).count(OLD)
    return counts


def write_report(changes, left, reader_counts):
    total = sum(row["count"] for row in changes)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = {
        "batch": 277,
        "time": now,
        "old": OLD,
        "new": NEW,
        "total": total,
        "changes": changes,
        "residuals": left,
        "final_reader_counts": reader_counts,
        "notes": [
            "Source-layer income-word residual cleanup; current final-reader HTML was already clean.",
            "No OCR merged files, backups, obsolete files, or historical packages were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/source_shouru_batch277_20260707.md"
    js = ROOT / "output/reports/source_shouru_batch277_20260707.json"
    lines = [
        "# 源层收入残字补修 batch277",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：上册大事记源稿、上册正文汇总、全书正文汇总。当前正式 HTML 中本批残字已为 0，本批用于源层防回流。",
        "- 原则：只处理完整残字 `收人 -> 收入`；不做 `人/入` 泛替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for row in changes:
        if row.get("missing"):
            lines.append(f"- `{row['path']}`：文件不存在，跳过。")
        elif row["count"]:
            lines.append(f"- `{row['path']}`：`{OLD}` -> `{NEW}`；次数 {row['count']}。")
    lines.extend(["", "## 正式 HTML 残留", ""])
    for rel, count in reader_counts.items():
        lines.append(f"- `{rel}`：`{OLD}` {count} 处")
    lines.extend(["", "## 目标源层残留", ""])
    if left:
        for rel, count in left.items():
            lines.append(f"- `{rel}`：`{OLD}` {count} 处")
    else:
        lines.append("- 本批目标源稿/汇总中残留为 0。")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md, total


def append_progress(report_md):
    progress = ROOT / "output/reports/progress/20260707_源层收入残字补修第二百七十七批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 源层收入残字补修第二百七十七批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文定点修复源层收入词残字：`收人 -> 收入`，覆盖上册大事记源稿、上册正文汇总、全书正文汇总，共 454 处；当前正式 HTML 本批残字已为 0，本批主要防止源层回流。
- 报告：`output/reports/source_shouru_batch277_20260707.md`；进度：`output/reports/progress/20260707_源层收入残字补修第二百七十七批.md`。
- 未处理 OCR merged、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
        memory.write_text(old.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")


def main():
    changes = apply_changes()
    left = residuals()
    reader_counts = final_reader_counts()
    md, total = write_report(changes, left, reader_counts)
    append_progress(md)
    print(f"total={total}")
    print(f"residuals={json.dumps(left, ensure_ascii=False)}")
    print(f"final_reader_counts={json.dumps(reader_counts, ensure_ascii=False)}")
    print(f"report={md}")


if __name__ == "__main__":
    main()
