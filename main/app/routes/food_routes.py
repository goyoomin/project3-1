from flask import Blueprint, render_template

food_bp = Blueprint('food', __name__, url_prefix='/food')

@food_bp.route('/')
def show_food():
    return render_template('food.html')
