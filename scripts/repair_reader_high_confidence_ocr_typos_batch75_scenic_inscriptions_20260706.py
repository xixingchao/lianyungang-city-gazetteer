from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第七十五批_风景石刻短片段.md"

REPLACEMENTS = [
    (
        "还有谭亨甫刻的一首右曼卿飞泉诗，意境古朴，书法精妙。诗日：“上狮子石，下有灌缨泉。",
        "还有谭亨甫刻的一首石曼卿飞泉诗，意境古朴，书法精妙。诗曰：“上蹲狮子石，下有濯缨泉。",
    ),
    ("久坐捐尘埃，冠弃斯冷然。", "久坐捐尘埃，冠弁斯泠然。"),
    ("山上旧有鸡鸣寺，今已妃，但鸡鸣石尚在", "山上旧有鸡鸣寺，今已圮，但鸡鸣石尚在"),
    ("上刻有古愚子的一首诗，诗日：“山不高兮", "上刻有古愚子的一首诗，诗曰：“山不高兮"),
    (
        "诗日：“龙洞良霄月照，黄花满地秋香。此时此会文彦，筋一咏情长，鑫矗山岩曲抱，瀑瀑胸海东流。",
        "诗曰：“龙洞良霄月照，黄花满地秋香。此时此会文彦，一觞一咏情长，矗矗山岩曲抱，潺潺朐海东流。",
    ),
]


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    changed = []
    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"expected exactly 1 hit for {old!r}, got {count}")
        text = text.replace(old, new)
        changed.append((old, new))
    HTML.write_text(text, encoding="utf-8")

    lines = [
        "# 高置信 OCR 错字补修第七十五批：风景石刻短片段",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for old, new in changed:
        lines.append(f"- `{old}` -> `{new}`")
    lines.extend([
        "",
        "## 证据与边界",
        "",
        "- 飞泉、鸡鸣山段依据 `workbench/ocr/paddle_ocr/中/part02/page_0097.txt`：同页 PaddleOCR 作 `石曼卿飞泉诗`、`诗曰`、`上蹲狮子石`、`濯缨泉`、`冠弁斯泠然`、`今已圮`。",
        "- 龙洞石刻段依据 `workbench/ocr/paddle_ocr/中/part02/page_0113.txt`：同页 PaddleOCR 作 `诗曰`、`一觞一咏情长`、`矗矗山岩曲抱`、`潺潺朐海东流`。",
        "- raw OCR/旧 reader 对应作 `右曼卿/诗日/上狮子/灌缨泉/冠弃斯冷然/今已妃/筋一咏/鑫矗/瀑瀑胸海`，判定为 OCR 形近或残片误识。",
        "- 本批仅处理上述同页 PaddleOCR 证据闭合片段；顾乾《云台山三十六景》旧志页大量 `诗日`、古文序文 `编繁`、书末 `避选` 与 `上尽，然长逝` 仍不猜改。未展示、未嵌入页图。",
        "",
    ])
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={len(changed)}")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
