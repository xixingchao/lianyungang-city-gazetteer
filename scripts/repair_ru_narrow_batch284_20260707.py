from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
ALL_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]
SOURCE_ROOT = ROOT / "workbench/body_chapters"

ALL_REPLACEMENTS = [
    {"old": "招人人会", "new": "招人入会", "evidence": "民俗摇彩签语境，招人加入会买彩签。"},
]

SOURCE_REPLACEMENTS = [
    {"old": "人市境", "new": "入市境", "evidence": "河流、病虫害、宗教人口或日军进入市境语境。"},
    {"old": "进人市场", "new": "进入市场", "evidence": "产品或农民进入市场交易语境。"},
    {"old": "进\n人市场", "new": "进\n入市场", "evidence": "跨行断开的进入市场交易语境。"},
    {"old": "进人市区", "new": "进入市区", "evidence": "外地施工队伍、车辆等进入市区语境。"},
    {"old": "迁人市", "new": "迁入市", "evidence": "车间迁入市工艺美术公司、户口迁入市区语境。"},
    {"old": "并人市", "new": "并入市", "evidence": "机构、工厂并入市属部门或单位语境。"},
    {"old": "人市县财政金库", "new": "入市县财政金库", "evidence": "财政金库入库语境。"},
    {"old": "交人市县国库", "new": "交入市县国库", "evidence": "排污费交入市县国库语境。"},
    {"old": "人社农户", "new": "入社农户", "evidence": "农业合作社、供销社入社农户统计语境。"},
    {"old": "人社50户", "new": "入社50户", "evidence": "渔业生产合作社入社户数语境。"},
]

EXCLUDED_PARTS = ["/backup", "backup_", "/obsolete/", "/paddle_", "PaddleOCR", ".bak"]


def iter_targets(roots):
    seen = set()
    for base in roots:
        for path in sorted(base.rglob("*")):
            if path.suffix.lower() not in {".html", ".md"}:
                continue
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            if any(part in rel for part in EXCLUDED_PARTS) or rel in seen:
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
        "batch": 284,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "Narrow 入/人 cleanup for current reader and source-layer prevention.",
            "招人人会 was fixed in current final-reader HTML and formal sources; other patterns are source-layer only.",
            "Normal phrases such as 5人市调整机构、工人社会、个人户 were intentionally not changed.",
            "No OCR merged files, backups, obsolete files, or historical packages were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/ru_narrow_batch284_20260707.md"
    js = ROOT / "output/reports/ru_narrow_batch284_20260707.json"
    lines = [
        "# 入字窄模式补修 batch284",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总；除 `招人人会` 外，其余为源层防回流。",
        "- 原则：只处理上下文明确的入市境、进入市场、并入市、入社等窄短语；保留正常词。",
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
    progress = ROOT / "output/reports/progress/20260707_入字窄模式补修第二百八十四批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 入字窄模式补修第二百八十四批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文定点修复 `招人人会 -> 招人入会`，并在源层防回流修复入市境、进入市场、进入市区、迁入市、并入市、入市县财政金库、交入市县国库、入社农户、入社50户等窄模式，共 {total} 处。
- 报告：`output/reports/ru_narrow_batch284_20260707.md`；进度：`output/reports/progress/20260707_入字窄模式补修第二百八十四批.md`。
- 正常词如 `5人市调整机构`、`工人社会`、`个人户` 未处理；未处理 OCR merged、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
