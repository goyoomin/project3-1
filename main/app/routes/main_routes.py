from flask import Blueprint, render_template
import json
import os
from datetime import datetime

main_routes = Blueprint('main', __name__)

def is_today_in_due(due_str, today_str):
    if "to" in due_str:
        try:
            start, end = due_str.split("to")
            return start.strip() <= today_str <= end.strip()
        except:
            return False
    else:
        return due_str.strip() == today_str

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

    # 오늘 포함된 일정 필터링
    today_tasks = [t for t in tasks if is_today_in_due(t.get("due", ""), today_str)]
    today_done = sum(1 for t in today_tasks if t.get("done"))
    today_total = len(today_tasks)
    today_progress = round((today_done / today_total) * 100) if today_total else 0
    top_urgent_tasks = [t for t in today_tasks if t.get("priority") == "긴급"][:3]

    return render_template(
        "index.html",
        current_date=today_display,
        today_tasks=today_total,
        today_done=today_done,
        today_progress=today_progress,
        top_urgent_tasks=top_urgent_tasks
    )
