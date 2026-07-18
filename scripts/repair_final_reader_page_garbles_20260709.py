from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    ROOT / "output" / "final_reader" / "连云港市志_全书.html",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
    ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
]

REPLACEMENTS = [
    {
        "label": "reader_price_page_number",
        "old": "<p>· 458·</p>",
        "new": "",
        "paths": [ROOT / "output" / "final_reader" / "连云港市志_全书.html"],
    },
    {
        "label": "reader_education_table_page_2198",
        "old": "<p>:2198·</p>",
        "new": "",
        "paths": [ROOT / "output" / "final_reader" / "连云港市志_全书.html"],
    },
    {
        "label": "reader_education_table_page_2200",
        "old": "<p>2200·</p>",
        "new": "",
        "paths": [ROOT / "output" / "final_reader" / "连云港市志_全书.html"],
    },
    {
        "label": "reader_education_table_header_2201",
        "old": "<p>初等教育·2201</p>",
        "new": "",
        "paths": [ROOT / "output" / "final_reader" / "连云港市志_全书.html"],
    },
    {
        "label": "reader_appendix_country_writings_header",
        "old": "<p>二、乡土文存·2721 ·十五、石桥流水山东村胶环大涧，上有石桥，千章古木，两岸清阴，流水瀑缓，最为澄澈。诗日：</p>",
        "new": "<p>十五、石桥流水山东村胶环大涧，上有石桥，千章古木，两岸清阴，流水瀑缓，最为澄澈。诗日：</p>",
        "paths": [ROOT / "output" / "final_reader" / "连云港市志_全书.html"],
    },
    {
        "label": "source_education_table_page_2200",
        "old": "\n2200·\n\n续上表",
        "new": "\n续上表",
        "paths": [
            ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
            ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
        ],
    },
    {
        "label": "source_education_table_header_2201",
        "old": "\n第三章\n初等教育·2201\n续上表",
        "new": "\n续上表",
        "paths": [
            ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
            ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
        ],
    },
    {
        "label": "source_appendix_country_writings_header",
        "old": "\n二、乡土文存·2721 ·\n十五、石桥流水",
        "new": "\n十五、石桥流水",
        "paths": [
            ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
            ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md",
        ],
    },
]

REPORT_JSON = ROOT / "output" / "reports" / "final_reader_page_garbles_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "final_reader_page_garbles_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_最终阅读器页码残留清理.md"


def replace_once(text: str, old: str, new: str) -> tuple[str, int]:
    count = text.count(old)
    if count:
        text = text.replace(old, new, 1)
    return text, count


def main() -> None:
    changes = []
    for item in REPLACEMENTS:
        for path in item["paths"]:
            text = path.read_text(encoding="utf-8")
            updated, count = replace_once(text, item["old"], item["new"])
            applied = count > 0
            if applied:
                path.write_text(updated, encoding="utf-8", newline="\n")
            changes.append({
                "label": item["label"],
                "path": str(path.relative_to(ROOT)),
                "matched": count,
                "applied": applied,
            })

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"generated_at": now, "changes": changes}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 最终阅读器页码残留清理",
        "",
        f"- 时间：{now}",
        "- 范围：当前最终阅读器、对应正文汇总和下册分段源稿中的高置信页码/页眉残留。",
        "- 说明：仅处理已定位的精确残留，不做全局页码规则替换。",
        "",
        "## 改写清单",
        "",
        "| 项 | 文件 | 命中 | 已改 |",
        "|---|---|---:|---|",
    ]
    for c in changes:
        lines.append(f"| {c['label']} | `{c['path']}` | {c['matched']} | {'是' if c['applied'] else '否'} |")
    lines.extend([
        "",
        "## 证据",
        "",
        "- `· 458·` 为第八卷价格管理段落后的独立页码段落。",
        "- `:2198·`、`2200·`、`初等教育·2201` 位于第五十卷初等教育表格续页之间，前文已存在规范章标题。",
        "- `二、乡土文存·2721 ·` 位于附录乡土文存页眉，前文已存在规范 `二、乡土文存` 标题。",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    PROGRESS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
