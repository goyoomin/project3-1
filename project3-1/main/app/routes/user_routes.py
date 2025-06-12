from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from main.app.routes.login_routes import users  # 🔄 상대경로에 맞게 수정

user_bp = Blueprint('user', __name__, url_prefix='/user')

# 설정 페이지
@user_bp.route('/settings')
def settings():
    return render_template('settings.html')

# 사용자 정보 업데이트
@user_bp.route('/settings/update-profile', methods=['POST'])
def update_profile():
    name = request.form.get('name')
    email = request.form.get('email')
    student_id = request.form.get('student_id')
    department = request.form.get('department')

    session['name'] = name
    session['email'] = email
    session['student_id'] = student_id
    session['department'] = department

    flash("✅ 사용자 정보가 업데이트되었습니다.")
    return redirect(url_for('user.settings'))

# 비밀번호 변경
@user_bp.route('/settings/change-password', methods=['POST'])
def change_password():
    current = request.form.get('current_password')
    new = request.form.get('new_password')
    confirm = request.form.get('confirm_password')

    user = session.get('user')

    if user not in users:
        flash("⚠️ 사용자 정보를 찾을 수 없습니다.")
        return redirect(url_for('user.settings'))

    if not check_password_hash(users[user]['password'], current):
        # ❗ 잘못된 현재 비밀번호인 경우 쿼리 파라미터로 전달
        return redirect(url_for('user.settings') + '?pwerror=1')

    if new != confirm:
        flash("❗ 새 비밀번호가 일치하지 않습니다.")
        return redirect(url_for('user.settings'))

    users[user]['password'] = generate_password_hash(new)
    flash("✅ 비밀번호가 변경되었습니다.")
    return redirect(url_for('user.settings'))

# 테마 변경
@user_bp.route('/settings/theme', methods=['POST'])
def change_theme():
    theme = request.form.get('theme')
    if theme in ['light', 'dark']:
        session['theme'] = theme
        flash(f"🎨 테마가 '{theme}' 모드로 변경되었습니다.")
    else:
        flash("❗ 유효하지 않은 테마입니다.")
    return redirect(url_for('user.settings'))
