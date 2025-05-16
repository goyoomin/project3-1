# main_routes.py
from flask import Blueprint, render_template

main_routes = Blueprint('main', __name__)  # ✅ 이름이 'main'이어야 함

@main_routes.route('/')
def index():  # ✅ 함수 이름이 'index'여야 함
    return render_template('index.html')
