from flask import Blueprint, request, jsonify, render_template
from app.services.food_service import get_recommended_foods, crawl_food_menu, search_restaurants_naver#, load_local_food#, search_restaurants_from_json
from datetime import datetime

#from ..services.food_service import load_local_food

food_bp = Blueprint('food', __name__)

@food_bp.route('/')
def index():
    # 초기 페이지: 오늘 날짜 데이터로 렌더링
    today_str = datetime.today().strftime('%Y-%m-%d')
    food_menus = crawl_food_menu(today_str)
    recommended_foods = get_recommended_foods(today_str)
    return render_template('food.html', food_menus=food_menus, recommended_foods=recommended_foods)

@food_bp.route('/api/foods')
def api_foods():
    # 날짜 쿼리 파라미터로 받음, 없으면 오늘 날짜 사용
    date_str = request.args.get('date')
    if not date_str:
        date_str = datetime.today().strftime('%Y-%m-%d')

    food_menus = crawl_food_menu(date_str)
    recommended_foods = get_recommended_foods(date_str)
    
    return jsonify({
        'food_menus': food_menus,
        'recommended_foods': recommended_foods
    })


@food_bp.route('/local')
def local_food():
    # 초기 페이지 렌더링 (검색창, 결과 표시 영역 포함)
    return render_template('food_local.html')

@food_bp.route('/api/local')
def api_local_food():
    user_query = request.args.get('query', '').strip()  # 빈 문자열도 잡기 위해 기본값 '' 사용
    if not user_query:  # 빈 문자열일 경우
        user_query = '식당'

    default_location = "한경대학교 근처"
    search_query = f"{default_location} {user_query}"

    local_foods = search_restaurants_naver(search_query, None, None)

    return jsonify({
        "query": user_query,
        "results": local_foods
    })

