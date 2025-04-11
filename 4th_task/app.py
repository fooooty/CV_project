import streamlit as st
import pandas as pd
import os

# 파일 경로
BOOK_INFO_PATH = "4th_task/book_info_results.csv"
USED_BOOKS_PATH = "4th_task/used_books_list.csv"
UPLOAD_IMAGE_PATH = "4th_task/uploaded.jpg"

# Streamlit 페이지 설정
st.set_page_config(page_title="중고책 자동 등록기", layout="centered")
st.title("📚 중고책 판매 자동 등록기")

# 초기화 (세션 상태)
if "ocr_done" not in st.session_state:
    st.session_state.ocr_done = False
if "final_submitted" not in st.session_state:
    st.session_state.final_submitted = False

# 📸 이미지 업로드
uploaded_file = st.file_uploader("책장이 찍힌 이미지(.jpg/.jpeg)를 업로드하세요", type=["jpg", "jpeg"])

if uploaded_file and not st.session_state.ocr_done:
    # 1. 이미지 저장
    with open(UPLOAD_IMAGE_PATH, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ 이미지 업로드 완료! OCR 및 유사도 분석 중...")

    # 2. 외부 스크립트 실행 (OCR → 유사도 → 책 검색)
    with st.spinner("🔍 책 인식 및 정보 검색 중... 잠시만 기다려주세요"):
        os.system("python 4th_task/detection_and_ocr.py")
        os.system("python 4th_task/find_similarity.py")
        os.system("python 4th_task/book_info_search.py")
    st.session_state.ocr_done = True
    st.success("✅ 책 정보 분석이 완료되었습니다!")

# 3. 분석 결과 로드
if st.session_state.ocr_done and os.path.exists(BOOK_INFO_PATH):
    df = pd.read_csv(BOOK_INFO_PATH)
    st.subheader("📖 추출된 책 정보")

    for i, row in df.iterrows():
        with st.expander(f"🔎 {row['제목']}"):
            st.markdown(f"**저자:** {row['저자']}")
            st.markdown(f"**출판사:** {row['출판사']}")
            st.markdown(f"**정가:** {row['가격']}")

            # 상태 및 희망가 입력
            condition = st.radio(f"📦 상태 선택 - {row['제목']}", ["상", "중", "하"], key=f"condition_{i}", horizontal=True)
            price_input = st.text_input(f"💰 희망 판매가 (숫자만)", key=f"price_{i}")

            if st.session_state.get(f"confirmed_{i}", False) is False:
                if st.button("📥 이 책 등록", key=f"register_{i}"):
                    if not price_input.isdigit():
                        st.warning("숫자만 입력해주세요!", icon="⚠️")
                    else:
                        new_row = {
                            "제목": row["제목"],
                            "저자": row["저자"],
                            "출판사": row["출판사"],
                            "네이버 최저 가격": row["가격"],
                            "상태": condition,
                            "희망판매가": f"{int(price_input):,}원"
                        }

                        # 파일에 저장
                        if os.path.exists(USED_BOOKS_PATH):
                            used_df = pd.read_csv(USED_BOOKS_PATH)
                            used_df = pd.concat([used_df, pd.DataFrame([new_row])], ignore_index=True)
                        else:
                            used_df = pd.DataFrame([new_row])

                        used_df.to_csv(USED_BOOKS_PATH, index=False, encoding="utf-8-sig")
                        st.session_state[f"confirmed_{i}"] = True
                        st.success("✅ 등록 완료")

    # ✅ 최종 등록 마무리 및 다운로드
    st.divider()
    if st.button("✅ 선택 완료 및 CSV 만들기"):
        st.session_state.final_submitted = True

    if st.session_state.final_submitted:
        if os.path.exists(USED_BOOKS_PATH):
            st.success("📁 최종 등록된 책 목록")
            final_df = pd.read_csv(USED_BOOKS_PATH)
            st.dataframe(final_df)
            st.download_button(
                label="📂 중고책 리스트 CSV 다운로드",
                data=final_df.to_csv(index=False, encoding="utf-8-sig"),
                file_name="used_books_final.csv",
                mime="text/csv"
            )
        else:
            st.warning("등록된 책이 없습니다!", icon="⚠️")
