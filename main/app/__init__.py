from flask import Flask
from main.app.routes.todolist_routes import todolist_bp
from main.app.routes.food_routes import food_bp
from main.app.routes.map_routes import map_bp
from main.app.routes.timetable_routes import timetable_bp
from main.app.routes.login_routes import login_bp
from main.app.routes.intro_routes import intro_bp

def create_app():
    app = Flask(
        __name__,
        template_folder='main/app/templates',
        static_folder='main/app/static'
    )
    app.secret_key = "비밀키12345"  # Flash와 Session 사용을 위해 필요

    # 블루프린트 등록
    app.register_blueprint(todolist_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(timetable_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(intro_bp)

    return app
