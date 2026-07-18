from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"
NOTE = """
## 2026-07-06 高置信 OCR 错字补修第六十九批：四库全书编纂
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch69_siku_bianzuan_20260706.py`，据 Paddle 同页证据修复主阅读版 1 处 `被选送编繁《四库全书》馆` -> `被选送编纂《四库全书》馆`。
- 证据：`workbench/ocr/paddle_ocr/下/part02/page_0383.txt` 同句为 `被选送编纂《四库全书》馆充任抄录员`；raw 为 `编繁` 形近残留。
- 边界：同页姓名 `李普元/李晋元` 未取得闭合证据，未改；旧序文 `网罗编繁成书`、`任编繁者` 局部 OCR 未闭合，未改。报告：`output/reports/progress/20260706_高置信OCR错字补修第六十九批_四库全书编纂.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第六十九批：四库全书编纂"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
