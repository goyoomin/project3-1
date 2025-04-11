from flask import Flask
from main.todolist.todolist_web import todolist_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(todolist_bp)

if __name__ == "__main__":
    app.run(debug=True)
