from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]

REPLACEMENTS = [
    {"old": "关手目前形势", "new": "关于目前形势", "evidence": "报告题名固定搭配。"},
    {"old": "送莱送饭", "new": "送菜送饭", "evidence": "拥军支前慰问语境，莱为菜形近误识。"},
    {"old": "娟妓", "new": "娼妓", "evidence": "收容、检举娼妓语境。"},
    {"old": "卖淫缥娟", "new": "卖淫嫖娼", "evidence": "治安司法查禁卖淫嫖娼固定搭配。"},
    {"old": "抓获卖淫缥娟者", "new": "抓获卖淫嫖娼者", "evidence": "治安司法查禁卖淫嫖娼固定搭配。"},
    {"old": "学寸期满", "new": "学习期满", "evidence": "技校学生学习期满语境。"},
    {"old": "学寸雷锋", "new": "学习雷锋", "evidence": "学雷锋活动语境。"},
    {"old": "学寸毛泽东著作", "new": "学习毛泽东著作", "evidence": "学生学习毛泽东著作语境。"},
    {"old": "主要学寸“", "new": "主要学习“", "evidence": "干部培训学习课程语境。"},
    {"old": "到八路军一一五师学寸", "new": "到八路军一一五师学习", "evidence": "参军女青年到部队学习语境。"},
    {"old": "总产614.9公斤", "new": "总产614.9万公斤", "evidence": "14.25万亩、单产43公斤对应总产约614万公斤。"},
    {"old": "超过于元", "new": "超过千元", "evidence": "庭院生产收入超过千元语境。"},
    {"old": "10方余人次", "new": "10万余人次", "evidence": "演出100余场、观众10万余人次语境。"},
    {"old": "剧自近于部", "new": "剧目近千部", "evidence": "剧团移植上演剧目数量语境。"},
    {"old": "淮海剧团和灌云县准海剧团", "new": "淮海剧团和灌云县淮海剧团", "evidence": "前后均为淮海剧团，准为淮形近误识。"},
    {"old": "提拨", "new": "提拔", "evidence": "干部任用、提拔干部固定写法。"},
    {"old": "于部任领导", "new": "干部任领导", "evidence": "选拔干部任领导职务语境。"},
    {"old": "各级领导于部", "new": "各级领导干部", "evidence": "普法重点对象各级领导干部语境。"},
    {"old": "100名于部", "new": "100名干部", "evidence": "人事局抽调干部语境。"},
    {"old": "于部每夜补助", "new": "干部每夜补助", "evidence": "国防建设施工干部、民工补助并列语境。"},
    {"old": "千部", "new": "干部", "evidence": "干部管理、干部培训、干部学校、干部四化等语境；近千部已预保护。"},
]

EXCLUDED_PARTS = ["/backup", "backup_", "/obsolete/", "/package/", "/paddle_", "PaddleOCR", ".bak"]
PROTECT = [("近千部", "近__PROTECT_QIANBU__")]


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
        for old, token in PROTECT:
            text = text.replace(old, token)
        items = []
        for item in REPLACEMENTS:
            count = text.count(item["old"])
            if count:
                text = text.replace(item["old"], item["new"])
            items.append({**item, "count": count})
        for old, token in PROTECT:
            text = text.replace(token, old)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="")
            changes.append({"path": rel, "items": items})
    return changes


def residuals():
    found = {}
    for rel, path in iter_targets():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for old, token in PROTECT:
            text = text.replace(old, token)
        hits = {item["old"]: text.count(item["old"]) for item in REPLACEMENTS if text.count(item["old"])}
        if hits:
            found[rel] = hits
    return found


def write_report(changes, left):
    total = sum(item["count"] for row in changes for item in row["items"])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = {
        "batch": 289,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "High-confidence OCR typo cleanup for fixed phrases in current reader and formal body sources.",
            "近千部 was protected before the 千部->干部 replacement to preserve the valid quantity phrase.",
            "1990年14月 and other date-like ambiguities were intentionally left for source-page review.",
            "No OCR merged files, backups, obsolete files, package files, or historical outputs were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/high_conf_terms_batch289_20260707.md"
    js = ROOT / "output/reports/high_conf_terms_batch289_20260707.json"
    lines = [
        "# 高置信正文残字补修 batch289",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。",
        "- 原则：只处理上下文明确的固定搭配、形近误识和可用数字校验确认的单位残字。",
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
    progress = ROOT / "output/reports/progress/20260707_高置信正文残字补修第二百八十九批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 高置信正文残字补修第二百八十九批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文定点修复当前正式阅读 HTML 与正式正文源稿/汇总中的高置信残字：`关手目前形势 -> 关于目前形势`、`送莱送饭 -> 送菜送饭`、`娟妓 -> 娼妓`、`卖淫缥娟 -> 卖淫嫖娼`、`学寸 -> 学习` 窄短语、`总产614.9公斤 -> 总产614.9万公斤`、`超过于元 -> 超过千元`、`10方余人次 -> 10万余人次`、`剧自近于部 -> 剧目近千部`、`提拨 -> 提拔`，以及干部语境 `千部/于部 -> 干部`，共 {total} 处。
- 报告：`output/reports/high_conf_terms_batch289_20260707.md`；进度：`output/reports/progress/20260707_高置信正文残字补修第二百八十九批.md`。
- `近千部` 已预保护，未被 `千部 -> 干部` 误伤；`1990年14月` 等日期疑点未回源前不处理；未处理 OCR merged、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
