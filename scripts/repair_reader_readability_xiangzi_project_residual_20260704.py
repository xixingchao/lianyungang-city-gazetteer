# -*- coding: utf-8 -*-
"""Repair source-checked 项自 -> 项目 OCR slips in final reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_xiangzi_project_residual_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_xiangzi_project_residual_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_项自项目残留回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/paddle_ocr/中/part01/page_0107.txt:26-27; page_0273.txt:13; "
    "page_0320.txt:37-39; page_0422.txt:48; page_0431.txt:28,34; page_0503.txt:25-26; "
    "workbench/ocr/paddle_ocr/中/part02/page_0190.txt:21-22; page_0371.txt:6-10; "
    "workbench/ocr/paddle_ocr/下/part01/page_0428.txt:16-18; page_0455.txt:39; "
    "workbench/ocr/paddle_ocr/下/part02/page_0422.txt:40; page_0423.txt:4-7; page_0424.txt:7"
)

REPLACEMENTS = [
    ("食品淀粉生产项目", "该项自由扬州“五一”食品厂帮助设计", "该项目由扬州“五一”食品厂帮助设计", "中/part01/page_0107.txt:26-27"),
    ("电子技改项目完成", "全部技术引进和技术改造项自完成", "全部技术引进和技术改造项目完成", "章节源+同类项目语境"),
    ("建材优秀项目奖", "国家优秀项自奖", "国家优秀项目奖", "中/part01/page_0273.txt:13"),
    ("建筑啤酒厂安装项目", "啤酒广安装项自有", "啤酒厂安装项目有", "中/part01/page_0320.txt:37"),
    ("电力一般项目", "一般项自有定额", "一般项目有定额", "章节源+同句项目审批制度"),
    ("开发区三资项目", "“三资”项自和高效益", "“三资”项目和高效益", "中/part01/page_0422.txt:48"),
    ("开发区狠抓项目资金", "狠抓项自、资金的引进", "狠抓项目、资金的引进", "中/part01/page_0431.txt:28"),
    ("开发区项目引进序幕", "开发区项自引进工作的序幕", "开发区项目引进工作的序幕", "中/part01/page_0431.txt:34"),
    ("口岸重点建设项目", "重点建设项自之一", "重点建设项目之一", "章节源+同类重点建设项目"),
    ("口岸统计项目", "对项自进行解除", "对项目进行解除", "中/part01/page_0503.txt:25-26"),
    ("外贸项目批件", "配齐项自批件", "配齐项目批件", "中/part02/page_0190.txt:21-22"),
    ("税务回收投资项目", "回收投资时间长的项自", "回收投资时间长的项目", "章节源+同句项目并列"),
    ("金融批准项目", "经审定批准项自：113个", "经审定批准项目：113个", "中/part02/page_0371.txt:6"),
    ("劳动安全技术措施项目", "安全技术措施项自范围", "安全技术措施项目范围", "章节源+表题"),
    ("外事东辛奶牛项目", "东辛奶牛项自协调会", "东辛奶牛项目协调会", "章节源+同句投资合作"),
    ("科技星火计划项目", "4个“星火计划”项自", "4个“星火计划”项目", "下/part01/page_0428.txt:16-18"),
    ("科技监测项目", "饮用水两个项自", "饮用水两个项目", "下/part01/page_0455.txt:39"),
    ("附录这批项目", "这批项自投产后", "这批项目投产后", "下/part02/page_0423.txt:4-7"),
    ("附录技术改造项目", "第一期技术改造项自需五亿元", "第一期技术改造项目需五亿元", "下/part02/page_0424.txt:7"),
]

SKIPPED = ["`这是一项自动控制多` 中的 `项自` 为合法跨词片段，本批保留。"]


def patch_reader() -> dict[str, int]:
    text = HTML.read_text(encoding="utf-8")
    counts: dict[str, int] = {}
    for label, old, new, _source in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
        elif new not in text:
            raise RuntimeError(f"neither old nor new text found: {label}")
        counts[label] = count
    HTML.write_text(text, encoding="utf-8")
    verify_reader()
    return counts


def verify_reader() -> None:
    text = HTML.read_text(encoding="utf-8")
    missing = [new for _label, _old, new, _source in REPLACEMENTS if new not in text]
    residuals = [old for _label, old, new, _source in REPLACEMENTS if old in text and old not in new]
    if missing or residuals:
        raise RuntimeError(f"verification failed: missing={missing}, residuals={residuals}")


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def write_reports(counts: dict[str, int]) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    items = [
        {"label": label, "old": old, "new": new, "source": source, "count": counts[label]}
        for label, old, new, source in REPLACEMENTS
    ]
    payload = {
        "time": now,
        "scope": "多卷正文 `项自` 项目类残留",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "仅修复语境和源文支持为 `项目` 的 `项自`；合法跨词 `一项自动控制` 保留。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 项自/项目残留回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 保留：`这是一项自动控制多` 中的合法跨词片段。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 项自/项目残留回源修复

- 对多卷正文 `项自` 残留做小批回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `该项自由/技术改造项自/国家优秀项自奖/安装项自/三资项自/项自批件/批准项自/星火计划项自/这批项自/技术改造项自` 等 19 项为 `项目`。
- 保留 `这是一项自动控制多` 中的合法跨词片段，不做机械替换。
- 报告：`output/reports/reader_readability_xiangzi_project_residual_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 项自/项目残留回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
