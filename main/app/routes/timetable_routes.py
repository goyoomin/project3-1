from flask import Blueprint, render_template

timetable_bp = Blueprint('timetable', __name__, url_prefix='/timetable')

@timetable_bp.route("/")
def index():
    return render_template("timetable.html")
