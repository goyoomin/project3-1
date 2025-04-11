
import json
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# JSON 파일에서 학식 데이터 불러오기
def load_menu():
    with open('food_menu.json', 'r', encoding='utf-8') as file:
        return json.load(file)  # JSON 파일을 파이썬 딕셔너리로 변환

# API 엔드포인트: JSON 형식으로 학식 데이터 제공
@app.route('/api/menu')
def get_menu():
    food_menu = load_menu()  # JSON 파일을 불러와 사용
    return jsonify(food_menu)

# 웹페이지 렌더링
@app.route('/')
def index():
    food_menu = load_menu()  # JSON 파일을 불러와 사용
    return render_template('index.html', menu=food_menu)

if __name__ == '__main__':
    app.run(debug=True)
