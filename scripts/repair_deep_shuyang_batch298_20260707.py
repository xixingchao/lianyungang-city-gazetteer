from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]

REPLACEMENTS = [
    {"old": "深人调查", "new": "深入调查", "evidence": "深入调查研究固定搭配。"},
    {"old": "深人灾区", "new": "深入灾区", "evidence": "慰问团深入灾区慰问语境。"},
    {"old": "深人农村", "new": "深入农村", "evidence": "深入农村开展工作/巡回演出语境。"},
    {"old": "深人盐场", "new": "深入盐场", "evidence": "深入盐场了解生产/演出语境。"},
    {"old": "深人至", "new": "深入至", "evidence": "深入至各用电公社培训农电工语境。"},
    {"old": "深人实际", "new": "深入实际", "evidence": "走出机关、深入实际固定搭配。"},
    {"old": "深人发展", "new": "深入发展", "evidence": "改革开放不断深入发展固定搭配。"},
    {"old": "深人各工厂", "new": "深入各工厂", "evidence": "文化宣传活动深入各工厂、农村语境。"},
    {"old": "江苏述阳", "new": "江苏沭阳", "evidence": "与灌南、响水等县并列的江苏沭阳地名。"},
    {"old": "述阳县", "new": "沭阳县", "evidence": "近现代县名沭阳县语境。"},
    {"old": "述阳等地", "new": "沭阳等地", "evidence": "宿北、宿迁、东海、灌云、沭阳等地水灾语境。"},
    {"old": "述阳、灌云", "new": "沭阳、灌云", "evidence": "海属四县/路南东海等近现代地名并列语境。"},
    {"old": "述阳十字桥", "new": "沭阳十字桥", "evidence": "宿北新安镇及沭阳十字桥决堤放水语境。"},
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
    md = ROOT / "output/reports/deep_shuyang_batch298_20260707.md"
    js = ROOT / "output/reports/deep_shuyang_batch298_20260707.json"
    progress = ROOT / "output/reports/progress/20260707_深入与沭阳窄语境补修第二百九十八批.md"
    lines = ["# 深入与沭阳窄语境补修 batch298", "", f"- 生成时间：{now}", f"- 修复总数：{total}", "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。", "- 原则：只处理已抽样确认的深入固定搭配和近现代沭阳地名语境。", "- 图片处理：未打开、展示或嵌入图片。", "", "## 替换明细"]
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
    js.write_text(json.dumps({"batch": 298, "time": now, "total": total, "changes": changes, "residuals": left}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    progress.write_text(content, encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 深入与沭阳窄语境补修第二百九十八批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文抽样，窄语境补修 `深人调查/灾区/农村/盐场/至/实际/发展/各工厂 -> 深入...`，以及近现代地名 `江苏述阳/述阳县/述阳等地/述阳、灌云/述阳十字桥 -> 沭阳...`，共 {total} 处。
- 报告：`output/reports/deep_shuyang_batch298_20260707.md`；进度：`output/reports/progress/20260707_深入与沭阳窄语境补修第二百九十八批.md`。
- `沐阳`、`胸山`、古文/建置疑点未回源前不处理；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
        memory.write_text(old.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")
    print(f"total={total}")
    print(f"residuals={json.dumps(left, ensure_ascii=False)}")
    print(f"report={md}")


if __name__ == "__main__":
    main()
