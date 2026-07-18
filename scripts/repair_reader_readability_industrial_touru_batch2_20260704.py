# -*- coding: utf-8 -*-
"""Repair source-checked 投人 -> 投入 slips in industrial/development sections."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_industrial_touru_batch2_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_industrial_touru_batch2_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_工业开发区投人投入第二批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/paddle_ocr/中/part01/page_0089.txt:138; page_0110.txt:13; "
    "page_0195.txt:17; page_0208.txt:17; page_0211.txt:18; page_0221.txt:35; "
    "page_0227.txt:11; page_0229.txt:13; page_0273.txt:21; page_0279.txt:26; "
    "page_0289.txt:15,37; page_0291.txt:4,20; page_0423.txt:12,21; "
    "page_0424.txt:18; page_0434.txt:18; page_0444.txt:16"
)

REPLACEMENTS = [
    ("汽水小批量", "制成汽水，并投人小批量生产", "制成汽水，并投入小批量生产", "中/part01/page_0089.txt:138"),
    ("糖浆投产", "糖浆试制成功并投人生产", "糖浆试制成功并投入生产", "中/part01/page_0110.txt:13"),
    ("深耕犁耕作", "五铧犁成功并投人耕作", "五铧犁成功并投入耕作", "中/part01/page_0195.txt:17"),
    ("锅炉车间使用", "3160平方米车间投人使用", "3160平方米车间投入使用", "中/part01/page_0208.txt:17"),
    ("BA水泵生产", "BA型水泵全系列17个品种29个规格全部投人生产", "BA型水泵全系列17个品种29个规格全部投入生产", "中/part01/page_0211.txt:18"),
    ("漆包线试生产", "漆包线生产设备安装完毕。1988年投人试生产", "漆包线生产设备安装完毕。1988年投入试生产", "中/part01/page_0221.txt:35"),
    ("弓锯床批产", "通过省级技术鉴定，投人批量生产", "通过省级技术鉴定，投入批量生产", "中/part01/page_0227.txt:11"),
    ("连利水表试产", "连利水表有限公司投人试生产", "连利水表有限公司投入试生产", "中/part01/page_0229.txt:13"),
    ("砖瓦试生产", "1984年秋投人试生产", "1984年秋投入试生产", "中/part01/page_0273.txt:21"),
    ("水泥运行", "年底投人运行", "年底投入运行", "中/part01/page_0279.txt:26"),
    ("高铝粉设备", "安装并投人使用，提高了高铝粉", "安装并投入使用，提高了高铝粉", "中/part01/page_0289.txt:15"),
    ("岩棉批产", "岩棉制品成功，并投人批量生产", "岩棉制品成功，并投入批量生产", "中/part01/page_0289.txt:37"),
    ("釉面砖生产", "釉面砖开始投人生产", "釉面砖开始投入生产", "中/part01/page_0291.txt:4"),
    ("防腐涂料试产", "装置。当年投人试生产", "装置。当年投入试生产", "中/part01/page_0291.txt:20"),
    ("基础设施投入", "加大基础设施投人，改善居住环境", "加大基础设施投入，改善居住环境", "中/part01/page_0423.txt:12"),
    ("教育投入", "加大教育投人，到2000年", "加大教育投入，到2000年", "中/part01/page_0423.txt:21"),
    ("供电线路使用", "两条10千伏供电线路投人使用", "两条10千伏供电线路投入使用", "中/part01/page_0424.txt:18"),
    ("饲料公司投产", "同年7月投人生产，年生产饲料能力", "同年7月投入生产，年生产饲料能力", "中/part01/page_0434.txt:18"),
    ("临时货栈使用", "临时货栈同期投人使用", "临时货栈同期投入使用", "中/part01/page_0444.txt:16"),
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
    residuals = [old for _label, old, _new, _source in REPLACEMENTS if old in text]
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
        "scope": "食品、机械、建材、开发区、口岸 `投人` 残留第二批",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "principle": "仅修复页级 PaddleOCR 明确为 `投入` 的长短语；不做全局 `投人` 替换。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 工业开发区投人/投入第二批回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验条目：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 政治运动、人物、附录等语境中的 `投人` 未在本批处理。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 工业开发区投人/投入第二批回源修复

- 对食品、机械、建材、开发区、口岸中的 `投人` 残留做第二批回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `投人小批量生产/投人生产/投人耕作/投人使用/投人试生产/投人批量生产/投人运行/基础设施投人/教育投人/货栈同期投人使用` 等 19 处为 `投入`。
- 本批只采用页级 PaddleOCR 明确支持的长短语；其它 `投人` 继续逐页核证。
- 报告：`output/reports/reader_readability_industrial_touru_batch2_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 工业开发区投人/投入第二批回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
