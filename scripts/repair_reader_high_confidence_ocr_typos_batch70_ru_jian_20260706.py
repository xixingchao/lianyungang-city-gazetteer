from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第七十批_注入混入汉奸.md"

REPLACEMENTS = [
    (
        "0.2%利凡诺胎膜外注人引产法",
        "0.2%利凡诺胎膜外注入引产法",
        "`workbench/ocr/paddle_ocr/下/part01/page_0450.txt` 同句作 `0.2%利凡诺胎膜外注入引产法`；raw 为 `注人`。",
    ),
    (
        "与混人革命根据地的汉好特务进行斗争",
        "与混入革命根据地的汉奸特务进行斗争",
        "`workbench/ocr/paddle_ocr/下/part01/page_0065.txt` 同句作 `与混入革命根据地的汉奸/特务进行斗争`；raw 为 `混人...汉好`。",
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
        "# 高置信 OCR 错字补修第七十批：注入、混入、汉奸",
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
        "- `并人徐州第四监狱`、`避选`、`上尽，然长逝`、`用破万人心` 仍缺稳定证据，本批不猜改。",
        "- 未展示、未嵌入页图。",
        "",
    ])
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={len(changed)}")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
