from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"
NOTE = """
## 2026-07-06 高置信 OCR 错字补修第七十一批：焦献猷、嚣张、朐山
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch71_paddle_backed_20260706.py`，据 Paddle 同页证据修复主阅读版 5 个精确短片段。
- 主要修复：焦献猷人物小传开头 `焦献献/学元臣/出俸禄/大早/息求` -> `焦献猷/字元臣/捐出俸禄/大旱/恳求`，并同步后文 `焦献猷查知后`；两处 `器张` -> `嚣张`；`购买张文苗房舍，建胸山书院` -> `购买张文茁房舍，建朐山书院`。
- 证据：`workbench/ocr/paddle_ocr/下/part02/page_0383.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0065.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0108.txt`、`workbench/ocr/paddle_ocr/下/part01/page_0349.txt`。
- 边界：`劳动力管理同题` 目标字跨页未闭合，未改；`胸山（今海州锦屏山）` 属《汉书》地名语境，未改。报告：`output/reports/progress/20260706_高置信OCR错字补修第七十一批_焦献猷嚣张朐山.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第七十一批：焦献猷、嚣张、朐山"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
