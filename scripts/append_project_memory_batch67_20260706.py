from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"

NOTE = """
## 2026-07-06 高置信 OCR 错字补修第六十七批：书末编纂术语
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch67_book_end_bianzuan_20260706.py`，修复主阅读版书末现代修志语境 4 个唯一命中的短片段。
- 主要修复：`市志编繁委员会/省志编繁委员` -> `市志编纂委员会/省志编纂委员`，`连云港市地方志编繁委员会` -> `连云港市地方志编纂委员会`，`市志编委员会` -> `市志编纂委员会`，`为《连云港市志》编繁、评审、校核、出版` -> `为《连云港市志》编纂、评审、校核、出版`。
- 证据边界：依据书末同段及全书现代机构名“地方志编纂委员会/市志编纂委员会/省地方志编纂委员会”统一；人物传和旧志序文中的 `编繁` 暂不处理，需另行核古籍语境。报告：`output/reports/progress/20260706_高置信OCR错字补修第六十七批_书末编纂术语.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第六十七批：书末编纂术语"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
