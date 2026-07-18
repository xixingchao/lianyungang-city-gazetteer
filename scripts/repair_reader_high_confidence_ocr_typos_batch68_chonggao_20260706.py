from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第六十八批_崇高献身精神.md"

OLD = "凝聚了一批具有票高献身精神的专家、学者和修志专业人员的无私奉献"
NEW = "凝聚了一批具有崇高献身精神的专家、学者和修志专业人员的无私奉献"
EVIDENCE = "局部放大 OCR `workbench/ocr/tesseract_check/book_end_20260706/crops/page_0476_quote_band_a_4x.txt` 读作 `凝聚了一批具有崇/高献身精神`；raw 行断作 `具有票` + `高献身精神`。"


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise SystemExit(f"expected exactly 1 hit, got {count}")
    HTML.write_text(text.replace(OLD, NEW), encoding="utf-8")
    REPORT.write_text(
        "\n".join([
            "# 高置信 OCR 错字补修第六十八批：崇高献身精神",
            "",
            f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 修复项",
            "",
            f"- `{OLD}` -> `{NEW}`（命中 1 处）",
            f"  - 证据：{EVIDENCE}",
            "",
            "## 边界",
            "",
            "- 只修主阅读版，不改 OCR 原文。",
            "- `用破万人心` 局部 OCR 仍读作原样，缺少稳定替代文本，本批不猜改。",
            "- 未展示、未嵌入页图。",
            "",
        ]),
        encoding="utf-8",
    )
    print("changed=1")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
