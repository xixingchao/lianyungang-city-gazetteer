from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md",
    "workbench/body_chapters/第三十卷至第四十二卷（中part02）.md",
    "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
    "workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md",
    "workbench/body_chapters/连云港市志_全书_正文汇总.md",
]

REPLACEMENTS = [
    {"old": "投人", "new": "投入", "evidence": "上下文为投入使用、投入生产、投入市场、资金投入、干部投入等。"},
    {"old": "划人", "new": "划入", "evidence": "上下文为划入预算、划入金库、划入区县或规划入社等。"},
    {"old": "转人", "new": "转入", "evidence": "上下文为转入河道、地下、生产、学校/院系、账户或学习阶段等。"},
]


def apply_changes():
    changes = []
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            changes.append({"path": rel, "missing": True, "items": []})
            continue
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
        changes.append({"path": rel, "missing": False, "items": items})
    return changes


def residuals():
    found = {}
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = {item["old"]: text.count(item["old"]) for item in REPLACEMENTS if text.count(item["old"])}
        if hits:
            found[rel] = hits
    return found


def final_reader_counts():
    counts = {}
    for path in sorted((ROOT / "output/final_reader").glob("*.html")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        counts[str(path.relative_to(ROOT)).replace("\\", "/")] = {
            item["old"]: text.count(item["old"]) for item in REPLACEMENTS
        }
    return counts


def write_report(changes, left, reader_counts):
    total = sum(item["count"] for row in changes for item in row["items"])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = {
        "batch": 278,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "final_reader_counts": reader_counts,
        "notes": [
            "Source-layer 入/人 residual cleanup only; current final-reader HTML had no target hits.",
            "No OCR merged files, backups, obsolete files, or historical packages were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/source_ruzican_batch278_20260707.md"
    js = ROOT / "output/reports/source_ruzican_batch278_20260707.json"
    lines = [
        "# 源层入字残留补修 batch278",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：中册两个分段源稿、下册两个分段源稿、全书正文汇总。当前正式 HTML 中本批目标残字已为 0，本批用于源层防回流。",
        "- 原则：只处理完整残字短语 `投人 -> 投入`、`划人 -> 划入`、`转人 -> 转入`；不做 `人/入` 泛替换。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for row in changes:
        if row.get("missing"):
            lines.append(f"- `{row['path']}`：文件不存在，跳过。")
            continue
        for item in row["items"]:
            if item["count"]:
                lines.append(f"- `{row['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    lines.extend(["", "## 正式 HTML 残留", ""])
    for rel, hits in reader_counts.items():
        lines.append(f"- `{rel}`：{hits}")
    lines.extend(["", "## 目标源层残留", ""])
    if left:
        for rel, hits in left.items():
            lines.append(f"- `{rel}`：{hits}")
    else:
        lines.append("- 本批目标源稿/汇总中残留为 0。")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md, total


def append_progress(report_md):
    progress = ROOT / "output/reports/progress/20260707_源层入字残留补修第二百七十八批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 源层入字残留补修第二百七十八批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文定点修复源层入/人残字：`投人 -> 投入`、`划人 -> 划入`、`转人 -> 转入`，覆盖中册两个分段源稿、下册两个分段源稿、全书正文汇总，共 291 处；当前正式 HTML 本批目标残字已为 0，本批主要防止源层回流。
- 报告：`output/reports/source_ruzican_batch278_20260707.md`；进度：`output/reports/progress/20260707_源层入字残留补修第二百七十八批.md`。
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
