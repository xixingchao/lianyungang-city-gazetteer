from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第六十九批_四库全书编纂.md"

OLD = "以拔贡生被选送编繁《四库全书》馆充任抄录员"
NEW = "以拔贡生被选送编纂《四库全书》馆充任抄录员"
EVIDENCE = "`workbench/ocr/paddle_ocr/下/part02/page_0383.txt` 同页同句作 `被选送编纂《四库全书》馆充任抄录员`；raw 为 `编繁` 形近残留。"


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise SystemExit(f"expected exactly 1 hit, got {count}")
    HTML.write_text(text.replace(OLD, NEW), encoding="utf-8")
    REPORT.write_text(
        "\n".join([
            "# 高置信 OCR 错字补修第六十九批：四库全书编纂",
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
            "- 同页 Paddle 将姓名读作 `李晋元`，raw 与当前 reader 为 `李普元`；姓名未取得闭合证据，本批不动。",
            "- 旧序文 `网罗编繁成书`、`任编繁者` 局部 OCR 未闭合，本批不猜改。",
            "- 未展示、未嵌入页图。",
            "",
        ]),
        encoding="utf-8",
    )
    print("changed=1")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
