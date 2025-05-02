from flask import Blueprint, render_template

food_routes = Blueprint('food', __name__, url_prefix='/food')

@food_routes.route('/')
def food_view():
    # 식당 페이지 렌더링
    return render_template('food.html')