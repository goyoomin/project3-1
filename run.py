from flask import Flask
from main.app.routes.main_routes import main_routes
from main.app.routes.map_routes import map_bp
from main.app.routes.food_routes import food_bp
from main.app.routes.timetable_routes import timetable_bp
from main.app.routes.todolist_routes import todolist_bp
from main.app.routes.login_routes import login_bp
from main.app.routes.intro_routes import intro_bp  # ✅ intro 라우터 import 추가

def create_app():
    app = Flask(
        __name__,
        template_folder='main/app/templates',
        static_folder='main/app/static'
    )
    app.secret_key = "비밀키12345"  # ✅ 세션, flash 사용을 위해 꼭 필요!

    # 🔹 블루프린트 등록
    app.register_blueprint(main_routes)
    app.register_blueprint(map_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(timetable_bp)
    app.register_blueprint(todolist_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(intro_bp)  # ✅ intro_bp 등록

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
