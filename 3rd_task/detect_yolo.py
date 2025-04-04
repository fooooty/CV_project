from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os

# 저장 경로 지정
save_dir = "3rd_task"
os.makedirs(save_dir, exist_ok=True)

# 1. 학습된 모델 로드
model = YOLO("/opt/homebrew/runs/detect/yolo_train/weights/best.pt")

# 2. 예측할 이미지 경로
image_path = '3rd_task/datasets/images/test/1027.jpg'
image = cv2.imread(image_path)

# 3. 객체 탐지 수행
results = model(image)

# 4. 시각화 - 박스 그리기
for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        label = f"{model.names[cls]} {conf:.2f}"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 5. 결과 이미지 저장
result_img_path = os.path.join(save_dir, "detected_result.jpg")
cv2.imwrite(result_img_path, image)
print(f"[✓] 결과 이미지 저장됨: {result_img_path}")