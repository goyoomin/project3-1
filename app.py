from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests

app = Flask(__name__, static_url_path="/static", static_folder="static")

# Secret key 설정 (환경 변수로 관리 추천)
app.secret_key = "your_secret_key"

# 글로벌 일정 리스트
schedules = []

# 메인 페이지
@app.route("/")
def home():
    user = session.get("user")
    return render_template("main.html", user=user, schedules=schedules)

# 수정 버튼
@app.route('/edit_detail/<int:schedule_id>/<int:detail_id>', methods=['GET', 'POST'])
def edit_detail(schedule_id, detail_id):
    if request.method == 'POST':
        schedules[schedule_id]['details'][detail_id]['task'] = request.form['task']
        schedules[schedule_id]['details'][detail_id]['time'] = request.form['time']
        schedules[schedule_id]['details'][detail_id]['location'] = request.form['location']
        return redirect(url_for('index'))
    detail = schedules[schedule_id]['details'][detail_id]
    return render_template('edit_detail.html', detail=detail)

# 삭제 버튼
@app.route('/delete_detail/<int:schedule_id>/<int:detail_id>', methods=['POST'])
def delete_detail(schedule_id, detail_id):
    schedules[schedule_id]['details'].pop(detail_id)
    return redirect(url_for('index'))

# 일정 관리 페이지 (로그인 필요)
@app.route('/index')
def index():
    if "user" not in session:  # 세션에 사용자 정보가 없으면
        return redirect(url_for("login"))  # 로그인 페이지로 리디렉션

    # 각 일정의 details를 날짜별로 정렬
    for schedule in schedules:
        if 'details' in schedule and isinstance(schedule['details'], list):
            for detail in schedule['details']:
                if 'date' not in detail:
                    detail['date'] = '미정'  # 기본값 추가
            schedule['details'].sort(key=lambda x: x['date'])  # 날짜 기준 정렬

    # 현재 스케줄 데이터를 서버 콘솔에 출력
    print("Current schedules:", schedules)

    return render_template('index.html', schedules=schedules, user=session.get("user"))

# 일정 등록 페이지 (로그인 필요)
@app.route('/add', methods=['GET', 'POST'])
def add_schedule():
    if "user" not in session:  # 세션에 사용자 정보가 없으면
        return redirect(url_for("login"))  # 로그인 페이지로 리디렉션
    
    if request.method == 'POST':
        title = request.form.get('title')
        date_range = request.form.get('daterange').split(" to ")
        start_date = date_range[0]
        end_date = date_range[1] if len(date_range) > 1 else start_date

        # 리스트의 맨 앞에 새 일정 추가
        schedules.insert(0, {
            'title': title,
            'start_date': start_date,
            'end_date': end_date,
            'details': []
        })

        # 디버깅용 출력
        print("Updated schedules:", schedules)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:schedule_id>', methods=['POST'])
def delete_schedule(schedule_id):
    if 0 <= schedule_id - 1 < len(schedules):
        schedules.pop(schedule_id - 1)
    return redirect(url_for('index'))

@app.route('/edit/<int:schedule_id>', methods=['GET'])
def edit_schedule(schedule_id):
    # schedule_id에 해당하는 일정 데이터 확인
    if schedule_id < 1 or schedule_id > len(schedules):
        return "Invalid schedule ID", 404  # 유효하지 않은 ID 처리

    schedule = schedules[schedule_id - 1]  # 0-based index 사용
    return render_template('edit.html', schedule_id=schedule_id, schedule=schedule)

@app.route('/update/<int:index>', methods=['POST'])
def update_schedule(index):
    print(f"Updating schedule with ID: {index}")  # 디버깅 메시지
    date = request.form.get('date')
    task = request.form.get('task')
    time = request.form.get('time')
    location = request.form.get('location')

    # 새로운 세부 정보 추가
    new_detail = {
        'date': date if date else '미정',
        'task': task,
        'time': time,
        'location': location
    }

    if 'details' not in schedules[index - 1] or not isinstance(schedules[index - 1]['details'], list):
        schedules[index - 1]['details'] = []
    schedules[index - 1]['details'].append(new_detail)

    print("Updated schedules:", schedules)  # 디버깅 메시지
    return redirect('/index')

@app.route('/details/<int:schedule_id>')
def schedule_details(schedule_id):
    schedule = schedules[schedule_id - 1]
    # details가 없으면 기본값 설정
    if 'details' not in schedule or not schedule['details']:
        schedule['details'] = {
            'task': '세부 정보 없음',
            'time': '시간 정보 없음',
            'location': '위치 정보 없음'
        }
    return render_template('details.html', schedule=schedule)

# 실시간 날씨 정보를 반환
@app.route("/weather")
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "위치 정보가 제공되지 않았습니다."}), 400

    api_key = "c71e3d33cdc280883095bca0d2ea785e"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=kr"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "icon": data["weather"][0]["icon"],
            "city": data.get("name"),
            "description": data["weather"][0]["description"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
        return jsonify(weather_data)
    else:
        return jsonify({"error": f"API 요청 실패: {response.status_code}"}), response.status_code

# 추천 페이지
@app.route("/recommend")
def recommend():
    return render_template("recommend.html")

# chatbot 페이지
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

# 지도 페이지
@app.route("/map")
def map():
    return render_template("map.html")

# 로그인 페이지
@app.route("/login")
def login():
    return render_template("login.html")

# Kakao OAuth
@app.route("/oauth")
def oauth():
    code = request.args.get("code")
    if not code:
        return "카카오 인증 코드가 없습니다.", 400

    client_id = "407becad7762e834c7c08938bce8f3af"
    redirect_uri = "http://127.0.0.1:5000/oauth"

    # 액세스 토큰 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code": code
    }

    try:
        token_response = requests.post(token_url, data=data)
        token_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"토큰 요청 실패: {e}", 400

    token_json = token_response.json()
    access_token = token_json.get("access_token")
    if not access_token:
        return "액세스 토큰을 가져오지 못했습니다.", 400

    # 사용자 정보 요청
    user_url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        user_response = requests.get(user_url, headers=headers)
        user_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"사용자 정보 요청 실패: {e}", 400

    user_info = user_response.json()

    # 사용자 정보 저장
    try:
        session["user"] = {
            "nickname": user_info["kakao_account"]["profile"]["nickname"],
            "profile_image": user_info["kakao_account"]["profile"]["profile_image_url"],
        }
        session["access_token"] = access_token
    except KeyError as e:
        return f"사용자 정보 처리 실패: {e}", 400

    return redirect("/")

# 로그아웃
@app.route("/logout", methods=["POST"])
def logout():
    access_token = session.get("access_token")
    if access_token:
        logout_url = "https://kapi.kakao.com/v1/user/logout"
        headers = {"Authorization": f"Bearer {access_token}"}
        requests.post(logout_url, headers=headers)

    session.clear()
    return jsonify({"success": True})

# 세션 사용자 정보 주입
@app.context_processor
def inject_user():
    return dict(user=session.get("user"))

# 서버 시작 시 데이터 마이그레이션
for schedule in schedules:
    if 'details' in schedule and isinstance(schedule['details'], list):
        for detail in schedule['details']:
            if 'date' not in detail:
                detail['date'] = '미정'  # 기본값 추가

if __name__ == "__main__":
    app.run(debug=True)
