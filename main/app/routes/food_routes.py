from flask import Blueprint, render_template

food_routes = Blueprint('food', __name__, url_prefix='/food')

@food_routes.route('/')
def index():
    return render_template('food.html')
