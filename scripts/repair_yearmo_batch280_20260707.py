from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]

REPLACEMENTS = [
    {"old": "1990年未，", "new": "1990年末，", "evidence": "年末时间点，后接机构、人数、持币量等状态统计。"},
    {"old": "1959年未，", "new": "1959年末，", "evidence": "人口统计时间点。"},
    {"old": "1975年未，", "new": "1975年末，", "evidence": "人口密度统计时间点。"},
    {"old": "1990年未外地", "new": "1990年末外地", "evidence": "表题时间点。"},
    {"old": "年未，市局", "new": "年末，市局", "evidence": "邮电设备开通后的年末状态。"},
    {"old": "年未实绩", "new": "年末实绩", "evidence": "人口自然增长率年末实绩。"},
    {"old": "1979年未定额资产", "new": "1979年末定额资产", "evidence": "资产占用统计时间点。"},
    {"old": "1985年未增长", "new": "1985年末增长", "evidence": "相对于 1985 年末的增长。"},
    {"old": "1990年未下辖", "new": "1990年末下辖", "evidence": "机构辖属统计时间点。"},
    {"old": "1990年未已与", "new": "1990年末已与", "evidence": "金融往来业务统计时间点。"},
    {"old": "1990年未，城乡", "new": "1990年末，城乡", "evidence": "居民持币量统计时间点。"},
    {"old": "到年未净投放", "new": "到年末净投放", "evidence": "现金投放统计时间点。"},
]

EXCLUDED_PARTS = ["/backup", "backup_", "/obsolete/", "/paddle_", "PaddleOCR", ".bak"]


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
        "batch": 280,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "Narrow 未/末 cleanup for explicit year-end contexts only.",
            "Phrases such as 年未有变化、年未变、多年未见、全年未发生、未列入 were intentionally left unchanged.",
            "No OCR merged files, backups, obsolete files, or historical packages were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/yearmo_batch280_20260707.md"
    js = ROOT / "output/reports/yearmo_batch280_20260707.json"
    lines = [
        "# 年末窄模式补修 batch280",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。",
        "- 原则：只处理明确为年末时间点的窄短语；保留 `年未有变化`、`年未变`、`多年未见`、`全年未发生`、`未列入` 等正确用法。",
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
        lines.append("- 本批窄模式在当前正式阅读 HTML 和正式正文源稿/汇总中均为 0。")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return md, total


def append_progress(report_md, total):
    progress = ROOT / "output/reports/progress/20260707_年末窄模式补修第二百八十批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 年末窄模式补修第二百八十批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文定点修复明确为年末时间点的 `年未` 残字窄模式，共 {total} 处；保留 `年未有变化`、`年未变`、`多年未见`、`全年未发生`、`未列入` 等正确用法。
- 报告：`output/reports/yearmo_batch280_20260707.md`；进度：`output/reports/progress/20260707_年末窄模式补修第二百八十批.md`。
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
