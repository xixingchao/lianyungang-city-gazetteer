from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOWER_READER = ROOT / "output/final_reader/连云港市志_下册.html"
FULL_READER = ROOT / "output/final_reader/连云港市志_全书.html"
REPORT = ROOT / "output/reports/lower_reader_legal_administration_phrase_20260707.md"
PROGRESS = ROOT / "output/reports/progress/20260707_下册法制工作漏句修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

OLD_HTML = "市、县、区政</p><p>问题，1989年，对全市个体税收专项检查"
NEW_HTML = (
    "市、县、区政府和有关政府部门聘请律师担任常年法律顾问134家。"
    "行政执法部门依法处理各种违法</p><p>问题，1989年，对全市个体税收专项检查"
)
EVIDENCE = "市、县、区政府和有关政府部门聘请律师担任常年法律顾问134家。行政执法部门依法处理各种违法问题，1989年，对全市个体税收专项检查"
BAD_TEXT = "市、县、区政问题，1989年，对全市个体税收专项检查"


def append_memory_once(entry: str) -> bool:
    text = MEMORY.read_text(encoding="utf-8")
    if "下册法制工作漏句修复" in text:
        return False
    MEMORY.write_text(text.rstrip() + "\n\n" + entry.strip() + "\n", encoding="utf-8")
    return True


def main() -> None:
    lower = LOWER_READER.read_text(encoding="utf-8")
    full = FULL_READER.read_text(encoding="utf-8")

    evidence_count = full.count(EVIDENCE)
    old_count = lower.count(OLD_HTML)
    if evidence_count != 1:
        raise SystemExit(f"full-reader evidence count expected 1, got {evidence_count}")
    if old_count != 1:
        raise SystemExit(f"lower-reader old html count expected 1, got {old_count}")

    lower = lower.replace(OLD_HTML, NEW_HTML, 1)
    LOWER_READER.write_text(lower, encoding="utf-8")

    report = f"""# 下册法制工作漏句修复（2026-07-07）

## 修复对象

- `output/final_reader/连云港市志_下册.html`

## 问题

下册当前阅读稿在法制宣传段落中残留断裂句：

```text
{BAD_TEXT}
```

当前全书阅读稿同一位置为完整句：

```text
{EVIDENCE}
```

## 处理

- 仅替换下册 reader 中 1 处跨段残句。
- 用当前全书 reader 的完整句补回缺失内容。
- 未处理其它候选；未打开、展示或嵌入图片。

## 结果

- 修复处数：1
- 生成时间：{datetime.now().isoformat(timespec='seconds')}
"""
    REPORT.write_text(report, encoding="utf-8")

    progress = f"""# 下册法制工作漏句修复

- 日期：2026-07-07
- 对象：`output/final_reader/连云港市志_下册.html`
- 报告：`output/reports/lower_reader_legal_administration_phrase_20260707.md`

## 摘要

复核用户报告后的 reader 残句时，发现下册法制宣传段落中 `市、县、区政问题` 为跨段漏句；当前全书 reader 同位置保留完整句 `市、县、区政府和有关政府部门聘请律师担任常年法律顾问134家。行政执法部门依法处理各种违法问题...`。

已仅在下册 reader 定点补回该完整句，修复 1 处；未打开、展示或嵌入图片。
"""
    PROGRESS.write_text(progress, encoding="utf-8")

    memory_entry = """
## 2026-07-07 下册法制工作漏句修复

- 复核发现当前全书 reader 中法制宣传段落完整，但下册 reader 同位置残留跨段漏句 `市、县、区政问题，1989年...`。
- 已仅在 `output/final_reader/连云港市志_下册.html` 用全书 reader 完整句补回 `市、县、区政府和有关政府部门聘请律师担任常年法律顾问134家。行政执法部门依法处理各种违法问题...`，修复 1 处。
- 报告：`output/reports/lower_reader_legal_administration_phrase_20260707.md`；未打开、展示或嵌入图片。
"""
    memory_written = append_memory_once(memory_entry)

    print(json.dumps({
        "lower_reader": str(LOWER_READER.relative_to(ROOT)),
        "fixes": 1,
        "full_reader_evidence_count": evidence_count,
        "report": str(REPORT.relative_to(ROOT)),
        "progress": str(PROGRESS.relative_to(ROOT)),
        "memory_written": memory_written,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
