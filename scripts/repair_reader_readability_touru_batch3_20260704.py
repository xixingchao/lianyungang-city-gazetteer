# -*- coding: utf-8 -*-
"""Repair source-checked 投人 -> 投入 slips in remaining multi-volume contexts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_touru_batch3_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_touru_batch3_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_投人投入第三批回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = (
    "workbench/ocr/paddle_ocr/中/part02/page_0056.txt:29; page_0063.txt:21; page_0083.txt:32; "
    "page_0139.txt:21; page_0166.txt:21; page_0231.txt:23; page_0292.txt:4; "
    "page_0339.txt:21; page_0341.txt:6; page_0353.txt:35; page_0397.txt:12; "
    "page_0444.txt:28; page_0472.txt:26; workbench/ocr/paddle_ocr/下/part01/page_0093.txt:40; "
    "page_0098.txt:22; page_0273.txt:28; page_0451.txt:39; page_0453.txt:35; "
    "workbench/ocr/paddle_ocr/下/part02/page_0044.txt:6; page_0391.txt:24; page_0420.txt:6; page_0423.txt:11"
)

REPLACEMENTS = [
    ("铁路营运", "投人营运后，机车牵引定数", "投入营运后，机车牵引定数", "中/part02/page_0056.txt:29"),
    ("白塔埠机场", "1958年竣工，投人使用", "1958年竣工，投入使用", "中/part02/page_0063.txt:21"),
    ("微波通信", "微波通信工程通过验收并投人使用", "微波通信工程通过验收并投入使用", "中/part02/page_0083.txt:32"),
    ("彩电市场", "彩色电视机.1000台，投人市场", "彩色电视机.1000台，投入市场", "中/part02/page_0139.txt:21"),
    ("土地投入", "增加了对土地的投人", "增加了对土地的投入", "中/part02/page_0166.txt:21"),
    ("生油市场", "调人75吨生油投人市场", "调人75吨生油投入市场", "中/part02/page_0231.txt:23"),
    ("农业投入财政", "用于市县农业投人", "用于市县农业投入", "中/part02/page_0292.txt:4"),
    ("印花税检查", "干部投人了检查活动", "干部投入了检查活动", "中/part02/page_0339.txt:21"),
    ("税务投入工作", "抽调214名干部投人工作", "抽调214名干部投入工作", "中/part02/page_0341.txt:6"),
    ("现金投放", "全市共投人现金11.41亿元", "全市共投入现金11.41亿元", "中/part02/page_0353.txt:35"),
    ("固定资产投入", "固定资产投人盲目增加", "固定资产投入盲目增加", "中/part02/page_0397.txt:12"),
    ("反右斗争", "党员投人“反右”斗争", "党员投入“反右”斗争", "中/part02/page_0444.txt:28"),
    ("实验电机生产", "教仪有限公司投人生产", "教仪有限公司投入生产", "中/part02/page_0472.txt:26"),
    ("灭火保卫", "400余人投人灭火及组织安全保卫", "400余人投入灭火及组织安全保卫", "下/part01/page_0093.txt:40"),
    ("在押犯劳动", "在押犯人轮流投人劳动", "在押犯人轮流投入劳动", "下/part01/page_0098.txt:22"),
    ("劳动保护资金", "每年投人大量资金用于改善", "每年投入大量资金用于改善", "下/part01/page_0273.txt:28"),
    ("输液针头", "小儿输液针头投人应用", "小儿输液针头投入应用", "下/part01/page_0451.txt:39"),
    ("过海电缆", "过海电缆投人使用", "过海电缆投入使用", "下/part01/page_0453.txt:35"),
    ("影剧院", "7月1日投人使用", "7月1日投入使用", "下/part02/page_0044.txt:6"),
    ("抗日宣传", "积极投人抗日宣传活动", "积极投入抗日宣传活动", "下/part02/page_0391.txt:24"),
    ("附录农业生产", "全社投人农业生产的78686个劳动日", "全社投入农业生产的78686个劳动日", "下/part02/page_0420.txt:6"),
    ("附录投入少", "兴办投人少、产出多、见效快", "兴办投入少、产出多、见效快", "下/part02/page_0423.txt:11"),
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
        "scope": "交通、邮电、商业、供销、财政、税务、金融、政党、治安司法、劳动、科技、文化、人物、附录 `投人` 残留第三批",
        "source": SOURCE,
        "reader_path": str(HTML),
        "verified_items": len(REPLACEMENTS),
        "current_run_replacements": sum(counts.values()),
        "items": items,
        "skipped": ["第三十二卷名胜旅游 `臭敬梓、投人，开发旅游资源` 为复杂串行残文，本批不凭 `投人` 单点修。"],
        "principle": "仅修复页级 PaddleOCR 明确为 `投入` 的长短语；复杂串行残文另行处理。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 投人/投入第三批回源修复",
        "",
        f"- 时间：{now}",
        f"- 范围：{payload['scope']}",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        f"- 本批核验条目：{payload['verified_items']} 项",
        f"- 本次脚本复跑实际改写：{payload['current_run_replacements']} 处",
        "- 保留：第三十二卷名胜旅游复杂串行残文，需另行整体回源处理。",
        "",
    ]
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")
    memory = f"""
## 2026-07-04 投人/投入第三批回源修复

- 对交通、邮电、商业、供销、财政、税务、金融、政党、治安司法、劳动、科技、文化、人物、附录中的 `投人` 残留做第三批回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `投人营运/投人使用/投人市场/土地的投人/农业投人/投人检查活动/投人工作/投人现金/固定资产投人/投人反右斗争/投人灭火/投人劳动/投人应用/投人抗日宣传/投人农业生产/投人少产出多` 等 22 处为 `投入`。
- 第三十二卷名胜旅游 `臭敬梓、投人，开发旅游资源` 为复杂串行残文，本批不凭单词处理。
- 报告：`output/reports/reader_readability_touru_batch3_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 投人/投入第三批回源修复", memory)


def main() -> None:
    counts = patch_reader()
    write_reports(counts)
    print(json.dumps({"current_run_replacements": sum(counts.values()), "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
