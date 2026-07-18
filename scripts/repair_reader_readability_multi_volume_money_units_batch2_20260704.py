# -*- coding: utf-8 -*-
"""Second source-verified money-unit repair batch across several volumes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_multi_volume_money_units_batch2_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_multi_volume_money_units_batch2_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_多卷金额单位错识第二批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/paddle_ocr/中/part01/page_0292.txt:21; page_0297.txt:24; "
    "page_0298.txt:30; page_0349.txt:26; page_0401.txt:21; page_0411.txt:100; "
    "page_0413.txt:4; page_0417.txt:26; page_0433.txt:7-8; "
    "workbench/ocr/paddle_ocr/下/part01/page_0242.txt:11; page_0278.txt:16-19"
)

REPLACEMENTS = [
    ("建材塑料门窗产值", "生产线投人试生产。至年底，完成工业总产值150方元，实现利税20方元", "生产线投入试生产。至年底，完成工业总产值150万元，实现利税20万元", "中/part01/page_0292.txt:21"),
    ("建筑勘察节省投资", "节省投资20方元", "节省投资20万元", "中/part01/page_0297.txt:24"),
    ("建筑住宅总投资", "总投资9000方元", "总投资9000万元", "中/part01/page_0298.txt:30"),
    ("电力海盐线投资", "总投资2166.12方元", "总投资2166.12万元", "中/part01/page_0349.txt:26"),
    ("乡镇轻工业产值", "年产值85266方元", "年产值85266万元", "中/part01/page_0401.txt:21"),
    ("青口镇投入资金", "为企业投入资金860方元", "为企业投入资金860万元", "中/part01/page_0411.txt:100"),
    ("赣马镇固定资产", "固定资产原值1095方元", "固定资产原值1095万元", "中/part01/page_0413.txt:4"),
    ("浦南食品厂产值", "1990年创产值500方元", "1990年创产值500万元", "中/part01/page_0417.txt:26"),
    ("钟山氨纶投资", "总投资9571方元，其中港方投入125方美元", "总投资9571万元，其中港方投入125万美元", "中/part01/page_0433.txt:7"),
    ("劳动服务贷款", "无息贷款424方元", "无息贷款424万元", "下/part01/page_0242.txt:11"),
    ("劳动防尘投资", "市绝缘材料广采用风水相结合的防尘措施", "市绝缘材料厂采用风水相结合的防尘措施", "下/part01/page_0278.txt:16"),
    ("锦屏化工防尘", "锦屏化工厂投资70多方元", "锦屏化工厂投资70多万元", "下/part01/page_0278.txt:16"),
    ("重点项目投资", "投资153.9方元", "投资153.9万元", "下/part01/page_0278.txt:19"),
]

SKIPPED = [
    "金融卷、税务卷、文化卷、人物卷等剩余 `方元` 继续逐页核证后再处理。",
]


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
        "scope": "第二十三、二十四、二十五、二十七、二十八、四十七卷",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": SKIPPED,
        "principle": "仅修复页级 OCR 可直接证明为 `万元/万美元` 的金额单位错识及同源短错。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 多卷金额单位错识第二批回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验修复：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 重点：修正 `150方元/20方元/9000方元/2166.12方元/85266方元/860方元/1095方元/500方元/9571方元/125方美元/424方元/70多方元/153.9方元` 等，并同步修正 `投人试生产`、`绝缘材料广`。",
        "- 保留：" + "；".join(SKIPPED),
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 多卷金额单位错识第二批回源修复

- 对第二十三、二十四、二十五、二十七、二十八、四十七卷做第二批金额单位错识回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `150方元/20方元/9000方元/2166.12方元/85266方元/860方元/1095方元/500方元/9571方元/125方美元/424方元/70多方元/153.9方元` → 对应 `万元/万美元`，并同步修正 `投人试生产`→`投入试生产`、`绝缘材料广`→`绝缘材料厂`。
- 金融卷、税务卷、文化卷、人物卷等剩余 `方元` 继续逐页核证后再处理。
- 报告：`output/reports/reader_readability_multi_volume_money_units_batch2_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 多卷金额单位错识第二批回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
