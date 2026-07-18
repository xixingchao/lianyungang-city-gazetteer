from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

TARGET_ROOTS = [
    ROOT / "output/final_reader",
    ROOT / "workbench/body_chapters",
]

REPLACEMENTS = [
    {"old": "人库", "new": "入库", "evidence": "上下文为粮食、税款、产品、库区或仓储入库。"},
    {"old": "人境", "new": "入境", "evidence": "上下文为进入境内、入境船舶、检疫查验或传入境内。"},
    {"old": "人院", "new": "入院", "evidence": "上下文为医院入院规则、敬老院入院人数或病人入院。"},
    {"old": "人伍", "new": "入伍", "evidence": "上下文为兵役、志愿兵、义务兵和应征青年入伍。"},
    {"old": "人狱", "new": "入狱", "evidence": "上下文为被捕入狱、逮捕入狱。"},
    {"old": "人帐", "new": "入帐", "evidence": "上下文为房屋估价入帐。"},
]

EXCLUDED_PARTS = [
    "/backup",
    "backup_",
    "/obsolete/",
    "/paddle_",
    "PaddleOCR",
    ".bak",
]


def iter_targets():
    seen = set()
    for base in TARGET_ROOTS:
        for path in sorted(base.rglob("*")):
            if path.suffix.lower() not in {".html", ".md"}:
                continue
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            if any(part in rel for part in EXCLUDED_PARTS):
                continue
            if rel in seen:
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
        "batch": 279,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "High-confidence 入/人 residual cleanup in current final-reader HTML and formal body sources.",
            "No OCR merged files, backups, obsolete files, or historical packages were changed.",
            "Ambiguous terms such as 人选、人市、人会、年未 were intentionally not changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/ruzi_high_conf_batch279_20260707.md"
    js = ROOT / "output/reports/ruzi_high_conf_batch279_20260707.json"
    lines = [
        "# 高置信入字残留补修 batch279",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。",
        "- 原则：只处理上下文稳定的完整残字短语；不处理 `人选`、`人市`、`人会`、`年未` 等混合候选。",
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
        lines.append("- 本批目标短语在当前正式阅读 HTML 和正式正文源稿/汇总中均为 0。")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md, total


def append_progress(report_md):
    progress = ROOT / "output/reports/progress/20260707_高置信入字残留补修第二百七十九批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 高置信入字残留补修第二百七十九批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文定点修复当前正式阅读 HTML 与正式正文源稿/汇总中的高置信入/人残字：`人库 -> 入库`、`人境 -> 入境`、`人院 -> 入院`、`人伍 -> 入伍`、`人狱 -> 入狱`、`人帐 -> 入帐`，共 {sum(item['count'] for row in json.loads((ROOT / 'output/reports/ruzi_high_conf_batch279_20260707.json').read_text(encoding='utf-8'))['changes'] for item in row['items']) if (ROOT / 'output/reports/ruzi_high_conf_batch279_20260707.json').exists() else '若干'} 处。
- 报告：`output/reports/ruzi_high_conf_batch279_20260707.md`；进度：`output/reports/progress/20260707_高置信入字残留补修第二百七十九批.md`。
- `人选`、`人市`、`人会`、`年未` 等混合候选未批量处理；未处理 OCR merged、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
        memory.write_text(old.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")


def main():
    changes = apply_changes()
    left = residuals()
    md, total = write_report(changes, left)
    append_progress(md)
    print(f"total={total}")
    print(f"residuals={json.dumps(left, ensure_ascii=False)}")
    print(f"report={md}")


if __name__ == "__main__":
    main()
