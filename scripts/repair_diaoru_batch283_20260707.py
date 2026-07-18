from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]

REPLACEMENTS = [
    {"old": "从上海调人", "new": "从上海调入", "evidence": "从外地调入钢材。"},
    {"old": "调人生铁", "new": "调入生铁", "evidence": "从东北钢铁公司调入生铁。"},
    {"old": "调人镀锌", "new": "调入镀锌", "evidence": "从徐州五金公司调入镀锌铁皮。"},
    {"old": "调人外地菜", "new": "调入外地菜", "evidence": "蔬菜调入外地菜统计语境。"},
    {"old": "调人外地386.5万公斤", "new": "调入外地386.5万公斤", "evidence": "蔬菜统购包销中外地菜调入量。"},
    {"old": "赣榆调人", "new": "赣榆调入", "evidence": "粮食合理流向中地瓜干由东海、赣榆调入。"},
    {"old": "四川\n调人", "new": "四川\n调入", "evidence": "粮食合理流向中稻谷由四川调入。"},
    {"old": "四川</p><p>调人", "new": "四川</p><p>调入", "evidence": "正式 HTML 跨段同一句，稻谷由四川调入。"},
    {"old": "<p>调人</p>", "new": "<p>调入</p>", "evidence": "粮食调入、调出统计表表头。"},
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
        "batch": 283,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "Narrow 调人->调入 cleanup for explicit material/food transfer contexts and table headers only.",
            "治调人员、抽调人员、催调人员 and other valid 调人 substrings were intentionally left unchanged.",
            "No OCR merged files, backups, obsolete files, or historical packages were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/diaoru_batch283_20260707.md"
    js = ROOT / "output/reports/diaoru_batch283_20260707.json"
    lines = [
        "# 调入窄模式补修 batch283",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。",
        "- 原则：只处理明确为物资、蔬菜、粮食调入和表头 `调入` 的窄短语；保留 `治调人员`、`抽调人员`、`催调人员` 等正常词。",
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
    progress = ROOT / "output/reports/progress/20260707_调入窄模式补修第二百八十三批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 调入窄模式补修第二百八十三批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文定点修复物资、蔬菜、粮食调入语境和粮食调入/调出统计表表头中的 `调人 -> 调入` 窄模式，共 {total} 处。
- 报告：`output/reports/diaoru_batch283_20260707.md`；进度：`output/reports/progress/20260707_调入窄模式补修第二百八十三批.md`。
- `治调人员`、`抽调人员`、`催调人员` 等正常词未批量处理；未处理 OCR merged、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
