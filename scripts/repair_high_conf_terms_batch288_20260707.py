from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOTS = [ROOT / "output/final_reader", ROOT / "workbench/body_chapters"]

REPLACEMENTS = [
    {"old": "道土道善", "new": "道士吴道善", "evidence": "全书正式阅读稿同段已为道士吴道善；宗教人物语境。"},
    {"old": "道土", "new": "道士", "evidence": "道教人物、道教人员和李白诗题语境。"},
    {"old": "人至真", "new": "入至真", "evidence": "应召入至真观的入观语境。"},
    {"old": "后人天台", "new": "后入天台", "evidence": "后入天台山的迁入/入山语境。"},
    {"old": "红萝下于", "new": "红萝卜干", "evidence": "酱园加工红萝卜干、大头菜、甜闷瓜等腌制品语境。"},
    {"old": "庵一息", "new": "奄奄一息", "evidence": "粮油贸易市场衰败语境。"},
    {"old": "兰中全会", "new": "三中全会", "evidence": "中国共产党十一届三中全会固定史实。"},
    {"old": "理学学土学位", "new": "理学学士学位", "evidence": "学位名固定写法；避免误伤大学土木科。"},
    {"old": "内阁学土", "new": "内阁学士", "evidence": "清代官名固定写法；避免误伤大学土木科。"},
    {"old": "季大钊", "new": "李大钊", "evidence": "《新青年》主办者、与陈独秀并列演讲者均为李大钊。"},
    {"old": "加人中国", "new": "加入中国", "evidence": "加入中国共产党、加入中国科技报研究会等组织加入语境。"},
    {"old": "加人国民党", "new": "加入国民党", "evidence": "个人身份加入政党语境。"},
    {"old": "考人南京", "new": "考入南京", "evidence": "考入学校语境。"},
    {"old": "考人江苏", "new": "考入江苏", "evidence": "考入学校语境。"},
    {"old": "考人上海", "new": "考入上海", "evidence": "考入学校语境。"},
    {"old": "考人山东", "new": "考入山东", "evidence": "考入学校语境。"},
    {"old": "考人私立", "new": "考入私立", "evidence": "考入学校语境。"},
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
    report = {
        "batch": 288,
        "time": now,
        "total": total,
        "changes": changes,
        "residuals": left,
        "notes": [
            "High-confidence proper-name, fixed-phrase, organization-join, and school-admission typo cleanup.",
            "学土 was repaired only in narrow phrases to avoid damaging 大学土木科.",
            "善长三玄 was intentionally left unchanged because it needs source-page evidence before changing to 擅长.",
            "No OCR merged files, backups, obsolete files, package files, or historical outputs were changed.",
            "No image display was used.",
        ],
    }
    md = ROOT / "output/reports/high_conf_terms_batch288_20260707.md"
    js = ROOT / "output/reports/high_conf_terms_batch288_20260707.json"
    lines = [
        "# 高置信正文残字补修 batch288",
        "",
        f"- 生成时间：{now}",
        f"- 修复总数：{total}",
        "- 范围：当前正式阅读 HTML、正式正文源稿/汇总。",
        "- 原则：只处理上下文明确的专名、固定史实、入观/入党/考入学校等窄短语。",
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
    progress = ROOT / "output/reports/progress/20260707_高置信正文残字补修第二百八十八批.md"
    progress.write_text(report_md.read_text(encoding="utf-8"), encoding="utf-8")
    memory = ROOT / "PROJECT_MEMORY.md"
    marker = "## 2026-07-07 高置信正文残字补修第二百八十八批"
    old = memory.read_text(encoding="utf-8") if memory.exists() else ""
    if marker not in old:
        addition = f"""
{marker}

- 依据上下文定点修复当前正式阅读 HTML 与正式正文源稿/汇总中的高置信残字：道教人物/诗题 `道土 -> 道士`，`人至真 -> 入至真`、`后人天台 -> 后入天台`，菜名 `红萝下于 -> 红萝卜干`，固定语 `庵一息 -> 奄奄一息`，史实 `兰中全会 -> 三中全会`，窄模式 `学土 -> 学士`，专名 `季大钊 -> 李大钊`，以及源层 `加人中国/国民党 -> 加入...`、`考人南京/江苏/上海/山东/私立 -> 考入...`，共 {total} 处。
- 报告：`output/reports/high_conf_terms_batch288_20260707.md`；进度：`output/reports/progress/20260707_高置信正文残字补修第二百八十八批.md`。
- `学土` 未全局替换，避免误伤 `大学土木科`；`善长三玄` 证据不足未处理；未处理 OCR merged、backup、obsolete、历史交付包；未打开、展示或嵌入图片。
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
