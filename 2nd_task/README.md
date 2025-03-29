
# 📌 Commento 2차 업무: Unit Test + 2D → 3D 변환 실습

---

## ✅ 과제 목표

- Python 기반의 **단위 테스트(Unit Test)** 작성
- OpenCV를 활용한 **2D 이미지 → 3D 포인트 클라우드** 변환 구현
- 기능의 정확성 검증 및 시각화 결과 확인

---

## ✅ 사용 데이터 및 도구

- 테스트용 이미지: `sample.png`
- 사용 라이브러리: `OpenCV`, `NumPy`, `matplotlib`, `pytest`

---

## ✅ 주요 기능 요약

### 1. 기능 구현 (`depth_processing.py`)
- 이미지 로드 (`load_image`)
- Grayscale 변환 후 컬러 Depth Map 생성 (`generate_depth_map`)
- X, Y, Z 좌표로 구성된 3D 포인트 클라우드 생성 (`generate_point_cloud`)
- 결과물 저장: `depth_map.jpg`, `point_cloud.npy`

### 2. 유닛 테스트 (`test_3d_processing.py`)
- `pytest` 기반 유닛 테스트 구성
- 주요 기능에 대한 검증 수행:
  - 출력 모양 확인
  - Z 값 검증
  - X, Y 좌표 정렬 검증
  - 예외 처리 테스트 (`FileNotFoundError`)

### 3. 포인트 클라우드 시각화 (`visualize_point_cloud.py`)
- 저장된 `.npy` 포인트 클라우드를 matplotlib 3D 산점도로 시각화
- Z값을 컬러맵(`cmap='jet'`)으로 색상 표현

---

## 📂 저장 결과 구조 예시

```plaintext
2nd_task/
├── sample.png                     # 입력 이미지
├── depth_processing.py            # 기능 구현 스크립트
├── test_3d_processing.py          # 유닛 테스트 스크립트
├── visualize_point_cloud.py       # 3D 시각화 스크립트
├── result/
│   ├── depth_map.jpg              # 생성된 컬러 depth map
│   └── point_cloud.npy            # 3D 포인트 클라우드 (NumPy 저장)
```

---

## ✅ 테스트 예시 출력

```plaintext
============================= test session starts ==============================
collected 3 items

test_3d_processing.py::test_generate_depth_map PASSED                 [ 33%]
test_3d_processing.py::test_generate_point_cloud PASSED              [ 66%]
test_3d_processing.py::test_load_image_file_not_found PASSED         [100%]

============================== 3 passed in 0.05s ===============================
```
