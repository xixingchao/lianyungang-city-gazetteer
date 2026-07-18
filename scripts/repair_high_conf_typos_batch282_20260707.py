from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

ALL_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]
SOURCE_ROOT = ROOT / "workbench/body_chapters"

ALL_REPLACEMENTS = [
    {"old": "以工代于", "new": "以工代干", "evidence": "干部录用语境，固定说法为以工代干。"},
    {"old": "精简穴员", "new": "精简人员", "evidence": "机构编制整顿语境，正式 HTML 全书处已呈现为精简人员。"},
    {"old": "疮疾", "new": "疟疾", "evidence": "寄生虫病防治、疟疾联防、疟疾防治研究等上下文。"},
    {"old": "症疾", "new": "疟疾", "evidence": "寄生虫病防治、传染病监测、五省联防和科研项目均为疟疾语境。"},
]

SOURCE_REPLACEMENTS = [
    {"old": "列人", "new": "列入", "evidence": "源稿中均为列入计划、序列、范围、名录、课表等语境；正式 HTML 已无目标残留。"},
    {"old": "纳人", "new": "纳入", "evidence": "源稿中均为纳入计划、预算、管理、范围、体系等语境；正式 HTML 已无目标残留。"},
]

EXCLUDED_PARTS = ["/backup", "backup_", "/obsolete/", "/paddle_", "PaddleOCR", ".bak"]


def is_allowed(rel: str) -> bool:
    return not any(part in rel for part in EXCLUDED_PARTS)


def iter_targets(roots):
    seen = set()
    for base in roots:
        for path in sorted(base.rglob("*")):
            if path.suffix.lower() not in {".html", ".md"}:
                continue
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            if not is_allowed(rel) or rel in seen:
                continue
            seen.add(rel)
            yield rel, path


def apply_group(roots, replacements):
    changes = []
    for rel, path in iter_targets(roots):
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        items = []
        for item in replacements:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        if text != original:
            path.write_text(text, encoding="utf-8", newline="")
            changes.append({"path": rel, "items": items})
    return changes


def apply_changes():
    changes = []
    changes.extend(apply_group(ALL_ROOTS, ALL_REPLACEMENTS))
    changes.extend(apply_group([SOURCE_ROOT], SOURCE_REPLACEMENTS))
    return changes


def residuals():
    found = {}
    for rel, path in iter_targets(ALL_ROOTS):
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = {item["old"]: text.count(item["old"]) for item in ALL_REPLACEMENTS if text.count(item["old"])}
        if hits:
            found[rel] = hits
    for rel, path in iter_targets([SOURCE_ROOT]):
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = {item["old"]: text.count(item["old"]) for item in SOURCE_REPLACEMENTS if text.count(item["old"])}
        if hits:
            found.setdefault(rel, {}).update(hits)
    return found


def write_report(changes, left):
    total = sum(item["count"] for row in changes for item in row["items"])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = {
        "batch": 282,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "High-confidence typo cleanup in current final-reader HTML and formal body sources.",
            "列人/纳人 were source-layer only because current final-reader HTML had no such target residuals.",
            "Ambiguous terms such as 加人、进人、调人、编人、人选、人市 were intentionally not bulk-changed.",
            "No OCR merged files, backups, obsolete files, or historical packages were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/high_conf_typos_batch282_20260707.md"
    js = ROOT / "output/reports/high_conf_typos_batch282_20260707.json"
    lines = [
        "# 高置信正文残字补修 batch282",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总；其中 `列人/纳人` 只修源层防回流。",
        "- 原则：只处理上下文明确的完整短语；不批量处理 `加人`、`进人`、`调人`、`编人`、`人选`、`人市` 等混合候选。",
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
    progress = ROOT / "output/reports/progress/20260707_高置信正文残字补修第二百八十二批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 高置信正文残字补修第二百八十二批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文定点修复当前正式阅读 HTML 与正式正文源稿/汇总中的高置信残字：`以工代于 -> 以工代干`、`精简穴员 -> 精简人员`、`疮疾/症疾 -> 疟疾`；并在源层防回流修复 `列人 -> 列入`、`纳人 -> 纳入`，共 {total} 处。
- 报告：`output/reports/high_conf_typos_batch282_20260707.md`；进度：`output/reports/progress/20260707_高置信正文残字补修第二百八十二批.md`。
- `加人`、`进人`、`调人`、`编人`、`人选`、`人市` 等混合候选未批量处理；未处理 OCR merged、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
