# main/app/routes/timetable_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session
from main.app.routes.todolist_routes import tasks as TODO_TASKS, calculate_dday, save_tasks
import cohere
import os
import re
from datetime import datetime

timetable_bp = Blueprint('timetable', __name__, url_prefix='/timetable')

# ── Cohere 클라이언트 초기화 ──
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "OeITm0DSjgEmWRNrdOua50mxn5Ra26AkeaWdYEUH")
if not COHERE_API_KEY:
    raise RuntimeError("환경 변수 COHERE_API_KEY를 설정해 주세요.")
co = cohere.Client(COHERE_API_KEY)

# ── 상수 및 전역 데이터 ──
DAYS         = ["Mon", "Tue", "Wed", "Thu", "Fri"]
HOURS        = list(range(9, 19))
SEMESTERS    = ["2024-1", "2024-2", "2025-1"]
NEXT_ID      = 1
SCHEDULE     = []
PLANS        = []
COLOR_PALETTE = [
    '#FFA69E','#AFCBFF','#D6D6F5','#FFCC70','#C0FFEE',
    '#B0E57C','#F7A9A8','#A7C7E7','#FFD700','#C8A2C8'
]
subject_colors = {}

def nid():
    global NEXT_ID
    NEXT_ID += 1
    return NEXT_ID - 1

def assign_color(subject):
    if subject not in subject_colors:
        subject_colors[subject] = COLOR_PALETTE[len(subject_colors) % len(COLOR_PALETTE)]
    return subject_colors[subject]

def build_blocks(semester):
    HEADER_PX = 60
    blocks = []
    for c in SCHEDULE:
        if c.get("semester") != semester:
            continue
        h1, m1 = map(int, c["start"].split(":"))
        h2, m2 = map(int, c["end"].split(":"))
        start_px  = HEADER_PX + (h1 - HOURS[0]) * 60 + m1
        height_px = (h2 - HOURS[0]) * 60 + m2 - ((h1 - HOURS[0]) * 60 + m1)
        if height_px <= 0:
            continue
        blocks.append({
            "id": c["id"],
            "col_idx": DAYS.index(c["day"]),
            "top_px": start_px,
            "height_px": height_px,
            "width": 100 / len(DAYS),
            "subject": c["subject"],
            "prof": c["prof"],
            "room": c["room"],
            "color": assign_color(c["subject"]),
            "memo": c.get("memo", ""),
            "start": c["start"],
            "end": c["end"]
        })
    return blocks

def gpt_generate(prompt: str) -> list[str]:
    """Cohere Chat API로 학습 계획 5개를 받아 문자열 리스트로 반환"""
    resp = co.chat(
        model="command-r",            # 최신 기본 모델 (plan에 맞게 필요하면 조정)
        message=prompt,               # v1 호환 파라미터
        temperature=0.7,
        max_tokens=150
    )
    raw = resp.text.strip()

     # ▸ 줄 단위로 자르고 ■ 날짜가 들어 있는 행만 수집
    lines = []
    for ln in raw.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        # 앞쪽 불릿 기호만 제거하고 **숫자는 남겨 둔다**
        ln = ln.lstrip("•*-– ").strip()
        if re.search(r"\d{4}[-./]\d{2}[-./]\d{2}", ln):
            lines.append(ln)
    return lines[:5]

def calculate_dday(due_date):
    try:
        today = datetime.today().date()
        due   = datetime.strptime(due_date, '%Y-%m-%d').date()
        return (due - today).days          # ▶ int
    except Exception:
        return None 


@timetable_bp.route("/")
def index():
    semester = request.args.get("semester") or session.get("semester") or SEMESTERS[-1]
    session["semester"] = semester
    return render_template(
        "timetable.html",
        days=DAYS,
        hours=HOURS,
        blocks=build_blocks(semester),
        plans=PLANS,
        semesters=SEMESTERS,
        current_semester=semester
    )

@timetable_bp.route("/add_course", methods=["POST"])
def add_course():
    sem = session.get("semester", SEMESTERS[-1])
    SCHEDULE.append({
        "id": nid(),
        "day": request.form["day"],
        "start": request.form["start"],
        "end": request.form["end"],
        "subject": request.form["subject"],
        "prof": request.form.get("prof", ""),
        "room": request.form.get("room", ""),
        "memo": request.form.get("memo", ""),
        "semester": sem
    })
    return redirect(url_for("timetable.index"))

@timetable_bp.route("/edit_course/<int:course_id>", methods=["POST"])
def edit_course(course_id):
    for c in SCHEDULE:
        if c["id"] == course_id:
            c.update({
                "day": request.form["day"],
                "start": request.form["start"],
                "end": request.form["end"],
                "subject": request.form["subject"],
                "prof": request.form.get("prof", ""),
                "room": request.form.get("room", ""),
                "memo": request.form.get("memo", "")
            })
            break
    return redirect(url_for("timetable.index"))

@timetable_bp.route("/delete_course/<int:course_id>", methods=["POST"])
def delete_course(course_id):
    global SCHEDULE
    SCHEDULE = [c for c in SCHEDULE if c["id"] != course_id]
    return redirect(url_for("timetable.index"))

@timetable_bp.route("/semester/add", methods=["POST"])
def add_semester():
    new_sem = request.form["new_semester"].strip()
    if new_sem and new_sem not in SEMESTERS:
        SEMESTERS.append(new_sem)
    return redirect(url_for("timetable.index"))

@timetable_bp.route("/semester/delete", methods=["POST"])
def delete_semester():
    del_sem = request.form["del_semester"]
    if del_sem in SEMESTERS and del_sem != session.get("semester"):
        SEMESTERS.remove(del_sem)
    return redirect(url_for("timetable.index"))

def _plan_exists(text, due):
    return any(p["text"] == text and p.get("due") == due for p in PLANS)

@timetable_bp.route("/add_plan", methods=["POST"])
def add_plan():
    text = request.form["plan"].strip()
    due  = request.form.get("due", "").strip()
    if text and not _plan_exists(text, due):         # ← 중복이면 건너뜀
        PLANS.append({"id": nid(), "text": text, "due": due, "done": False})
    return redirect(url_for("timetable.index"))

def _todo_exists(title, due):
    return any(t["title"] == title and t.get("due") == due for t in TODO_TASKS)

@timetable_bp.route("/plan/<int:plan_id>/toggle", methods=["POST"])
def plan_toggle(plan_id):
    for p in PLANS:
        if p["id"] == plan_id:
            p["done"] = not p["done"]
            if p["done"] and not _todo_exists(p["text"], p.get("due", "")):
                TODO_TASKS.append({
                    "title": p["text"],
                    "due":   p.get("due", ""),
                    "priority": "보통",
                    "memo": "",
                    "done": False,
                    "dday": calculate_dday(p.get("due", ""))
                })
                save_tasks(TODO_TASKS)
            break
    return redirect(url_for("timetable.index"))

@timetable_bp.route("/delete_plan/<int:plan_id>", methods=["POST"])
def delete_plan(plan_id):
    global PLANS
    PLANS = [p for p in PLANS if p["id"] != plan_id]
    return redirect(url_for("timetable.index"))

@timetable_bp.route("/gpt", methods=["POST"])
def gpt():
    sem = session.get("semester")
    schedule = [c for c in SCHEDULE if c.get("semester") == sem]
    sched_str = "\n".join(
        f"- {c['day']} {c['start']}-{c['end']}: {c['subject']}"
        for c in schedule
    ) or "시간표에 등록된 수업이 없습니다."
    plans_str = "\n".join(
        f"- {p['text']} (마감: {p['due'] or '미정'})"
        for p in PLANS
    ) or "등록된 할 일이 없습니다."

    prompt = (
        f"내 시간표:\n{sched_str}\n\n"
        f"할 일 목록:\n{plans_str}\n\n"
        "▶ 반드시 “YYYY-MM-DD: 과제명 공부하기” 형식으로만 5줄 출력해 주세요.\n"
        "▶ 첫 글자는 날짜(네 자리 연도-두 자리 월-두 자리 일)여야 하며, 날짜 뒤엔 콜론(:)을 넣어 주세요.\n"
        "▶ 오늘 기준 7일 이내의 날짜를 사용해 주세요.\n"
        "예시\n"
        "2025-06-15: 알고리즘 과제 마무리하기\n"
        "2025-06-16: 문제해결프로젝트 초안 작성\n"
)


    recs = gpt_generate(prompt)
    for bullet in recs:
        line = bullet.lstrip("-–• \t").strip()

        m = re.search(r"(\d{4}-\d{2}-\d{2})", line)
        if m:
            due = m.group(1)
            text = re.sub(rf".*?{re.escape(due)}[:\s\-–]*", "", line).strip()        
        else:
            due, text = "", line

        PLANS.append({"id": nid(), "text": text, "due": due, "done": False})


    return redirect(url_for("timetable.index"))
