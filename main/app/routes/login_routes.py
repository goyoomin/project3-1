from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import os
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

KAKAO_CLIENT_ID = os.getenv('KAKAO_REST_API_KEY')
KAKAO_REDIRECT_URI = os.getenv('KAKAO_REDIRECT_URI')

login_bp = Blueprint('login', __name__, url_prefix='/login')

# 📌 임시 사용자 저장소 (배포 시 DB로 대체)
users = {}

# 🔐 일반 로그인
@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            session['name'] = user['name']
            session['email'] = user.get('email', '')
            session['student_id'] = user.get('student_id', '')
            session['department'] = user.get('department', '')
            flash("✅ 로그인 성공!")
            return redirect(url_for('main.index'))
        else:
            flash("❌ 아이디 또는 비밀번호가 일치하지 않습니다.")
            return redirect(url_for('login.login'))

    return render_template('login.html')

# 🔐 회원가입
@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        student_id = request.form.get('student_id')
        department = request.form.get('department')

        if username in users:
            flash("⚠️ 이미 존재하는 아이디입니다.")
            return redirect(url_for('login.register'))

        if password != confirm:
            flash("❗ 비밀번호가 일치하지 않습니다.")
            return redirect(url_for('login.register'))

        users[username] = {
            'name': name,
            'email': email,
            'password': generate_password_hash(password),
            'student_id': student_id,
            'department': department
        }

        session['user'] = username
        session['name'] = name
        session['email'] = email
        session['student_id'] = student_id
        session['department'] = department

        return render_template('register_success_to_login.html')

    return render_template('register.html')

# 🔐 카카오 로그인
@login_bp.route('/kakao')
def kakao_login():
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
    )
    return redirect(kakao_auth_url)

# 🔁 카카오 로그인 콜백
@login_bp.route('/kakao/callback')
def kakao_callback():
    code = request.args.get('code')

    token_url = "https://kauth.kakao.com/oauth/token"
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_CLIENT_ID,
        'redirect_uri': KAKAO_REDIRECT_URI,
        'code': code
    }

    token_res = requests.post(token_url, data=token_data)
    access_token = token_res.json().get("access_token")

    if not access_token:
        flash("⚠️ 카카오 로그인 중 문제가 발생했습니다.")
        return redirect(url_for('login.login'))

    user_info_res = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_info_res.json()

    nickname = (
        user_info.get("properties", {}).get("nickname") or
        user_info.get("kakao_account", {}).get("profile", {}).get("nickname") or
        "사용자"
    )

    session['user'] = nickname
    session['name'] = nickname
    session['email'] = user_info.get("kakao_account", {}).get("email", '')
    session['student_id'] = ''
    session['department'] = ''

    flash(f"✅ {nickname}님, 카카오 로그인 성공!")
    return redirect(url_for('main.index'))

# 🔓 로그아웃
@login_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('intro.show_intro'))

# ✨ 외부에서 users 사용 가능하게 export
__all__ = ['users']
