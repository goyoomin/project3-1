from flask import Flask
from main.app.routes.main_routes import main_routes
from main.app.routes.map_routes import map_bp
from main.app.routes.food_routes import food_bp
from main.app.routes.timetable_routes import timetable_bp
from main.app.routes.todolist_routes import todolist_bp
from main.app.routes.login_routes import login_bp
from main.app.routes.intro_routes import intro_bp
from main.app.routes.user_routes import user_bp
from main.app.routes.notice_routes import notice_bp

from datetime import datetime, timedelta

def create_app():
    app = Flask(
        __name__,
        template_folder='main/app/templates',
        static_folder='main/app/static'
    )
    app.secret_key = "비밀키12345"

    @app.context_processor
    def inject_datetime_utils():
        return dict(datetime=datetime, timedelta=timedelta)

    app.register_blueprint(main_routes)
    app.register_blueprint(map_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(timetable_bp)
    app.register_blueprint(todolist_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(intro_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(notice_bp)

    return app
