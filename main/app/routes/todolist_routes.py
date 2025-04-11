# app/routes/todolist_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

todolist_bp = Blueprint('todolist', __name__, url_prefix='/todolist')

tasks = []

def calculate_dday(due_date):
    try:
        today = datetime.today().date()
        due = datetime.strptime(due_date, '%Y-%m-%d').date()
        return (due - today).days
    except:
        return "?"

@todolist_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        due = request.form.get("due", "").strip()

        if not title:
            flash("할 일을 입력해주세요.")
            return redirect(url_for('todolist.index'))

        new_task = {
            "title": title,
            "due": due,
            "priority": "보통",
            "memo": "",
            "done": False,
            "dday": calculate_dday(due)
        }

        tasks.append(new_task)
        flash("추가되었습니다!")
        return redirect(url_for('todolist.index'))

    sorted_tasks = sorted(tasks, key=lambda t: t["dday"] if isinstance(t["dday"], int) else 9999)
    return render_template("todolist.html", tasks=sorted_tasks)

@todolist_bp.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_done(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
    return redirect(url_for('todolist.index'))
