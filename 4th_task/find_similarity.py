import pandas as pd
from rapidfuzz import fuzz
import re

ocr_path = "4th_task/ocr_results.txt"
csv_path = "4th_task/book_info.csv"
output_path = "4th_task/similarity_results_top2.txt"

def normalize(text):
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^\w가-힣]", "", text)
    return text.lower()

def load_ocr_results(path):
    box_results = {}
    current_box = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("🟩 Box"):
                current_box = int(re.findall(r"\d+", line)[0])
                box_results[current_box] = []
            elif line.startswith("- 정방향 OCR:") or line.startswith("- 90도 회전 OCR:"):
                raw = line.split(":", 1)[1].strip().strip("[]").replace("'", "")
                texts = [t.strip() for t in raw.split(",") if t.strip()]
                box_results[current_box].extend(texts)
    return box_results

df = pd.read_csv(csv_path, low_memory=False)

title_pairs = []
for _, row in df.iterrows():
    title = str(row["TITLE_NM"]) if pd.notna(row["TITLE_NM"]) else ""
    subtitle = str(row["TITLE_SBST_NM"]) if pd.notna(row["TITLE_SBST_NM"]) else ""
    if title:
        title_pairs.append((title, normalize(title)))
    if subtitle:
        title_pairs.append((title, normalize(subtitle)))

ocr_boxes = load_ocr_results(ocr_path)

with open(output_path, "w", encoding="utf-8") as out:
    for box_idx, texts in ocr_boxes.items():
        out.write(f"\n====================\n🟩 Box {box_idx}\n")
        seen_titles = set()
        for text in texts:
            if len(text.strip()) < 2:
                continue
            norm_text = normalize(text)
            scores = [(original, fuzz.token_sort_ratio(norm_text, norm))
                      for original, norm in title_pairs]
            sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
            count = 0
            for title, score in sorted_scores:
                if title not in seen_titles:
                    out.write(f"  - {title} ({score}점) ← OCR 후보: {text}\n")
                    seen_titles.add(title)
                    count += 1
                    if count == 2:  # ✔️ OCR 후보당 2개
                        break

print(f"[✓] 유사도 기반 도서 추천 결과 (OCR 후보당 2개씩) 저장 완료: {output_path}")
