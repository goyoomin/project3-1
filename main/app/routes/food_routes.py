# main/app/routes/food_routes.py

from flask import Blueprint, render_template

food_bp = Blueprint('food', __name__, url_prefix='/food')

@food_bp.route('/')
def food_view():
    return render_template('food.html')
