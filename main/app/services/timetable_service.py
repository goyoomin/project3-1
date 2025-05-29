from __future__ import annotations
import os, json
from typing import List, Dict
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from openai import OpenAI

# ── 경로 & 앱 ───────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app  = Flask(__name__,
             template_folder=os.path.join(BASE, "templates"),
             static_folder=os.path.join(BASE, "static"))
app.secret_key = "secret_key_for_session"
app.config["TEMPLATES_AUTO_RELOAD"] = True
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

# ── Todo 블루프린트 가져오기 ───────────────────────────
from app.routes.todolist_routes import todolist_bp, tasks as TODO_TASKS, calculate_dday
app.register_blueprint(todolist_bp)

# ── 상수 ────────────────────────────────────────────────
DAYS  = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
HOURS = list(range(9, 19))
HEIGHT = (HOURS[-1] - HOURS[0]) * 60
SEMESTERS = ["2024-2", "2025-1", "2025-2"]

# ── 데이터 ─────────────────────────────────────────────
NEXT_ID = 1

def nid() -> int:
    global NEXT_ID
    NEXT_ID += 1
    return NEXT_ID - 1

SCHEDULE: List[Dict] = []
PLANS:    List[Dict] = []
COLOR_PALETTE = [
    '#FFA69E', '#AFCBFF', '#D6D6F5', '#FFCC70', '#C0FFEE',
    '#B0E57C', '#F7A9A8', '#A7C7E7', '#FFD700', '#C8A2C8'
]
subject_colors: Dict[str, str] = {}

def assign_color(subject: str) -> str:
    if subject not in subject_colors:
        index = len(subject_colors) % len(COLOR_PALETTE)
        subject_colors[subject] = COLOR_PALETTE[index]
    return subject_colors[subject]

def build_blocks(semester: str):
    out = []
    for c in SCHEDULE:
        if c.get("semester") != semester:
            continue
        h1, m1 = map(int, c["start"].split(":"))
        h2, m2 = map(int, c["end"].split(":"))
        s = (h1 - HOURS[0]) * 60 + m1
        e = (h2 - HOURS[0]) * 60 + m2
        if e <= s:
            continue
        out.append({
            "id": c["id"],
            "left": DAYS.index(c["day"]) / len(DAYS) * 100,
            "top": s / HEIGHT * 100,
            "width": 100 / len(DAYS),
            "height": (e - s) / HEIGHT * 100,
            "subject": c["subject"],
            "prof": c["prof"],
            "room": c["room"],
            "color": assign_color(c["subject"]),
            "memo": c.get("memo", ""),
            "start": c["start"],
            "end": c["end"]
        })
    return out

# ── 메인 화면 ───────────────────────────────────────────
@app.route("/")
def index():
    semester = request.args.get("semester") or session.get("semester") or SEMESTERS[-1]
    session["semester"] = semester
    return render_template("timetable.html",
        days=DAYS, hours=HOURS,
        blocks=build_blocks(semester),
        plans=PLANS,
        semesters=SEMESTERS,
        current_semester=semester)

# ── SCHEDULE CRUD ─────────────────────────────────────
@app.route("/add_course", methods=["POST"])
def add_course():
    semester = session.get("semester", SEMESTERS[-1])
    SCHEDULE.append({
        "id": nid(),
        "day":    request.form["day"],
        "start":  request.form["start"],
        "end":    request.form["end"],
        "subject":request.form["subject"],
        "prof":   request.form.get("prof", ""),
        "room":   request.form.get("room", ""),
        "memo": request.form.get("memo", ""),
        "semester": semester
    })
    return redirect(url_for("index"))

@app.route("/edit_course/<int:course_id>", methods=["POST"])
def edit_course(course_id):
    for c in SCHEDULE:
        if c["id"] == course_id:
            c.update({
                "day":    request.form["day"],
                "start":  request.form["start"],
                "end":    request.form["end"],
                "subject":request.form["subject"],
                "prof":   request.form.get("prof", ""),
                "room":   request.form.get("room", ""),
                "memo":    request.form.get("memo", "")
            })
            break
    return redirect(url_for("index"))

@app.route("/delete_course/<int:course_id>", methods=["POST"])
def delete_course(course_id):
    global SCHEDULE
    SCHEDULE = [c for c in SCHEDULE if c["id"] != course_id]
    return redirect(url_for("index"))

@app.route("/semester/add", methods=["POST"])
def add_semester():
    new_sem = request.form["new_semester"].strip()
    if new_sem and new_sem not in SEMESTERS:
        SEMESTERS.append(new_sem)
    return redirect(url_for("index"))

@app.route("/semester/delete", methods=["POST"])
def delete_semester():
    del_sem = request.form["del_semester"]
    if del_sem in SEMESTERS and del_sem != session.get("semester"):
        SEMESTERS.remove(del_sem)
    return redirect(url_for("index"))


# ── PLANNER CRUD ──────────────────────────────────────
@app.route("/add_plan", methods=["POST"])
def add_plan():
    text = request.form["plan"].strip()
    due = request.form.get("due", "").strip()
    if text:
        PLANS.append({"id": nid(), "text": text, "due": due, "done": False})
    return redirect(url_for("index"))

@app.route("/plan/<int:i>/toggle", methods=["POST"])
def plan_toggle(i):
    for p in PLANS:
        if p["id"] == i:
            p["done"] = not p["done"]
            if p["done"]:
                TODO_TASKS.append({
                    "title":    p["text"],
                    "due":      p.get("due", ""),
                    "priority": "보통",
                    "memo":     "",
                    "done":     False,
                    "dday":     calculate_dday(p.get("due", "")),
                })
            break
    return jsonify(ok=True)

# ── GPT 추천 ───────────────────────────────────────────
@app.route("/gpt", methods=["POST"])
def gpt():
    prompt = "이번 주 학습 계획 5가지 한 줄씩 추천해줘."
    try:
        res = client.chat.completions.create(
            model="gpt-4.0",
            messages=[{"role": "user", "content": prompt}],
        )
        for line in res.choices[0].message.content.splitlines():
            txt = line.strip("\u2022*- ").strip()
            if txt:
                PLANS.append({"id": nid(), "text": txt, "due": "", "done": False})
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500

# ── 실행 ───────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)