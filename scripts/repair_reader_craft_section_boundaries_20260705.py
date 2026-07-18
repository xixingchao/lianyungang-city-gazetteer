# -*- coding: utf-8 -*-
"""Restore source-backed craft section boundaries in the full reader."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_craft_section_boundaries_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_craft_section_boundaries_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_工艺美术小节边界修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

REPLACEMENTS = [
    {
        "label": "砖雕小节边界",
        "old": "<p>三、砖雕海州现存的唐、宋古建筑上尚能看到精美的砖雕工艺，技法有浮雕、多层雕等，图案有人物、花卉、龙凤、八卦、戏文等。砖雕工艺品多用于古建筑的门楼、檐脊、萧墙等装饰。鼓楼一带现存的砖雕工艺品多数出于近代砖雕名家海州人万桂富之手。万桂富15岁投师学习砖雕技法，18岁自立门户，从事仿古建筑营造，曾参加新浦的鼎丰园、生庆公等大型商号及海州的庙宇、富户住宅的砖雕工程，名扬苏北、鲁南。海州不少居民门旁的装饰性吉祥砖雕工艺“天香楼”皆用古城砖精雕而成。此外，居民建筑物上还遗存不少立雕，如“亮纱脊”、“兽头”、“飞檐”和浮雕“龙盘玉柱”、“万事如意”、“松鹤同春”、“三星高照”等，无不棚栩如生。“文化大革命”期间，海州古建筑砖雕工艺品被作为“四旧”（旧文化、旧思想、旧传统、旧习惯）受到不同程度的破坏。</p>",
        "new": "<h5>三、砖雕</h5>\n<p>海州现存的唐、宋古建筑上尚能看到精美的砖雕工艺，技法有浮雕、多层雕等，图案有人物、花卉、龙凤、八卦、戏文等。砖雕工艺品多用于古建筑的门楼、檐脊、萧墙等装饰。鼓楼一带现存的砖雕工艺品多数出于近代砖雕名家海州人万桂富之手。万桂富15岁投师学习砖雕技法，18岁自立门户，从事仿古建筑营造，曾参加新浦的鼎丰园、生庆公等大型商号及海州的庙宇、富户住宅的砖雕工程，名扬苏北、鲁南。海州不少居民门旁的装饰性吉祥砖雕工艺“天香楼”皆用古城砖精雕而成。此外，居民建筑物上还遗存不少立雕，如“亮纱脊”、“兽头”、“飞檐”和浮雕“龙盘玉柱”、“万事如意”、“松鹤同春”、“三星高照”等，无不棚栩如生。“文化大革命”期间，海州古建筑砖雕工艺品被作为“四旧”（旧文化、旧思想、旧传统、旧习惯）受到不同程度的破坏。</p>",
        "source": "workbench/ocr/raw/中/part01/page_0023.txt:4-14",
    },
    {
        "label": "木雕小节边界",
        "old": "<p>四、木出游》木，一高髻仕女骑坐骏马上，前有侍者牵马，后有侍女跟随。仕女凤仪高贵，悠闲雍容，唐代贵族妇女的形象棚栩如生。</p>",
        "new": "<h5>四、木</h5>\n<p>出游》木，一高髻仕女骑坐骏马上，前有侍者牵马，后有侍女跟随。仕女凤仪高贵，悠闲雍容，唐代贵族妇女的形象棚栩如生。</p>",
        "source": "workbench/ocr/raw/中/part01/page_0023.txt:15-17",
    },
    {
        "label": "泥塑小节边界",
        "old": "<p>五、泥塑东汉佛教传入朐县后，泥塑工艺品在寺庙应运而生。</p>",
        "new": "<h5>五、泥塑</h5>\n<p>东汉佛教传入朐县后，泥塑工艺品在寺庙应运而生。</p>",
        "source": "workbench/ocr/raw/中/part01/page_0023.txt:25-26",
    },
    {
        "label": "贝雕画小节边界",
        "old": "<p>一、贝雕画1965年1月，连云区办贝雕厂。5月，派9人去青岛贝雕厂学习1年。</p>",
        "new": "<h5>一、贝雕画</h5>\n<p>1965年1月，连云区办贝雕厂。5月，派9人去青岛贝雕厂学习1年。</p>",
        "source": "workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:250-251",
    },
    {
        "label": "喷绘画小节边界",
        "old": "<p>三、喷绘画1974年秋，赣榆县工艺厂生产喷绘画。1975年，生产800幅，1976年生产2400幅。由于喷绘画利润低，逐步停产。</p>",
        "new": "<h5>三、喷绘画</h5>\n<p>1974年秋，赣榆县工艺厂生产喷绘画。1975年，生产800幅，1976年生产2400幅。由于喷绘画利润低，逐步停产。</p>",
        "source": "workbench/ocr/raw/中/part01/page_0027.txt:20-22",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    changes = []
    for item in REPLACEMENTS:
        old_count = html.count(item["old"])
        if old_count == 1:
            html = html.replace(item["old"], item["new"], 1)
            status = "changed"
            changed = 1
        elif old_count == 0 and html.count(item["new"]) >= 1:
            status = "already_applied"
            changed = 0
        else:
            raise RuntimeError(f"expected {item['label']} once, got {old_count}")
        changes.append({"label": item["label"], "status": status, "changed": changed, "source": item["source"]})

    HTML.write_text(html, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"time": now, "target": str(HTML.relative_to(ROOT)).replace("\\", "/"), "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 工艺美术小节边界修复",
        "",
        f"- 时间：{now}",
        f"- 范围：`{HTML.relative_to(ROOT)}`。",
        "- 处理：按源 OCR 分行恢复第十七卷工艺美术中 5 个小节标题边界。",
        "",
        "## 结果",
        "",
    ]
    for change in changes:
        lines.append(f"- {change['label']}：{change['status']}，本次变更 {change['changed']}")
        lines.append(f"  - `{change['source']}`")
    text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(text, encoding="utf-8")
    PROGRESS.write_text(text, encoding="utf-8")

    marker = "## 2026-07-05 工艺美术小节边界修复"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 新增并运行 `scripts/repair_reader_craft_section_boundaries_20260705.py`，按源 OCR 分行恢复第十七卷工艺美术 5 个小节标题边界：`三、砖雕`、`四、木`、`五、泥塑`、`一、贝雕画`、`三、喷绘画`。
- 源页证据：`workbench/ocr/raw/中/part01/page_0023.txt:4-26`、`workbench/ocr/raw/中/part01/page_0027.txt:20-22`，贝雕画边界由 `workbench/body_chapters/第十七卷至第二十九卷（中part01）.md:250-251` 支撑。
- 报告：`output/reports/reader_craft_section_boundaries_20260705.md`。
""",
    )

    print("reader_craft_section_boundaries_repaired")
    print(f"changed={sum(change['changed'] for change in changes)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
