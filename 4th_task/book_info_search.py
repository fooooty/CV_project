from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
import re

# 1. OCR 유사도 파일에서 검색어 자동 추출
search_queries = []

with open("4th_task/similarity_results_top2.txt", "r", encoding="utf-8") as file:
    for line in file:
        match = re.search(r"- (.+?) \(", line)
        if match:
            title = match.group(1).strip()
            search_queries.append(title)

# ✅ 중복 제거
search_queries = list(dict.fromkeys(search_queries))

# 2. Selenium 설정
options = Options()
#options.add_argument("--headless")  # 주석처리로 화면 띄우기
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service('/Users/sonjiyeon/Downloads/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

results = []

# 3. 크롤링 시작
for query in search_queries:
    url = f"https://search.shopping.naver.com/book/search?query={query}"
    driver.get(url)
    time.sleep(2)

    try:
        book = driver.find_element(By.XPATH, "//li[starts-with(@class, 'bookListItem_item_book')]")
        
        title = book.find_element(
            By.CSS_SELECTOR,
            "span.bookListItem_text__oxa7M > span:nth-of-type(1)"
        ).text

        author = book.find_element(
            By.XPATH,
            ".//div[contains(@class, 'bookListItem_define_item')][.//span[text()='저자']]/span[contains(@class, 'bookListItem_define_data')]"
        ).text

        publisher = book.find_element(
            By.XPATH,
            ".//div[contains(@class, 'bookListItem_detail_publish')]/span[contains(@class, 'bookListItem_define_data')]"
        ).text

        price = book.find_element(
            By.XPATH,
            ".//span[starts-with(@class, 'bookPrice_price')]/em"
        ).text + "원"

        results.append([query, title, author, publisher, price])

    except Exception as e:
        print(f"[!] 검색 실패: {query} / {e}")
# 4. 결과 저장
with open("4th_task/book_info_results.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["검색어", "제목", "저자", "출판사", "가격"])
    writer.writerows(results)

print("[✓] 크롤링 완료 및 결과 저장: book_info_results.csv")
driver.quit()
