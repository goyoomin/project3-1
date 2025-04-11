# app/routes/timetable_routes.py

from flask import Blueprint, render_template

timetable_bp = Blueprint('timetable', __name__, url_prefix='/timetable')

@timetable_bp.route('/')
def show_timetable():
    return render_template('timetable.html')
