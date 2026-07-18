from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第七十一批_焦献猷嚣张朐山.md"

REPLACEMENTS = [
    (
        "焦献献（？～？）学元臣，清陕西榆阳人，由岁贡生入仕，海州知州。在任期间曾出俸禄，为地方开设义学，教授生徒。清雍正元年（1723年），海州大早，焦献献上书息求免除税收，放赈救济灾民。",
        "焦献猷（？～？）字元臣，清陕西榆阳人，由岁贡生入仕，海州知州。在任期间曾捐出俸禄，为地方开设义学，教授生徒。清雍正元年（1723年），海州大旱，焦献猷上书恳求免除税收，放赈救济灾民。",
        "`workbench/ocr/paddle_ocr/下/part02/page_0383.txt` 同段作 `焦献猷`、`字元臣`、`捐出俸禄`、`海州大旱`、`上书恳求`。",
    ),
    (
        "焦献献查知后，严加法办",
        "焦献猷查知后，严加法办",
        "同页 Paddle 后文作 `焦献猷查知后`，保持人物名一致。",
    ),
    (
        "匪特活动器张，在羽东、羽西、牛山、新民等区发现9股土匪",
        "匪特活动嚣张，在羽东、羽西、牛山、新民等区发现9股土匪",
        "`workbench/ocr/paddle_ocr/下/part01/page_0065.txt` 同句作 `匪特活动嚣张`。",
    ),
    (
        "经济犯罪分子的器张气焰压下去",
        "经济犯罪分子的嚣张气焰压下去",
        "`workbench/ocr/paddle_ocr/下/part01/page_0108.txt` 同句作 `经济犯罪分子的嚣张气焰压下去`。",
    ),
    (
        "购买张文苗房舍，建胸山书院",
        "购买张文茁房舍，建朐山书院",
        "`workbench/ocr/paddle_ocr/下/part01/page_0349.txt` 同句作 `购买张文茁房舍，建朐山书院`；同页标题为 `朐山书院`。",
    ),
]


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    changed = []
    for old, new, evidence in REPLACEMENTS:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"expected exactly 1 hit for {old!r}, got {count}")
        text = text.replace(old, new)
        changed.append((old, new, evidence))
    HTML.write_text(text, encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第七十一批：焦献猷、嚣张、朐山",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for old, new, evidence in changed:
        lines.append(f"- `{old}` -> `{new}`（命中 1 处）")
        lines.append(f"  - 证据：{evidence}")
    lines.extend([
        "",
        "## 边界",
        "",
        "- 只修主阅读版，不改 OCR 原文。",
        "- `劳动力管理同题` 目标字跨页未闭合，本批不猜改。",
        "- `胸山（今海州锦屏山）` 属《汉书》地名语境，未纳入本批。",
        "- 未展示、未嵌入页图。",
        "",
    ])
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={len(changed)}")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
