import cv2
import easyocr
from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import glob
import os

# Roboflow API 클라이언트 설정
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="6NhFdZxAlGVuIMPTmExy"
)

# 이미지 로드
image_dir = "4th_task"
image_files = glob.glob(os.path.join(image_dir, "uploaded.*"))
image = cv2.imread(image_files[0])
h, w, _ = image.shape

# 객체 탐지
custom_config = InferenceConfiguration(confidence_threshold=0.3)

# 설정을 적용하여 추론 실행
with CLIENT.use_configuration(custom_config):
    result = CLIENT.infer(image, model_id="bookshelf-digitizer/1")

# OCR 준비
reader = easyocr.Reader(['ko', 'en'])
annotated_image = image.copy()

# OCR 결과 저장용
ocr_results = []

# 각 박스 반복
for i, pred in enumerate(result['predictions']):
    x, y, box_w, box_h = int(pred["x"]), int(pred["y"]), int(pred["width"]), int(pred["height"])
    x1, y1 = max(0, x - box_w // 2), max(0, y - box_h // 2)
    x2, y2 = min(w, x + box_w // 2), min(h, y + box_h // 2)
    cropped = image[y1:y2, x1:x2]

    # OCR: 정방향
    texts_normal = [text for _, text, conf in reader.readtext(cropped) if conf > 0.3]

    # OCR: 90도 회전
    rotated = cv2.rotate(cropped, cv2.ROTATE_90_COUNTERCLOCKWISE)
    texts_rotated = [text for _, text, conf in reader.readtext(rotated) if conf > 0.3]

    # OCR 결과 저장
    ocr_results.append({
        "box_index": i,
        "texts_normal": texts_normal,
        "texts_rotated": texts_rotated
    })

    # 박스 + 번호 라벨 시각화
    label = f"Box {i}"
    cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 5)
    cv2.putText(annotated_image, label, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5)

# 이미지 저장
save_path = "4th_task/upload_labeled.jpg"
cv2.imwrite(save_path, annotated_image)
print(f"[✓] 박스 번호 시각화 저장됨: {save_path}")

#OCR 결과 저장
save_path = "4th_task/ocr_results.txt"
with open(save_path, "w", encoding="utf-8") as f:
    f.write("[📚 OCR 결과]\n")
    for res in ocr_results:
        f.write(f"\n🟩 Box {res['box_index']}\n")
        f.write(" - 정방향 OCR: " + ", ".join(res['texts_normal']) + "\n")
        f.write(" - 90도 회전 OCR: " + ", ".join(res['texts_rotated']) + "\n")

print(f"[✓] OCR 결과 저장 완료: {save_path}")
