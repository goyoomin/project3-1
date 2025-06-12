# main/app/routes/notice_routes.py

from flask import Blueprint, render_template

notice_bp = Blueprint('notice', __name__, url_prefix='/notice')

@notice_bp.route('/')
def index():
    return render_template('notice.html')  # 새 템플릿 만들기
