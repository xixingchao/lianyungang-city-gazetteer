"""Merge PaddleOCR per-page .txt files into a single volume markdown."""
from pathlib import Path

ROOT = Path(r"e:\codex_Learing\09_project_东辛农场\连云港市志_workstation")
PADDLE_DIR = ROOT / "workbench/ocr/paddle_ocr"
MERGED_DIR = ROOT / "workbench/ocr/paddle_ocr/merged"
MERGED_DIR.mkdir(parents=True, exist_ok=True)

UPPER_PARTS = [
    ("上", "part01", 300),
    ("上", "part02", 305),
    ("上", "part03", 298),
]

# ── 分册合并 ──
for volume, part, total in UPPER_PARTS:
    raw_dir = PADDLE_DIR / volume / part
    merged_path = MERGED_DIR / f"连云港市志_{volume}_{part}_PaddleOCR汇总.md"
    chunks = [f"# 连云港市志_{volume}_{part} PaddleOCR汇总\n"]
    for page_num in range(1, total + 1):
        txt_path = raw_dir / f"page_{page_num:04d}.txt"
        if not txt_path.exists():
            print(f"  [MISSING] {txt_path}")
            continue
        text = txt_path.read_text(encoding="utf-8")
        parts = text.split("\n\n", 1)
        body = parts[1].strip() if len(parts) == 2 else text.strip()
        chunks.append(f"\n\n## 第 {page_num} 页\n\n")
        chunks.append(body)
    merged_path.write_text("".join(chunks).rstrip() + "\n", encoding="utf-8")
    print(f"[MERGED] {volume}/{part}: {merged_path} ({len(chunks)} pages)")

# ── 上册总合并 ──
total_merged = MERGED_DIR / "连云港市志_上册_PaddleOCR汇总.md"
all_chunks = ["# 连云港市志 上册 PaddleOCR汇总\n"]
global_page = 0
for volume, part, total in UPPER_PARTS:
    raw_dir = PADDLE_DIR / volume / part
    for page_num in range(1, total + 1):
        global_page += 1
        txt_path = raw_dir / f"page_{page_num:04d}.txt"
        if not txt_path.exists():
            continue
        text = txt_path.read_text(encoding="utf-8")
        parts = text.split("\n\n", 1)
        body = parts[1].strip() if len(parts) == 2 else text.strip()
        all_chunks.append(f"\n\n## 第 {global_page} 页\n\n")
        all_chunks.append(body)
total_merged.write_text("".join(all_chunks).rstrip() + "\n", encoding="utf-8")
print(f"\n[TOTAL MERGED] {total_merged} ({global_page} pages)")
