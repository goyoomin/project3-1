from flask import Flask
from app.routes.todolist_routes import todolist_bp
from app.routes.food_routes import food_bp
from app.routes.map_routes import map_bp
from app.routes.timetable_routes import timetable_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "비밀키12345"  # ✅ 여기에 추가!

    # 블루프린트 등록
    app.register_blueprint(todolist_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(timetable_bp)

    return app
