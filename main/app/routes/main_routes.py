from flask import Blueprint, render_template, session
import json, os
from datetime import datetime

# ⬇️ 학식 관련 서비스 가져오기
from main.app.services.food_service import get_recommended_foods, crawl_food_menu

main_routes = Blueprint('main', __name__)

@main_routes.route("/")
def index():
    # 오늘 날짜
    today_str = datetime.today().strftime("%Y-%m-%d")
    today_display = datetime.today().strftime("%Y년 %m월 %d일")

    # ✅ 할 일 로드
    basedir = os.path.dirname(os.path.abspath(__file__))
    todo_path = os.path.join(basedir, "..", "tasks.json")

    tasks = []
    if os.path.exists(todo_path):
        with open(todo_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)

    today_tasks = [t for t in tasks if t.get("due") == today_str]
    today_done = sum(1 for t in today_tasks if t.get("done"))
    today_total = len(today_tasks)
    today_progress = round((today_done / today_total) * 100) if today_total else 0
    top_urgent_tasks = [t for t in today_tasks if t.get("priority") == "긴급"][:3]

    # ✅ 학식 정보 불러오기
    food_menus = crawl_food_menu(today_str)
    recommended_foods = get_recommended_foods(today_str)

    return render_template(
        "index.html",
        current_date=today_display,
        today_tasks=today_total,
        today_done=today_done,
        today_progress=today_progress,
        top_urgent_tasks=top_urgent_tasks,
        food_menus=food_menus,
        recommended_foods=recommended_foods
    )
