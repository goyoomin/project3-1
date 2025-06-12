import requests
from bs4 import BeautifulSoup
from datetime import datetime
import ssl
from urllib.request import urlopen
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import json
import os

# 보안 수준 낮춘 SSLContext 생성
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')  # ← 핵심 우회 설정
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# requests 세션에 어댑터 연결
session = requests.Session()
session.mount('https://', SSLAdapter())

# 첫 번째 크롤링 함수: 기식 메뉴 가져오기
def get_recommended_foods(selected_date_str=None):
    # 선택한 날짜가 없으면 오늘 날짜 사용
    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d')
    else:
        selected_date = datetime.now()

    selected_day = str(selected_date.day)  # '16' 같은 문자열로 변환

    url = "https://dormitory.hknu.ac.kr/bbs/board.php?bo_table=foodplan&h_flag=2"
    response = session.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    date_spans = soup.find_all("span", class_="caldate")
    meals = { "f01": "아침", "f02": "점심", "f03": "저녁" }
    meal_results = { "아침": "정보 없음", "점심": "정보 없음", "저녁": "정보 없음" }

    for date_span in date_spans:
        if date_span.text.strip() == selected_day:
            parent = date_span.find_parent("td")
            if not parent:
                continue
            plans = parent.find_all("ul", class_="plan")
            for plan in plans:
                for li in plan.find_all("li"):
                    span = li.find("span")
                    if span and span.get("class"):
                        cls = span.get("class")[0]
                        if cls in meals:
                            meal_time = li.get_text(separator="\n", strip=True).split('\n')
                            filtered = ["" if line == "8:00~9:30" else line for line in meal_time[1:]]
                            menu = "\n".join(filtered)
                            meal_results[meals[cls]] = menu.replace("\n", "<br>")

    return meal_results

# 두 번째 크롤링 함수: 학식 메뉴 가져오기
def crawl_food_menu(date_str=None):
    url = 'https://www.hknu.ac.kr/kor/670/subview.do'

    # 날짜 기본값: 오늘 날짜
    if date_str is None:
        date_str = datetime.today().strftime('%Y-%m-%d')
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y.%m.%d")
    except ValueError:
        # 날짜 형식 틀리면 오늘 날짜로 자동 변경
        target_date = datetime.today().strftime("%Y.%m.%d")

    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    food_menus = {
        "날짜": target_date,
        "맛난한끼": "",
        "건강한끼": ""
    }

    rows = soup.find_all('tr')
    current_date = None

    for row in rows:
        date_th = row.find('th', class_='dietDate')
        if date_th:
            lines = list(date_th.stripped_strings)
            if lines:
                current_date = lines[0].strip()

        if current_date != target_date:
            continue

        name_td = row.find('td', class_='dietNm')
        menu_td = row.find('td', class_='dietCont')

        if not name_td or not menu_td:
            continue

        restaurant_name = name_td.get_text(strip=True)
        raw_html = menu_td.decode_contents()
        menu_items = [item.strip() for item in raw_html.split('<br/>') if item.strip()]

        if "맛난한끼" in restaurant_name:
            food_menus["맛난한끼"] += "<br>".join(menu_items)
        elif "건강한끼" in restaurant_name:
            food_menus["건강한끼"] += "<br>".join(menu_items)

    return food_menus


NAVER_CLIENT_ID = "PIs5t_2gp8q1fT2lfkaw"
NAVER_CLIENT_SECRET = "lzPlbCZdT1"

def search_restaurants_naver(query, x=None, y=None):
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    url = f"https://openapi.naver.com/v1/search/local.json"
    params = {
        "query": query,
        "display": 5,
        "start": 1,
        "sort": "random"
    }
    if x and y:
        params['x'] = x
        params['y'] = y

    res = requests.get(url, headers=headers, params=params)
    data = res.json()
    return data.get("items", [])
