# Commento 1차 업무

---

## 1차 요청: 빨간색 영역 감지 (OpenCV)

### 📍 기능 설명
- OpenCV를 활용해 이미지 내 **빨간색 영역만 감지 및 시각화**하는 예제 코드 작성

📁 관련 코드: `image_processing.py`

---

## 추가 요청: HuggingFace Food101 전처리 및 필터링 

### 📍 사용 데이터셋
- [HuggingFace Datasets: `ethz/food101`](https://huggingface.co/datasets/ethz/food101)
- `train[:50]` 일부 샘플 사용

---

### ✅ 주요 기능 요약

#### 1. 이미지 전처리
- 크기 조정: 224×224
- 색상 변환: Grayscale
- 노이즈 제거: Gaussian Blur (radius = 0.5)

#### 2. 이미지 필터링
- 평균 밝기 < 0.4 제거
- 객체 감지: 가장 큰 덩어리가 이미지 면적의 3% 미만이면 제거  
- → **유효 이미지만 증강 대상**

#### 3. 데이터 증강
- 필터링 통과 이미지에만 적용
- 증강 방법:
  - 좌우 반전 (horizontal flip)
  - 90도 회전
  - ColorJitter: 밝기/대비/채도/색조 변화

> ⚠️ 증강은 **이미지 필터링을 통과한 이미지**에 대해서만 수행됩니다. 

📁 관련 코드: `plus_request.py`

#### 📂 저장 결과 구조 예시
```plaintext
image/preprocessed_samples/
├── 0000/
│   ├── 0000.png                    # 원본 이미지
│   ├── 0000_preprocessed.png       # 전처리 결과 (크기 조정 + Grayscale + Blur)
│   ├── 0000_preprocessed_mask.png  # 객체 마스크 시각화
│   ├── 0000_flip.png               # 증강: 좌우 반전
│   ├── 0000_rotate.png             # 증강: 90도 회전
│   ├── 0000_color.png              # 증강: 색상 변화
│   └── ...
├── 0001/
│   └── ...
