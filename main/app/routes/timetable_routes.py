# 올바르게 되어 있어야 할 예시
from flask import Blueprint

timetable_bp = Blueprint('timetable', __name__, url_prefix='/timetable')

@timetable_bp.route('/')
def timetable_main():
    return '시간표 메인 페이지입니다.'
