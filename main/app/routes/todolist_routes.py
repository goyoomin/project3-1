# 예시 (이렇게 되어 있어야 함)
from flask import Blueprint

todolist_bp = Blueprint('todolist', __name__, url_prefix='/todolist')

@todolist_bp.route('/')
def todolist_main():
    return '할 일 목록 메인 페이지입니다.'
