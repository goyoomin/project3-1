from flask import Blueprint, render_template, request, redirect, url_for, flash, session

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 예시: 고정된 ID/PW로 로그인 검사
        if username == 'admin' and password == 'admin':
            session['user'] = username
            flash("✅ 로그인 성공!")
            return redirect(url_for('main.index'))  # 메인 페이지로 이동
        else:
            flash("❌ 로그인 실패. 다시 시도해주세요.")
            return redirect(url_for('login.login'))

    return render_template('login.html')

@login_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("👋 로그아웃 되었습니다.")
    return redirect(url_for('login.login'))
