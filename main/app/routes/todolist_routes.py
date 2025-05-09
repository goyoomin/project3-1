import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta

todolist_bp = Blueprint('todolist', __name__, url_prefix='/todolist')

TASKS_FILE = "tasks.json"


# 🔹 JSON에서 로드
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 🔹 JSON에 저장
def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# 🔹 D-day 계산
def calculate_dday(due_date):
    try:
        today = datetime.today().date()
        due = datetime.strptime(due_date, '%Y-%m-%d').date()
        return (due - today).days
    except:
        return "?"

# 🔹 진행률 및 주간 통계
def calculate_stats(tasks):
    today = datetime.today().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    total = len(tasks)
    done = sum(1 for t in tasks if t.get("done"))
    progress = int((done / total) * 100) if total > 0 else 0

    added, completed = 0, 0
    for t in tasks:
        try:
            d = t["due"].split(" to ")[0] if "to" in t["due"] else t["due"]
            due_date = datetime.strptime(d, '%Y-%m-%d').date()
            if week_start <= due_date <= week_end:
                added += 1
                if t.get("done"):
                    completed += 1
        except:
            continue

    return progress, added, completed

# 🔸 메인 화면
@todolist_bp.route("/", methods=["GET", "POST"])
def index():
    tasks = load_tasks()
    keyword = request.args.get("keyword", "").strip()
    hide_done = request.args.get("hide_done") == "on"

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        due = request.form.get("due", "").strip()
        priority = request.form.get("priority", "보통")
        memo = request.form.get("memo", "").strip()

        if not title or not due:
            flash("할 일과 날짜를 입력해주세요.")
            return redirect(url_for('todolist.index'))

        dday_base = due.split(" to ")[0] if "to" in due else due

        new_task = {
            "title": title,
            "due": due,
            "priority": priority,
            "memo": memo,
            "done": False,
            "dday": calculate_dday(dday_base)
        }

        tasks.append(new_task)
        save_tasks(tasks)
        flash("추가 완료!")
        return redirect(url_for('todolist.index'))

    filtered = [
        t for t in tasks
        if keyword.lower() in t["title"].lower() and (not hide_done or not t["done"])
    ]
    sorted_tasks = sorted(filtered, key=lambda t: t["dday"] if isinstance(t["dday"], int) else 9999)

    progress, added_week, done_week = calculate_stats(tasks)

    return render_template("todolist.html",
                           tasks=sorted_tasks,
                           keyword=keyword,
                           hide_done=hide_done,
                           progress=progress,
                           added_this_week=added_week,
                           done_this_week=done_week)

# 🔸 완료 토글
@todolist_bp.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_done(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
        save_tasks(tasks)
    return redirect(url_for('todolist.index'))

# 🔸 삭제
@todolist_bp.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for('todolist.index'))

# 🔸 수정
@todolist_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            due = request.form.get("due", "").strip()
            priority = request.form.get("priority", "보통")
            memo = request.form.get("memo", "").strip()

            dday_base = due.split(" to ")[0] if "to" in due else due

            tasks[task_id].update({
                "title": title,
                "due": due,
                "priority": priority,
                "memo": memo,
                "dday": calculate_dday(dday_base)
            })
            save_tasks(tasks)
            return redirect(url_for('todolist.index'))

        return render_template("edit_task.html", task=tasks[task_id], task_id=task_id)

    return redirect(url_for('todolist.index'))

# 🔸 캘린더 보기
@todolist_bp.route("/calendar")
def calendar_view():
    tasks = load_tasks()
    return render_template("calendar.html", tasks=tasks)

# 🔸 날짜 수정 (드래그)
@todolist_bp.route("/update-date/<int:task_id>", methods=["POST"])
def update_date(task_id):
    tasks = load_tasks()  # ✅ 꼭 필요!
    if 0 <= task_id < len(tasks):
        data = request.get_json()
        new_date = data.get("new_date")
        tasks[task_id]["due"] = new_date
        tasks[task_id]["dday"] = calculate_dday(new_date)
        save_tasks(tasks)  # ✅ 저장까지!
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "fail"}), 400

