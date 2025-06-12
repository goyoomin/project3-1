# main/app/routes/food_routes.py
from flask import Blueprint, render_template

food_bp = Blueprint('food', __name__, url_prefix='/food')

@food_bp.route('/')
def index():  # ← 이 함수명이 'index'여야 함
    return render_template('food.html')
