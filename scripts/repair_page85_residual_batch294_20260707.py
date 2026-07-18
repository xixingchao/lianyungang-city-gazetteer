from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "workbench/body_chapters/第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench/body_chapters/连云港市志_全书_正文汇总.md",
]
REPLACEMENTS = [
    {"old": "大家检举娟 妓", "new": "大家检举娼妓", "evidence": "页级 OCR workbench/ocr/paddle_ocr/下/part01/page_0085.txt 为 大家检举娼妓。"},
]


def main():
    changes = []
    for path in TARGETS:
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
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
    for path in TARGETS:
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = {item["old"]: text.count(item["old"]) for item in REPLACEMENTS if text.count(item["old"])}
        if hits:
            left[rel] = hits
    total = sum(item["count"] for row in changes for item in row["items"])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = ROOT / "output/reports/page85_residual_batch294_20260707.md"
    js = ROOT / "output/reports/page85_residual_batch294_20260707.json"
    progress = ROOT / "output/reports/progress/20260707_下册第85页娼妓残留补修第二百九十四批.md"
    lines = [
        "# 下册第85页娼妓残留补修 batch294",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 页级证据：`workbench/ocr/paddle_ocr/下/part01/page_0085.txt`。",
        "- 图片处理：未打开、展示或嵌入图片。",
        "",
        "## 替换明细",
    ]
    for row in changes:
        for item in row["items"]:
            if item["count"]:
                lines.append(f"- `{row['path']}`：`{item['old']}` -> `{item['new']}`；次数 {item['count']}；依据：{item['evidence']}")
    lines.extend(["", "## 残留计数", ""])
    lines.append("- 本批目标短语在当前检查范围中均为 0。" if not left else json.dumps(left, ensure_ascii=False))
    content = "\n".join(lines) + "\n"
    md.write_text(content, encoding="utf-8")
    js.write_text(json.dumps({"batch": 294, "time": now, "total": total, "changes": changes, "residuals": left}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    progress.write_text(content, encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 下册第85页娼妓残留补修第二百九十四批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据页级 OCR `workbench/ocr/paddle_ocr/下/part01/page_0085.txt`，补修 batch293 后源稿中因空格残留的 `大家检举娟 妓 -> 大家检举娼妓`，共 {total} 处。
- 报告：`output/reports/page85_residual_batch294_20260707.md`；进度：`output/reports/progress/20260707_下册第85页娼妓残留补修第二百九十四批.md`。
- 未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
"""
        memory.write_text(old.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")
    print(f"total={total}")
    print(f"residuals={json.dumps(left, ensure_ascii=False)}")
    print(f"report={md}")


if __name__ == "__main__":
    main()
