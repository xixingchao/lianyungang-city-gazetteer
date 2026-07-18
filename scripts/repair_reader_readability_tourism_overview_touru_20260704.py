# -*- coding: utf-8 -*-
"""Repair the tourism overview paragraph around the last 投人 residue."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "output" / "final_reader" / "连云港市志_全书.html"
REPORT_JSON = ROOT / "output" / "reports" / "reader_readability_tourism_overview_touru_20260704.json"
REPORT_MD = ROOT / "output" / "reports" / "reader_readability_tourism_overview_touru_20260704.md"
PROGRESS = ROOT / "output" / "reports" / "progress" / "20260704_名胜旅游概述投人串行回源修复.md"
MEMORY = ROOT / "PROJECT_MEMORY.md"

SOURCE = "workbench/ocr/paddle_ocr/中/part02/page_0095.txt:16-20"
OLD = "连云港市山海形胜，自古以来，吸引了无数达官显贵、文人墨客到此游历。孔子登山观海，秦始皇两度巡游，以及陶渊明、李白、石曼卿、苏东坡、沈括、李清照、辛弃疾、臭敬梓、投人，开发旅游资源，振兴旅游事业，促进经济和社会协调发展，按照国家规划把连云港市建设成为华东地区新兴的工业、外贸、港口、旅游城市。"
NEW = "连云港市山海形胜，自古以来，吸引了无数达官显贵、文人墨客到此游历。孔子登山观海，秦始皇两度巡游，以及陶渊明、李白、石曼卿、苏东坡、沈括、李清照、辛弃疾、吴敬梓、李汝珍、林则徐等幸临市境，留下了许多千古绝唱。20世纪80年代开始，不断加大旅游投入，开发旅游资源，振兴旅游事业，促进经济和社会协调发展，按照国家规划把连云港市建设成为华东地区新兴的工业、外贸、港口、旅游城市。"


def upsert_memory(path: Path, marker: str, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    start = old.index(marker)
    next_start = old.find("\n## ", start + 1)
    if next_start == -1:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n"
    else:
        new = old[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + old[next_start:].lstrip()
    path.write_text(new, encoding="utf-8")


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(f"expected one target paragraph, found {count}")
    text = text.replace(OLD, NEW)
    HTML.write_text(text, encoding="utf-8")
    verify = HTML.read_text(encoding="utf-8")
    if OLD in verify or NEW not in verify:
        raise RuntimeError("tourism overview repair verification failed")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "time": now,
        "scope": "第三十二卷名胜旅游概述复杂串行残文",
        "source": SOURCE,
        "reader_path": str(HTML),
        "current_run_replacements": count,
        "old": OLD,
        "new": NEW,
        "principle": "按页级 PaddleOCR 源文修复整句，不只替换 `投人` 单词。",
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = "\n".join([
        "# 名胜旅游概述投人串行回源修复",
        "",
        f"- 时间：{now}",
        "- 范围：第三十二卷名胜旅游概述",
        f"- 源文：`{SOURCE}`",
        f"- 阅读器：`{HTML}`",
        "- 修复：`臭敬梓、投人，开发旅游资源...` 串行残文。",
        "- 结果：补回 `吴敬梓、李汝珍、林则徐等幸临市境，留下了许多千古绝唱。20世纪80年代开始，不断加大旅游投入...`。",
        "",
    ])
    REPORT_MD.write_text(md, encoding="utf-8")
    PROGRESS.write_text(md, encoding="utf-8")
    memory = f"""
## 2026-07-04 名胜旅游概述投人串行回源修复

- 对第三十二卷名胜旅游概述最后 1 处 `投人` 残留做段落级回源修复。
- 源文依据：`{SOURCE}`。
- 修复 `臭敬梓、投人，开发旅游资源...` 为 `吴敬梓、李汝珍、林则徐等幸临市境，留下了许多千古绝唱。20世纪80年代开始，不断加大旅游投入...`。
- 至此 `投人/收人/纳人` 残留均已清零；`交人/项自/方元` 均为已识别合法跨词或作品名。
- 报告：`output/reports/reader_readability_tourism_overview_touru_20260704.md`。
"""
    upsert_memory(MEMORY, "## 2026-07-04 名胜旅游概述投人串行回源修复", memory)
    print(json.dumps({"current_run_replacements": count, "report": str(REPORT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
