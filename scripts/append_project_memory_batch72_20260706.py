from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "PROJECT_MEMORY.md"
NOTE = """
## 2026-07-06 高置信 OCR 错字补修第七十二批：劳动力管理问题
- 新增并运行 `scripts/repair_reader_high_confidence_ocr_typos_batch72_labor_problem_20260706.py`，修复主阅读版 1 个唯一命中的公文标题短片段：`加强劳动力管理同题的指示` -> `加强劳动力管理问题的指示`。
- 证据：`workbench/ocr/paddle_ocr/下/part01/page_0245.txt` 与 `workbench/ocr/raw/下/part01/page_0245.txt` 上一行均为 `关于控制各企、事业单位的人员增长和加强劳动力管理`；同段为国务院文件标题语境，正文汇总下一行残留 `同题的指示`，判定为 `问题` 形近 OCR 残留。
- 边界：`劳改队撤销，并人徐州第四监狱` 双源仍作 `并人`，继续不猜改；书末 `避选`、`上尽，然长逝`、`用破万人心` 已记录为硬点，仍未改。报告：`output/reports/progress/20260706_高置信OCR错字补修第七十二批_劳动力管理问题.md`。
""".strip()


def main() -> None:
    text = MEMORY.read_text(encoding="utf-8")
    marker = "## 2026-07-06 高置信 OCR 错字补修第七十二批：劳动力管理问题"
    if marker in text:
        print("already_present=1")
        return
    sep = "" if text.endswith("\n") else "\n"
    MEMORY.write_text(text + sep + "\n" + NOTE + "\n", encoding="utf-8")
    print("appended=1")


if __name__ == "__main__":
    main()
