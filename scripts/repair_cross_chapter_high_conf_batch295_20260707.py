from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]

REPLACEMENTS = [
    {"old": "依法速捕", "new": "依法逮捕", "evidence": "公安司法依法逮捕固定表述。"},
    {"old": "速捕", "new": "逮捕", "evidence": "抓捕、被捕、逮捕法办等语境，速为逮形近误识。"},
    {"old": "卖淫缥、复制", "new": "卖淫嫖娼、复制", "evidence": "公共场所整顿查处卖淫嫖娼、复制贩卖传播淫秽物品语境。"},
    {"old": "卖淫缥婚", "new": "卖淫嫖娼", "evidence": "卖淫嫖娼固定搭配。"},
    {"old": "卖淫娟", "new": "卖淫嫖娼", "evidence": "除六害、治安司法卖淫嫖娼语境。"},
    {"old": "黄色、淫移、反动", "new": "黄色、淫秽、反动", "evidence": "禁止进口黄色、淫秽、反动印刷品固定搭配。"},
    {"old": "淫移书刊", "new": "淫秽书刊", "evidence": "查禁和收缴淫秽书刊语境。"},
    {"old": "淫移物品", "new": "淫秽物品", "evidence": "收缴/传播淫秽物品固定搭配。"},
    {"old": "禁娟", "new": "禁烟", "evidence": "设立戒烟所和良济所整治吸食鸦片者和禁烟语境。"},
    {"old": "罄粟", "new": "罂粟", "evidence": "禁种罂粟、罂粟苗、罂粟碱等固定写法。"},
    {"old": "籁榆县", "new": "赣榆县", "evidence": "表注同列赣榆县，籁为赣形近误识。"},
    {"old": "整伤风化", "new": "整饬风化", "evidence": "民政概述整饬风化固定搭配。"},
    {"old": "对镇级政权进行整伤", "new": "对镇级政权进行整顿", "evidence": "镇级政权整顿语境。"},
    {"old": "撇获反对", "new": "捉获反对", "evidence": "带领青年妇女捉获地主游街示众语境。"},
    {"old": "先人后已", "new": "先人后己", "evidence": "雷锋精神先人后己固定表述。"},
    {"old": "准阳馄饨", "new": "淮阳馄饨", "evidence": "餐饮风味中淮阳馄饨，准为淮形近误识。"},
    {"old": "准阳等县", "new": "淮阳等县", "evidence": "与涟水、赣榆、淮阴、灌南等县并列的淮阳地名语境。"},
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
    md = ROOT / "output/reports/cross_chapter_high_conf_batch295_20260707.md"
    js = ROOT / "output/reports/cross_chapter_high_conf_batch295_20260707.json"
    report = {"batch": 295, "time": now, "total": total, "changes": changes, "residuals": left, "notes": ["Cross-chapter high-confidence OCR typo cleanup.", "沐阳 was intentionally left for source-page review.", "No image display was used."]}
    lines = [
        "# 跨章高置信残字补修 batch295",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。",
        "- 原则：只处理抽样均能坐实的固定搭配、地名/药名形近误识和治安司法术语。",
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
    progress = ROOT / "output/reports/progress/20260707_跨章高置信残字补修第二百九十五批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 跨章高置信残字补修第二百九十五批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据当前正式阅读 HTML 与正式正文源稿/汇总上下文，跨章补修高置信 OCR 残字：`速捕 -> 逮捕`、`依法速捕 -> 依法逮捕`、卖淫嫖娼/淫秽物品相关残字、`罄粟 -> 罂粟`、`籁榆县 -> 赣榆县`、`整伤风化 -> 整饬风化`、`对镇级政权进行整伤 -> 对镇级政权进行整顿`、`撇获反对 -> 捉获反对`、`先人后已 -> 先人后己`、`准阳 -> 淮阳` 窄短语，共 {total} 处。
- 报告：`output/reports/cross_chapter_high_conf_batch295_20260707.md`；进度：`output/reports/progress/20260707_跨章高置信残字补修第二百九十五批.md`。
- `沐阳` 等历史建置/地名疑点未回源前不处理；未处理 OCR 源文件、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
