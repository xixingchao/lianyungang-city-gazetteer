from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"
NOTE = """
## 2026-07-06 高置信 OCR 错字补修第七十批：注入、混入、汉奸
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch70_ru_jian_20260706.py`，据 Paddle 同页证据修复主阅读版 2 个短片段。
- 主要修复：`0.2%利凡诺胎膜外注人引产法` -> `0.2%利凡诺胎膜外注入引产法`；`与混人革命根据地的汉好特务进行斗争` -> `与混入革命根据地的汉奸特务进行斗争`。
- 证据：`workbench/ocr/paddle_ocr/下/part01/page_0450.txt` 作 `注入引产法`；`workbench/ocr/paddle_ocr/下/part01/page_0065.txt` 作 `混入革命根据地的汉奸/特务`。报告：`output/reports/progress/20260706_高置信OCR错字补修第七十批_注入混入汉奸.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第七十批：注入、混入、汉奸"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
