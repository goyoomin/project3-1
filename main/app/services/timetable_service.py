#timetable_serivie.py

from __future__ import annotations
import os, json
from typing import List, Dict
from flask import Flask, render_template, request, redirect, url_for, jsonify
from openai import OpenAI

# ── 경로 설정 ───────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../app
app  = Flask(__name__,
             template_folder=os.path.join(BASE, "templates"),
             static_folder=os.path.join(BASE, "static"))
app.config["TEMPLATES_AUTO_RELOAD"] = True
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

# ── 상수 ────────────────────────────────────────────────
DAYS  = ["Mon", "Tue", "Wed", "Thu", "Fri"]
HOURS = list(range(9, 19))  # 09~18
HEIGHT = (HOURS[-1] - HOURS[0]) * 60  # 540분

# ── 전역 데이터 ────────────────────────────────────────
NEXT_ID = 1
def nid():
    global NEXT_ID; NEXT_ID += 1; return NEXT_ID - 1

# 수업
SCHEDULE: List[Dict] = []   # {"id":.., "day":.., ...}

# 플래너
PLANS: List[Dict] = []      # {"id":.., "text":.., "done":False}

# ── 헬퍼 ───────────────────────────────────────────────
def build_blocks():
    out=[]
    for c in SCHEDULE:
        h1,m1=map(int,c["start"].split(':')); h2,m2=map(int,c["end"].split(':'))
        s=(h1-HOURS[0])*60+m1; e=(h2-HOURS[0])*60+m2
        if e<=s: continue
        out.append({"id":c["id"],
            "left":DAYS.index(c["day"])/len(DAYS)*100,
            "top": s/HEIGHT*100,"width":100/len(DAYS),
            "height":(e-s)/HEIGHT*100,
            "subject":c["subject"],"prof":c["prof"],"room":c["room"]})
    return out

# ── 라우트 ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("timetable.html",
        days=DAYS, hours=HOURS,
        blocks=build_blocks(), plans=PLANS)

# ── 수업 CRUD (변동 없음) ───────────────────────────────
@app.route("/add_course", methods=["POST"])
def add_course():
    SCHEDULE.append({"id":nid(),
        "day":request.form["day"],"start":request.form["start"],
        "end":request.form["end"],"subject":request.form["subject"],
        "prof":request.form.get("prof",""),"room":request.form.get("room","")})
    return redirect(url_for("index"))

@app.route("/course/<int:i>/json")
def course_json(i):  return _json_by_id(SCHEDULE,i)

@app.route("/course/<int:i>/update", methods=["POST"])
def course_update(i):
    _update(SCHEDULE,i,dict(day=request.form["day"],start=request.form["start"],
            end=request.form["end"],subject=request.form["subject"],
            prof=request.form.get("prof",""),room=request.form.get("room","")))
    return redirect(url_for("index"))

@app.route("/course/<int:i>/delete", methods=["POST"])
def course_del(i):
    _delete(SCHEDULE,i); return redirect(url_for("index"))

# ── 플래너 CRUD ───────────────────────────────────────
@app.route("/add_plan", methods=["POST"])
def add_plan():
    txt=request.form["plan"].strip()
    if txt: PLANS.append({"id":nid(),"text":txt,"done":False})
    return redirect(url_for("index"))

@app.route("/plan/<int:i>/toggle", methods=["POST"])
def plan_toggle(i):
    for p in PLANS:
        if p["id"]==i: p["done"]=not p["done"]; break
    return jsonify(ok=True)

# GPT 추천 그대로 (done=False 로 삽입) ──────────────────
@app.route("/gpt", methods=["POST"])
def gpt():
    prompt="이번 주 학습 계획 5가지 한 줄씩 추천해줘."
    try:
        res=client.chat.completions.create(model="gpt-4.0",
            messages=[{"role":"user","content":prompt}])
        for ln in res.choices[0].message.content.splitlines():
            txt=ln.strip("•*- ").strip()
            if txt: PLANS.append({"id":nid(),"text":txt,"done":False})
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False,error=str(e)),500

# ── 헬퍼 함수들 ───────────────────────────────────────
def _json_by_id(arr,i):
    for o in arr:
        if o["id"]==i: return jsonify(o)
    return jsonify(error="not found"),404

def _update(arr,i,vals):
    for o in arr:
        if o["id"]==i: o.update(vals); break

def _delete(arr,i):
    arr[:]=[o for o in arr if o["id"]!=i]

# ── 실행 ───────────────────────────────────────────────
if __name__=="__main__":
    app.run(debug=True)
