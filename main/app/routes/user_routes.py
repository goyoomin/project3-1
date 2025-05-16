from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__)  # 🔴 이름이 'user'여야 함

@user_bp.route('/settings')
def settings():
    return render_template('settings.html')
