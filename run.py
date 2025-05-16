from flask import Flask
from main.app.routes.main_routes import main_routes
from main.app.routes.map_routes import map_bp
from main.app.routes.food_routes import food_bp
from main.app.routes.timetable_routes import timetable_bp
from main.app.routes.todolist_routes import todolist_bp
from main.app.routes.login_routes import login_bp
from main.app.routes.intro_routes import intro_bp
from main.app.routes import user_bp  # ✅ 반드시 routes/__init__.py에 export 되어야 함
from main.app.routes.notice_routes import notice_bp

def create_app():
    app = Flask(
        __name__,
        template_folder='main/app/templates',
        static_folder='main/app/static'
    )
    app.secret_key = "비밀키12345"

    app.register_blueprint(main_routes)
    app.register_blueprint(map_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(timetable_bp)
    app.register_blueprint(todolist_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(intro_bp)
    app.register_blueprint(user_bp, url_prefix='/user')  # ✅ 경로: /user/settings 등
    app.register_blueprint(notice_bp, url_prefix='/notice')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
