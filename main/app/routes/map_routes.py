from flask import Blueprint, render_template
from app.services.map_service import get_location_data

map_bp = Blueprint('map', __name__, url_prefix='/map')

@map_bp.route('/')
def map_page():
    location = get_location_data()
    return render_template('map.html', location=location)