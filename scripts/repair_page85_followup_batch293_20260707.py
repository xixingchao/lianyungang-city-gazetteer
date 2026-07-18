from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]
SOURCE_EVIDENCE = "workbench/ocr/paddle_ocr/下/part01/page_0085.txt"

REPLACEMENTS = [
    {"old": "大家检举娟</p><p>妓", "new": "大家检举娼</p><p>妓", "evidence": "页级 OCR 为 大家检举娼妓。"},
    {"old": "大家检举娟 妓", "new": "大家检举娼妓", "evidence": "页级 OCR 为 大家检举娼妓。"},
    {"old": "卖淫娟案", "new": "卖淫嫖娼案", "evidence": "页级 OCR 为 卖淫嫖娼案103起。"},
    {"old": "卖淫缥婚案", "new": "卖淫嫖娼案", "evidence": "页级 OCR 为 卖淫嫖娼案24起。"},
    {"old": "查获淫物品", "new": "查获淫秽物品", "evidence": "页级 OCR 小标题为 查获淫秽物品。"},
    {"old": "反动淫书刊", "new": "反动淫秽书刊", "evidence": "页级 OCR 为 反动淫秽书刊。"},
    {"old": "淫移物品", "new": "淫秽物品", "evidence": "页级 OCR 为 淫秽物品。"},
    {"old": "淫秒物品", "new": "淫秽物品", "evidence": "页级 OCR 为 淫秽物品。"},
    {"old": "淫移画报", "new": "淫秽画报", "evidence": "页级 OCR 为 淫秽画报图片挂历。"},
    {"old": "3方余件", "new": "3万余件", "evidence": "页级 OCR 为 非法印刷品3万余件。"},
    {"old": "传播秽物品案", "new": "传播淫秽物品案", "evidence": "页级 OCR 为 传播淫秽物品案。"},
    {"old": "市区248</p><p>公安机关", "new": "市区248</p><p>名巫婆、神汉中，恢复活动的有198名，29名测字相命、阴阳先生中，重操旧业的有25人，</p><p>公安机关", "evidence": "页级 OCR 补足 248名巫婆、神汉... 段落。"},
    {"old": "市区248 公安机关", "new": "市区248名巫婆、神汉中，恢复活动的有198名，29名测字相命、阴阳先生中，重操旧业的有25人，公安机关", "evidence": "页级 OCR 补足 248名巫婆、神汉... 段落。"},
]

EXCLUDED_PARTS = ["/backup", "backup_", "/obsolete/", "/package/", "/paddle_", "PaddleOCR", ".bak"]


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
    md = ROOT / "output/reports/page85_followup_batch293_20260707.md"
    js = ROOT / "output/reports/page85_followup_batch293_20260707.json"
    report = {"batch": 293, "time": now, "total": total, "changes": changes, "residuals": left, "source_evidence": SOURCE_EVIDENCE, "notes": ["Page-backed follow-up cleanup for 下册 page_0085.", "No image display was used."]}
    lines = [
        "# 下册第85页页级 OCR 追加补修 batch293",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。",
        f"- 页级证据：`{SOURCE_EVIDENCE}`。",
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
    progress = ROOT / "output/reports/progress/20260707_下册第85页页级OCR追加补修第二百九十三批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 下册第85页页级OCR追加补修第二百九十三批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据页级 OCR `{SOURCE_EVIDENCE}`，追加补修下册第85页同段残留：`卖淫娟案/卖淫缥婚案 -> 卖淫嫖娼案`、`大家检举娟妓 -> 大家检举娼妓`、多处 `淫移/淫秒/淫 -> 淫秽`、`3方余件 -> 3万余件`，并补足 `市区248名巫婆、神汉...` 段落，共 {total} 处。
- 报告：`output/reports/page85_followup_batch293_20260707.md`；进度：`output/reports/progress/20260707_下册第85页页级OCR追加补修第二百九十三批.md`。
- `依法速捕` 等跨章源层疑点另行分批处理；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
