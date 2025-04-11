# 📚 중고책 자동 등록기

책장 이미지를 업로드하면 책 제목을 자동으로 추출하고, 네이버 도서 정보를 검색하여 중고책 판매 리스트를 만들어주는 자동화 도구입니다.  
Streamlit UI를 통해 중고 상태와 희망 판매가를 입력하고 `.csv`로 다운로드할 수 있습니다.

---

## 🚀 실행 방법

```bash
streamlit run 4th_task/app.py
```

---

## 🧭 사용 흐름

1. **책장 사진 업로드**  
   `.jpg` 또는 `.jpeg` 형식의 책장 이미지를 업로드합니다.

2. **OCR → 유사도 분석 → 도서 검색**  
   업로드한 이미지에서 책 제목을 감지하고,  
   사전 수집한 국립중앙도서관 소장 도서 데이터셋과 유사도 비교 후  
   유사도가 높은 도서를 네이버에서 검색해 정보를 가져옵니다.

3. **책 정보 확인 및 입력**  
   제목, 저자, 출판사, 최저 가격 자동 출력  
   중고 상태 선택: 상 / 중 / 하  
   희망 판매 가격 입력

4. **최종 `.csv` 다운로드**  
   등록 완료된 리스트를 CSV로 저장할 수 있습니다.

---

## 📁 폴더 구조

```
4th_task/
├── app.py                      # 📌 Streamlit 메인 앱
├── uploaded.jpg               # 업로드된 책장 이미지
├── detection_and_ocr.py       # 박스 검출 + OCR 
├── upload_labeled.jpg         # 박스 검출 결과 이미지 
├── ocr_results.txt            # OCR 텍스트 결과
├── find_similarity.py         # OCR 결과와 유사도 기반 후보 추출
├── book_info.csv              # 유사도 비교용 공공 데이터 포털에서 수집한 도서 정보 데이터셋
├── similarity_results_top2.txt # 유사도 상위 2개 후보 리스트
├── book_info_search.py        # Naver 도서 검색 (Selenium)
├── book_info_results.csv      # 크롤링된 책 정보
├── used_books_list.csv        # 사용자가 등록한 중고책 목록
├── README.md                  # 📖 프로젝트 설명서
```

---

## 🧠 세트 구성별 파일 설명

### 📌 1. 메인 앱 실행

| 파일 | 설명 |
|------|------|
| `app.py` | **Streamlit 기반의 메인 실행 파일**. 전체 프로세스(UI + 자동 실행)을 담당합니다. |

---

### 🧠 2. OCR + 유사도 분석 세트

| 파일 | 설명 |
|------|------|
| `detection_and_ocr.py` | YOLOv8로 책을 감지하여 `upload_labeled.jpg`을 생성하고, Tesseract로 제목 텍스트를 추출하여 `ocr_results.txt` 생성 |
| `find_similarity.py` | `ocr_results.txt`와 공공도서관소장도서 데이터셋(`book_info.csv`) 간 유사도를 계산해 상위 2개를 `similarity_results_top2.txt`로 저장 |
| `book_info.csv` | [공공 데이터 포털](https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=9bc56c9c-bc4e-4b68-90da-f4900009fc05)에서 수집한 도서 정보 데이터셋. 유사도 비교 기준으로 사용됨 |

---

### 🔍 3. 도서 정보 검색 세트

| 파일 | 설명 |
|------|------|
| `book_info_search.py` | `similarity_results_top2.txt`의 제목을 네이버에서 검색해 도서 정보(title, author, publisher, price 등)를 `book_info_results.csv`에 저장 |
| `book_info_results.csv` | 네이버에서 검색된 도서 정보 결과 |

---

### 📝 4. 사용자 입력 / 저장 관련

| 파일 | 설명 |
|------|------|
| `used_books_list.csv` | 사용자가 입력한 **중고책 정보**(상태, 희망가 포함)를 저장 |

---

### 🖼️ 5. 이미지 / 결과 파일

| 파일 | 설명 |
|------|------|
| `uploaded.jpg` | 사용자가 업로드한 이미지 |
| `upload_labeled.jpg` | 검출된 책 박스가 표시된 결과 이미지 |
| `ocr_results.txt` | OCR로 추출한 텍스트 결과 |
| `similarity_results_top2.txt` | 유사도 상위 2개의 후보 검색어 |

---

## 🛠 사용 기술 스택

- **Computer Vision**: OpenCV, YOLOv8, Tesseract OCR
- **데이터 유사도 분석**: `difflib.SequenceMatcher`, 정규표현식
- **크롤링**: Selenium (네이버 도서 검색)
- **웹 인터페이스**: Streamlit

---

## ✅ 예시

- 책장을 촬영한 이미지 업로드
- OCR로 자동 인식된 제목 → 유사한 도서 추천
- 저자/출판사/정가 자동 가져오기
- 중고 상태 선택 + 희망가 입력
- 최종 `.csv` 다운로드

---

## 📦 설치 필요 패키지

```txt
streamlit
pandas
opencv-python
pytesseract
selenium
ultralytics
```

---