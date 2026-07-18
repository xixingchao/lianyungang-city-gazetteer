from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "workbench" / "body_chapters" / "连云港市志_上册_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "连云港市志_全书_正文汇总.md",
    ROOT / "workbench" / "body_chapters" / "第十七卷至第二十九卷（中part01）.md",
    ROOT / "workbench" / "body_chapters" / "第三十卷至第四十二卷（中part02）.md",
    ROOT / "workbench" / "body_chapters" / "第四十三卷至第五十一卷（下part01）.md",
]
PATTERN = re.compile(r"^[:：]?\d{3,4}·$|^·\s*\d{3,4}\s*·$")
REPORT_JSON = ROOT / "output" / "reports" / "body_source_standalone_page_numbers_20260709.json"
REPORT_MD = ROOT / "output" / "reports" / "body_source_standalone_page_numbers_20260709.md"
PROGRESS_MD = ROOT / "output" / "reports" / "progress" / "20260709_正文源稿独立页码行清理.md"


def main() -> None:
    removed = []
    for path in PATHS:
        lines = path.read_text(encoding="utf-8").splitlines()
        out = []
        for idx, line in enumerate(lines, start=1):
            if PATTERN.fullmatch(line.strip()):
                prev_line = lines[idx - 2].strip() if idx >= 2 else ""
                next_line = lines[idx].strip() if idx < len(lines) else ""
                removed.append({
                    "path": str(path.relative_to(ROOT)),
                    "line": idx,
                    "text": line,
                    "prev": prev_line,
                    "next": next_line,
                })
                continue
            out.append(line)
        path.write_text("\n".join(out) + "\n", encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"generated_at": now, "removed_count": len(removed), "removed": removed}
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# 正文源稿独立页码行清理",
        "",
        f"- 时间：{now}",
        "- 范围：现行正文源稿与上册/全书正文汇总，不处理 OCR 原始文件、PaddleOCR 历史汇总、backup、obsolete。",
        "- 规则：仅删除整行匹配 `256·`、`:2198·`、`· 1326 ·` 这类独立页码行；不处理行内数字。",
        f"- 删除：{len(removed)} 行。",
        "",
        "## 删除明细",
        "",
        "| 文件 | 原行号 | 原文 | 上文 | 下文 |",
        "|---|---:|---|---|---|",
    ]
    for r in removed:
        md.append(f"| `{r['path']}` | {r['line']} | `{r['text']}` | `{r['prev'][:40]}` | `{r['next'][:40]}` |")
    REPORT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    PROGRESS_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"removed={len(removed)} report={REPORT_MD}")


if __name__ == "__main__":
    main()
