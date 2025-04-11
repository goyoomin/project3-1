from flask import Blueprint, render_template
from app.services.food_service import get_recommended_foods

food_bp = Blueprint('food', __name__, url_prefix='/food')

@food_bp.route('/')
def food_page():
    foods = get_recommended_foods()
    return render_template('food.html', foods=foods)
