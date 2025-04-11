# main/todolist/todolist_web.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

# 블루프린트 정의
todolist_bp = Blueprint('todolist', __name__, url_prefix="/todolist")

# 초기 할 일 목록 (임시 메모리 저장)
tasks = []

# D-day 계산 함수
def calculate_dday(due_date):
    try:
        today = datetime.today().date()
        due = datetime.strptime(due_date, '%Y-%m-%d').date()
        return (due - today).days
    except:
        return "?"

# 메인 화면 및 추가 처리
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
            "priority": "보통",   # 기본 우선순위
            "memo": "",
            "done": False,
            "dday": calculate_dday(due)
        }

        tasks.append(new_task)
        flash("추가되었습니다!")
        return redirect(url_for('todolist.index'))

    # D-day 기준 정렬
    sorted_tasks = sorted(tasks, key=lambda t: t["dday"] if isinstance(t["dday"], int) else 9999)
    return render_template("todolist.html", tasks=sorted_tasks)

# 완료 체크 토글
@todolist_bp.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_done(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
    return redirect(url_for('todolist.index'))
