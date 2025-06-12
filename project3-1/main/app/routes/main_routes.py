from flask import Blueprint, render_template
import json, os
from datetime import datetime
import main.app.routes.timetable_routes as timetable_routes  # ✅ 실시간 참조

main_routes = Blueprint('main', __name__)

@main_routes.route("/")
def index():
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_display = datetime.now().strftime("%Y년 %m월 %d일")

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

    # ✅ current_semester를 선언해야 함!
    semester = timetable_routes.SEMESTERS[-1]
    blocks = timetable_routes.build_blocks(semester, row_height=60, header_height=84)

    return render_template(
        "index.html",
        current_date=today_display,
        today_tasks=today_total,
        today_done=today_done,
        today_progress=today_progress,
        top_urgent_tasks=top_urgent_tasks,
        days=timetable_routes.DAYS,
        hours=timetable_routes.HOURS,
        blocks=blocks
    )
