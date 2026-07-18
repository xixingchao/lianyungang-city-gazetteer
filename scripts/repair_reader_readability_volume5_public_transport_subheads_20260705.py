# -*- coding: utf-8 -*-
"""Repair source-backed public transport subheading boundaries in volume 5."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_volume5_public_transport_subheads_20260705.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_volume5_public_transport_subheads_20260705.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260705_第五卷公共交通小标题边界补修.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"
SOURCE = "workbench/body_chapters/连云港市志_上册_正文汇总.md"

REPAIRS = [
    {
        "label": "三、客运机动车 / 机动三轮车",
        "source": f"{SOURCE}:18505-18511",
        "old": "<p>三、客运机动车机动三轮车1970年，新浦搬运营业所在人力客运三轮车上安装小型汽油机，改制成机动客运三轮车，同年共改装7辆。",
        "new": "<h5>三、客运机动车</h5>\n<p><strong>机动三轮车</strong>1970年，新浦搬运营业所在人力客运三轮车上安装小型汽油机，改制成机动客运三轮车，同年共改装7辆。",
    },
    {
        "label": "公共汽车",
        "source": f"{SOURCE}:18511",
        "old": "<p>公共汽车 民国时期，当地行驶的客运汽车大都是在货车上搭棚布改制成的，群众称之为“敞口车”，汽车均为外国制造。",
        "new": "<p><strong>公共汽车</strong> 民国时期，当地行驶的客运汽车大都是在货车上搭棚布改制成的，群众称之为“敞口车”，汽车均为外国制造。",
    },
    {
        "label": "出租汽车",
        "source": f"{SOURCE}:18581",
        "old": "109 车队出租汽车1985年4月，市中北汽车出租公司在新浦成立，有30馀辆轿车、面包车跑市内外客运。",
        "new": "109 车队</p>\n<p><strong>出租汽车</strong>1985年4月，市中北汽车出租公司在新浦成立，有30馀辆轿车、面包车跑市内外客运。",
    },
]


def append_once(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def patch_html() -> list[dict[str, str]]:
    text = HTML.read_text(encoding="utf-8")
    fixed: list[dict[str, str]] = []
    for item in REPAIRS:
        count = text.count(item["old"])
        if count != 1:
            raise RuntimeError(f"expected one match for {item['label']}, got {count}")
        text = text.replace(item["old"], item["new"], 1)
        fixed.append({"label": item["label"], "source": item["source"]})
    HTML.write_text(text, encoding="utf-8")
    return fixed


def main() -> None:
    fixed = patch_html()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第五卷城乡建设 / 第三章公用事业 / 第三节公共交通",
        "html_boundaries_fixed": len(fixed),
        "fixed": fixed,
        "notes": ["恢复客运机动车 h5 和三处小类标题边界；公交表残文未在本轮重建。"],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五卷公共交通小标题边界补修

- 时间：{now}
- 范围：第五卷城乡建设 / 第三章公用事业 / 第三节公共交通。
- 本次修复边界：{len(fixed)} 处。

## 修复

"""
    md += "".join(f"- `{item['label']}`（依据 `{item['source']}`）\n" for item in fixed)
    md += "\n## 说明\n\n- 仅恢复源文可证明的小标题/小类标题边界，不改正文。\n- `出租汽车` 前仍保留公交表残文，表格重建另行回源处理。\n"
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-05 第五卷公共交通小标题边界补修"
    append_once(
        MEMORY,
        marker,
        f"""
{marker}
- 修复第五卷公共交通 3 处标题边界：`三、客运机动车`、`公共汽车`、`出租汽车`。
- 依据 `{SOURCE}:18505-18581`；只拆标题边界，不重建公交营运情况表。
- 报告：`output/reports/reader_readability_volume5_public_transport_subheads_20260705.md`。
""",
    )
    print(f"html_boundaries_fixed={len(fixed)}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
