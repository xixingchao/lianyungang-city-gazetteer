# -*- coding: utf-8 -*-
"""Sync cleaned Volume 59 source block into the full body summary."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLEAN_SOURCE = ROOT / "workbench" / "body_chapters" / "第五十二卷至第六十卷及附录（下part02）.md"
FULL_SUMMARY = ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md"
REPORT_MD = ROOT / "output" / "reports" / "volume59_full_summary_sync_20260709.md"
REPORT_JSON = ROOT / "output" / "reports" / "volume59_full_summary_sync_20260709.json"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260709_第五十九卷方言全书正文汇总同步.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"


def line_no(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def extract_clean_volume(text: str) -> tuple[str, int, int]:
    start = text.index("第五十九卷 方言")
    end = text.index("第六十卷 人物", start)
    return text[start:end].strip() + "\n\n", start, end


def find_full_volume(text: str) -> tuple[int, int]:
    needle = "<!-- page-anchor: LYG-2727 -->"
    anchor = text.index(needle)
    start = text.index("第五十九卷", anchor)
    end = text.index("第六十卷", start)
    return start, end


def main() -> None:
    clean_text = CLEAN_SOURCE.read_text(encoding="utf-8")
    full_text = FULL_SUMMARY.read_text(encoding="utf-8")
    clean_block, clean_start, clean_end = extract_clean_volume(clean_text)
    full_start, full_end = find_full_volume(full_text)
    old_block = full_text[full_start:full_end]
    changed = old_block != clean_block
    if changed:
        FULL_SUMMARY.write_text(full_text[:full_start] + clean_block + full_text[full_end:], encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = {
        "time": now,
        "changed": changed,
        "clean_source": str(CLEAN_SOURCE.relative_to(ROOT)),
        "full_summary": str(FULL_SUMMARY.relative_to(ROOT)),
        "clean_lines": [line_no(clean_text, clean_start), line_no(clean_text, clean_end)],
        "full_old_lines": [line_no(full_text, full_start), line_no(full_text, full_end)],
        "old_chars": len(old_block),
        "new_chars": len(clean_block),
        "old_noise_samples": {
            "broken_title": "概·述" in old_block or "第五十九卷\n概·述" in old_block,
            "square_noise_prefix": "833838338" in old_block,
            "dirty_homophone_anchor": "<!-- page-anchor: LYG-2735 -->" in old_block,
        },
        "new_markers": {
            "volume_title": "第五十九卷 方言" in clean_block,
            "chapter3": "第三章同音字汇" in clean_block,
            "chapter4": "第四章方言词汇" in clean_block,
            "chapter5": "第五章语法特点" in clean_block,
        },
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""# 第五十九卷方言全书正文汇总同步

- 时间：{now}
- 范围：`第五十九卷 方言`
- 源：`{result['clean_source']}`
- 目标：`{result['full_summary']}`

## 动作

- 用当前下册 part02 中已清理的第五十九卷方言块，替换全书正文汇总中的旧 OCR 形态方言卷块。
- 不改 OCR 原始文件，不改最终阅读器正文，不猜改音标和词条。
- 目的是让后续“正文汇总”与已清理底稿一致，避免继续从旧脏块派生问题。

## 证据

- 清理源范围行：{result['clean_lines'][0]}-{result['clean_lines'][1]}。
- 全书汇总旧块范围行：{result['full_old_lines'][0]}-{result['full_old_lines'][1]}。
- 旧块字符数：{result['old_chars']}。
- 新块字符数：{result['new_chars']}。
- 旧块噪声：卷题断裂/概述中点={result['old_noise_samples']['broken_title']}；数字噪声前缀={result['old_noise_samples']['square_noise_prefix']}；旧页锚同音字汇={result['old_noise_samples']['dirty_homophone_anchor']}。
- 新块标志：卷题={result['new_markers']['volume_title']}；第三章={result['new_markers']['chapter3']}；第四章={result['new_markers']['chapter4']}；第五章={result['new_markers']['chapter5']}。

## 结果

- 发生改写：{changed}
"""
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")

    marker = "## 2026-07-09 第五十九卷方言全书正文汇总同步"
    memory = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    if marker not in memory:
        entry = f"""
{marker}

- 用 `workbench/body_chapters/第五十二卷至第六十卷及附录（下part02）.md` 中已清理的第五十九卷方言块，同步替换 `workbench/body_chapters/连云港市志_全书_正文汇总.md` 中旧 OCR 形态方言卷块。
- 旧块存在 `概·述`、数字噪声前缀和旧页锚同音字汇等问题；本批只同步工作底稿汇总，不改 OCR 原始文件，不改阅读器正文。
- 报告：`output/reports/volume59_full_summary_sync_20260709.md`；进度：`output/reports/progress/20260709_第五十九卷方言全书正文汇总同步.md`。
"""
        MEMORY.write_text(memory.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")

    print("volume59 full summary synced")
    print(f"changed={int(changed)}")
    print(f"old_chars={result['old_chars']}")
    print(f"new_chars={result['new_chars']}")
    print(f"report={REPORT_MD}")


if __name__ == "__main__":
    main()
