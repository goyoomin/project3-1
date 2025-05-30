# app/routes/map_routes.py

from flask import Blueprint, render_template
from main.app.services.map_service import buildings

map_bp = Blueprint('map', __name__, url_prefix='/map')

@map_bp.route('/')
def show_map():
    return render_template('map.html', buildings=buildings)