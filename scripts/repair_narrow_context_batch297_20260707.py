from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]

REPLACEMENTS = [
    {"old": "深人城乡", "new": "深入城乡", "evidence": "深入城乡开展演唱/反奸诉苦运动语境。"},
    {"old": "深人开展", "new": "深入开展", "evidence": "深入开展政治协商、节约用水等固定搭配。"},
    {"old": "深人贯彻", "new": "深入贯彻", "evidence": "深入贯彻路线方针政策固定搭配。"},
    {"old": "深人基层", "new": "深入基层", "evidence": "深入基层演出/帮助工作/普查语境。"},
    {"old": "村民酿，党委审定", "new": "村民酝酿，党委审定", "evidence": "候选人提名、酝酿、审定程序语境。"},
    {"old": "东海、述阳、灌云", "new": "东海、沭阳、灌云", "evidence": "与东海、灌云并列县名，正式阅读稿同段为沭阳。"},
    {"old": "东海、述阳、灌云三县", "new": "东海、沭阳、灌云三县", "evidence": "东海、沭阳、灌云三县会剿语境。"},
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


def main():
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
    left = {}
    for rel, path in iter_targets():
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = {item["old"]: text.count(item["old"]) for item in REPLACEMENTS if text.count(item["old"])}
        if hits:
            left[rel] = hits
    total = sum(item["count"] for row in changes for item in row["items"])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = ROOT / "output/reports/narrow_context_batch297_20260707.md"
    js = ROOT / "output/reports/narrow_context_batch297_20260707.json"
    progress = ROOT / "output/reports/progress/20260707_窄语境残字补修第二百九十七批.md"
    lines = ["# 窄语境残字补修 batch297", "", f"- 生成时间：{now}", f"- 修复总数：{total}", "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。", "- 原则：只处理已抽样确认的深入、酝酿、沭阳窄语境。", "- 图片处理：未打开、展示或嵌入图片。", "", "## 替换明细"]
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
    content = "\n".join(lines) + "\n"
    md.write_text(content, encoding="utf-8")
    js.write_text(json.dumps({"batch": 297, "time": now, "total": total, "changes": changes, "residuals": left}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    progress.write_text(content, encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 窄语境残字补修第二百九十七批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文与正式阅读稿对照，窄语境补修 `深人城乡/开展/贯彻/基层 -> 深入...`、`村民酿，党委审定 -> 村民酝酿，党委审定`、`东海、述阳、灌云 -> 东海、沭阳、灌云`，共 {total} 处。
- 报告：`output/reports/narrow_context_batch297_20260707.md`；进度：`output/reports/progress/20260707_窄语境残字补修第二百九十七批.md`。
- `沐阳`、`胸山`、`善长三玄`、`了若指掌` 等未回源前不处理；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
        memory.write_text(old.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")
    print(f"total={total}")
    print(f"residuals={json.dumps(left, ensure_ascii=False)}")
    print(f"report={md}")


if __name__ == "__main__":
    main()
