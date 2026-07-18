"""对比 RapidOCR vs PaddleOCR 对第50页的识别质量"""
import json, sys, time, numpy as np
from pathlib import Path

# Force UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

ROOT = Path(r"e:\codex_Learing\09_project_东辛农场\连云港市志_workstation")
IMAGE_PATH = ROOT / "workbench/conversion/page_images/上/part01/page_0050_180dpi.jpg"
RAPID_JSON = ROOT / "workbench/ocr/raw/上/part01/page_0050.json"

# ── RapidOCR ──
rapid_data = json.loads(RAPID_JSON.read_text(encoding="utf-8"))
rapid_lines = [line["text"] for line in rapid_data["lines"]]
rapid_text = "\n".join(rapid_lines)
rapid_conf = rapid_data["avg_confidence"]
rapid_time = rapid_data["time_s"]

# ── PaddleOCR ──
from paddleocr import PaddleOCR
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)
t0 = time.time()
result = ocr.predict(str(IMAGE_PATH))
paddle_time = time.time() - t0

res = result[0]
paddle_texts = res["rec_texts"]
paddle_scores = res["rec_scores"]
paddle_text = "\n".join(paddle_texts)
paddle_conf = float(np.mean(paddle_scores))

print("=" * 80)
print("[RapidOCR]")
print(f"  avg_conf={rapid_conf:.4f}, time={rapid_time:.1f}s, lines={len(rapid_lines)}, chars={len(rapid_text)}")
print(rapid_text)
print()
print("=" * 80)
print("[PaddleOCR PP-OCRv6]")
print(f"  avg_conf={paddle_conf:.4f}, time={paddle_time:.1f}s, lines={len(paddle_texts)}, chars={len(paddle_text)}")
print(paddle_text)
print()

# ── 关键错误检查 ──
print("=" * 80)
print("[Key Error Comparison]")
checks = [
    ("糟运→漕运", "糟运", "漕运"),
    ("收人→收入", "收人", "收入"),
    ("述阳→沭阳", "述阳", "沭阳"),
    ("倭寇蔻→倭寇", "寇蔻", "寇"),
    ("窜人→窜入", "窜人", "窜入"),
    ("昊继勋→吴继勋", "昊继勋", "吴继勋"),
    ("尽夜→昼夜", "尽夜", "昼夜"),
    ("胥更→胥吏", "胥更", "胥吏"),
    ("同治→同知", "同治", "同知"),
    ("圆林寺→园林寺", "圆林寺", "园林寺"),
    ("新瞳→新壩", "新瞳", "新壩"),
]
fixed = 0
still_bad = 0
for desc, wrong, correct in checks:
    r_has = wrong in rapid_text
    p_has = wrong in paddle_text
    p_correct = correct in paddle_text
    if r_has and not p_has:
        print(f"  [FIXED] {desc}")
        fixed += 1
    elif r_has and p_has:
        print(f"  [STILL BAD] {desc}")
        still_bad += 1
    elif not r_has:
        print(f"  [Rapid was OK] {desc}")

print(f"\n  Fixed: {fixed}, Still bad: {still_bad}")

# ── 逐行差异 ──
print()
print("=" * 80)
print("[Line-by-line Diffs]")
max_lines = max(len(rapid_lines), len(paddle_texts))
diffs = 0
for i in range(max_lines):
    r = rapid_lines[i] if i < len(rapid_lines) else "(missing)"
    p = paddle_texts[i] if i < len(paddle_texts) else "(missing)"
    if r != p:
        diffs += 1
        if diffs <= 15:
            print(f"  L{i}: R=[{r}] P=[{p}]")
print(f"\n  Total diffs: {diffs}/{max_lines}")
