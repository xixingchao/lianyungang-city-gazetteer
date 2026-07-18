from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"
NOTE = """
## 2026-07-06 高置信 OCR 错字补修第六十八批：崇高献身精神
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch68_chonggao_20260706.py`，修复主阅读版书末《后记》1 处 `票高献身精神` -> `崇高献身精神`。
- 证据：`workbench/ocr/tesseract_check/book_end_20260706/crops/page_0476_quote_band_a_4x.txt` 局部放大 OCR 读出 `具有崇/高献身精神`；raw 原文断行为 `具有票` + `高献身精神`，判定为 OCR 形近误识。
- 边界：`用破万人心` 局部 OCR 仍读作原样，暂不猜改。报告：`output/reports/progress/20260706_高置信OCR错字补修第六十八批_崇高献身精神.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第六十八批：崇高献身精神"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
