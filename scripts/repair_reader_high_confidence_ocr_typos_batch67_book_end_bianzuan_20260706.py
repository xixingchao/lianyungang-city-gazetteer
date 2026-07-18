from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT = ROOT / "output" / "reports" / "progress" / "20260706_高置信OCR错字补修第六十七批_书末编纂术语.md"

REPLACEMENTS = [
    (
        "市志编繁委员会的集体筹划、省志编繁委员及市内外专家",
        "市志编纂委员会的集体筹划、省志编纂委员及市内外专家",
        "书末《后记》同页机构/工作语境均作编纂；正文已有多处“市志编纂委员会”。",
    ),
    (
        "连云港市地方志编繁委员会，办公室设在市委党史工委",
        "连云港市地方志编纂委员会，办公室设在市委党史工委",
        "前文大事记及档案卷均作“地方志编纂委员会”，同段后文也作“市志编纂委员会”。",
    ),
    (
        "市政府再次调整市志编委员会。1995年12月12~14日",
        "市政府再次调整市志编纂委员会。1995年12月12~14日",
        "下册书末 page_0478 raw 为“市志编委员会”，同段后文“第四次调整市志编纂委员会”补足漏字。",
    ),
    (
        "为《连云港市志》编繁、评审、校核、出版付出辛勤劳动",
        "为《连云港市志》编纂、评审、校核、出版付出辛勤劳动",
        "书末致谢语为现代修志术语，前后均用“编纂/总纂/分纂”。",
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
        "# 高置信 OCR 错字补修第六十七批：书末编纂术语",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 修复项",
        "",
    ]
    for old, new, evidence in changed:
        lines.extend([
            f"- `{old}` -> `{new}`（命中 1 处）",
            f"  - 证据：{evidence}",
        ])
    lines.extend([
        "",
        "## 边界",
        "",
        "- 只修主阅读版书末现代修志语境，不改 OCR 原文。",
        "- 人物传和旧志序文中的 `编繁` 未纳入本批，因需古籍语境继续核对。",
        "- 未展示、未嵌入页图。",
        "",
    ])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"changed={len(changed)}")
    print(f"progress={REPORT}")


if __name__ == "__main__":
    main()
