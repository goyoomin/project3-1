from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. 브라우저 자동 실행
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 창 없이 실행하고 싶으면 이 옵션 추가
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 2. 공지사항 페이지 접속
url = "https://www.hknu.ac.kr/kor/560/subview.do"
driver.get(url)
time.sleep(2)  # 페이지 로딩 대기

notices = []
rows = driver.find_elements(By.CSS_SELECTOR, ".board-list tbody tr")
for row in rows:
    try:
        title_tag = row.find_element(By.CSS_SELECTOR, "td.title a")
        title = title_tag.text.strip()
        link = title_tag.get_attribute('href')
        date = row.find_elements(By.TAG_NAME, "td")[4].text.strip()
        notices.append({"title": title, "link": link, "date": date})
    except Exception as e:
        continue

driver.quit()

# 결과 출력
for notice in notices[:10]:
    print(f"[{notice['date']}] {notice['title']} → {notice['link']}")
