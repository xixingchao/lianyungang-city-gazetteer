from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]

REPLACEMENTS = [
    {"old": "置信访", "new": "信访", "evidence": "第十一章信访标题前孤立残字，正式结构应为信访。"},
    {"old": "第节爱国卫生", "new": "第一节爱国卫生", "evidence": "公共卫生第一章开篇节标题。"},
    {"old": "第节妇女保健", "new": "第一节妇女保健", "evidence": "保健疗养第五章开篇节标题。"},
    {"old": "第节金融机构管理", "new": "第一节金融机构管理", "evidence": "金融管理第八章开篇节标题。"},
    {"old": "第节\n新海发电厂", "new": "第一节\n新海发电厂", "evidence": "电力工业中主要发电厂章节开篇节标题。"},
    {"old": "第节</p><p>新海发电厂", "new": "第一节</p><p>新海发电厂", "evidence": "分册 HTML 中新海发电厂开篇节标题。"},
    {"old": "第节\n自由市场贸易", "new": "第一节\n自由市场贸易", "evidence": "粮油市场贸易章节开篇节标题。"},
    {"old": "第节</p><p>自由市场贸易", "new": "第一节</p><p>自由市场贸易", "evidence": "分册 HTML 中自由市场贸易开篇节标题。"},
    {"old": "第节\n中国国民党革命委员会连云港市委员会", "new": "第一节\n中国国民党革命委员会连云港市委员会", "evidence": "民主党派地方组织章节开篇节标题。"},
    {"old": "第节</p><p>中国国民党革命委员会连云港市委员会", "new": "第一节</p><p>中国国民党革命委员会连云港市委员会", "evidence": "分册 HTML 中民革连云港市委员会开篇节标题。"},
]

EXCLUDED_PARTS = ["/backup", "backup_", "/obsolete/", "/paddle_", "PaddleOCR", ".bak", "上/序与凡例.md"]


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
        "batch": 286,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "Structural heading typo cleanup for current reader and formal body sources.",
            "TOC OCR file 上/序与凡例.md was intentionally excluded because its 第节 entries are table-of-contents noise requiring separate source review.",
            "No OCR merged files, backups, obsolete files, or historical packages were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/structural_heading_batch286_20260707.md"
    js = ROOT / "output/reports/structural_heading_batch286_20260707.json"
    lines = [
        "# 结构性标题残字补修 batch286",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总；排除目录 OCR 源稿 `上/序与凡例.md`。",
        "- 原则：只处理能由章节结构确认的孤立残字和开篇 `第一节` 标题。",
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
    progress = ROOT / "output/reports/progress/20260707_结构性标题残字补修第二百八十六批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 结构性标题残字补修第二百八十六批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据章节结构定点修复标题残字：`置信访 -> 信访`，以及爱国卫生、妇女保健、金融机构管理、新海发电厂、自由市场贸易、民革连云港市委员会等开篇 `第节 -> 第一节`，共 {total} 处。
- 报告：`output/reports/structural_heading_batch286_20260707.md`；进度：`output/reports/progress/20260707_结构性标题残字补修第二百八十六批.md`。
- 目录 OCR 源稿 `上/序与凡例.md` 的 `第节` 噪声未处理，留待目录专门回源；未处理 OCR merged、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
