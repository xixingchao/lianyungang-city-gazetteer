from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]
REPLACEMENTS = [
    {"old": "淫移物\n品", "new": "淫秽物\n品", "evidence": "收缴淫秽物品的布告语境。"},
    {"old": "淫移物</p><p>品", "new": "淫秽物</p><p>品", "evidence": "收缴淫秽物品的布告语境。"},
    {"old": "淫移物 品", "new": "淫秽物品", "evidence": "收缴淫秽物品的布告语境。"},
    {"old": "淫移录像带", "new": "淫秽录像带", "evidence": "查处、收缴淫秽录像带语境。"},
    {"old": "淫移的录音", "new": "淫秽的录音", "evidence": "海关查获黄色、淫秽录音录像带语境。"},
    {"old": "淫移刊物", "new": "淫秽刊物", "evidence": "海关查获未申报淫秽刊物语境。"},
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
    md = ROOT / "output/reports/yinhui_residual_batch296_20260707.md"
    js = ROOT / "output/reports/yinhui_residual_batch296_20260707.json"
    progress = ROOT / "output/reports/progress/20260707_淫秽残留补修第二百九十六批.md"
    lines = ["# 淫秽残留补修 batch296", "", f"- 生成时间：{now}", f"- 修复总数：{total}", "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。", "- 图片处理：未打开、展示或嵌入图片。", "", "## 替换明细"]
    for row in changes:
        for item in row["items"]:
            if item["count"]:
                lines.append(f"- `{row['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    lines.extend(["", "## 残留计数", ""])
    lines.append("- 本批目标短语在当前检查范围中均为 0。" if not left else json.dumps(left, ensure_ascii=False))
    content = "\n".join(lines) + "\n"
    md.write_text(content, encoding="utf-8")
    js.write_text(json.dumps({"batch": 296, "time": now, "total": total, "changes": changes, "residuals": left}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    progress.write_text(content, encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 淫秽残留补修第二百九十六批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据查禁/收缴/海关走私上下文，补修 batch295 后残留的 `淫移物品/淫移录像带/淫移刊物 -> 淫秽物品/淫秽录像带/淫秽刊物` 等窄短语，共 {total} 处。
- 报告：`output/reports/yinhui_residual_batch296_20260707.md`；进度：`output/reports/progress/20260707_淫秽残留补修第二百九十六批.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
        memory.write_text(old.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")
    print(f"total={total}")
    print(f"residuals={json.dumps(left, ensure_ascii=False)}")
    print(f"report={md}")


if __name__ == "__main__":
    main()
