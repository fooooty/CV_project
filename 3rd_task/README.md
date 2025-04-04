# 📌 Commento 3차 업무: YOLOv8 기반 객체 탐지 모델 학습 및 분석

---

## ✅ 과제 목표

- Hugging Face Dataset(CPPE-5)을 이용한 객체 탐지 실습
- YOLOv8 모델 학습 및 성능 분석
- 학습 로그 시각화 및 테스트 이미지 예측 결과 시각화

---

## ✅ 사용 데이터 및 도구

- **데이터셋**: [`rishitdagli/cppe-5`](https://huggingface.co/datasets/rishitdagli/cppe-5)
- **프레임워크**: Ultralytics YOLOv8
- **라이브러리**: OpenCV, Pandas, Matplotlib

---

## ✅ 주요 기능 요약

### 1. 모델 학습 및 데이터 전처리 (`train_yolo.py`)
- Hugging Face에서 CPPE-5 데이터셋 로드
- `train/val/test`로 데이터 분할
- YOLO 학습 형식으로 이미지 및 라벨 저장
- `yolov8n.pt` 기반 YOLOv8 모델 학습 (20 epoch)
- 결과 저장:
  - `runs/detect/yolo_train/weights/best.pt` (성능 최고 모델)
  - `results.csv` (학습 로그)

### 2. 학습 성능 로그 시각화 (`plot_train_log.py`)
- `results.csv`에서 Precision, Recall, mAP50, mAP50-95 추출
- 그래프 저장: `performance_from_results_csv.png`

### 3. 객체 탐지 예측 및 시각화 (`detect_yolo.py`)
- 학습된 `best.pt`로 테스트 이미지(`1001.jpg`) 예측
- 객체 탐지 결과를 시각화하여 저장
- 결과 이미지: `detected_result.jpg`

---

## 📂 저장 결과 구조 예시

```plaintext
3rd_task/
├── datasets/
│   ├── images/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── labels/
│       ├── train/
│       ├── val/
│       └── test/
├── yolov8n.pt                         # 사전 학습 모델
├── data.yaml                          # YOLO 데이터셋 정보
├── train_yolo.py                      # 학습 스크립트
├── plot_train_log.py                  # 성능 시각화 스크립트
├── detect_yolo.py                     # 객체 탐지 스크립트
├── performance_from_results_csv.png  # Precision, Recall 등 그래프
├── detected_result.jpg                # 탐지 결과 시각화
