# app/routes/map_routes.py

from flask import Blueprint, render_template, jsonify
from main.app.services import map_service
import requests

map_bp = Blueprint('map', __name__, url_prefix='/map')

TMAP_APPKEY = "huDKZfBQb69NgmfdrrN2N1uJIZZCkcgp4wAvgPHD"

@map_bp.route('/')
def show_map():
    return render_template('map.html', buildings=map_service.buildings)

@map_bp.route('/buildings')
def get_buildings():
    return jsonify(map_service.get_buildings_with_center())

@map_bp.route('/path/<int:start_id>/<int:end_id>')
def get_path(start_id, end_id):
    buildings = map_service.get_buildings_with_center()
    start = next((b for b in buildings if b['id'] == start_id), None)
    end = next((b for b in buildings if b['id'] == end_id), None)
    if not start or not end:
        return jsonify({'steps': [], 'path': [], 'message': '출발지 또는 도착지 정보가 없습니다.'})

    url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1"
    headers = {
        "appKey": TMAP_APPKEY,
        "Content-Type": "application/json"
    }
    
    body = {
        "startX": start['lng'],
        "startY": start['lat'],
        "endX": end['lng'],
        "endY": end['lat'],
        "reqCoordType": "WGS84GEO",
        "resCoordType": "WGS84GEO",
        "startName": start['name'],
        "endName": end['name'],
        "searchOption": "0"   # ★ 최단거리(거리 기준)
    }
    try:
        res = requests.post(url, headers=headers, json=body, timeout=6)
        result = res.json()
        print("Tmap 요청 정보:", body)
        print("Tmap 응답 결과:", result)
        path = []
        if 'features' not in result or not result['features']:
            return jsonify({'steps': [], 'path': [], 'message': '경로를 찾을 수 없습니다. (Tmap에 도보 네트워크가 없음)'})
        for feature in result.get('features', []):
            if feature['geometry']['type'] == "LineString":
                for lon, lat in feature['geometry']['coordinates']:
                    path.append({'lat': lat, 'lng': lon})
        if not path:
            return jsonify({'steps': [], 'path': [], 'message': '경로 데이터가 비어 있습니다.'})
        return jsonify({'steps': [], 'path': path, 'message': 'ok'})
    except Exception as e:
        print("Tmap 길찾기 에러:", e)
        return jsonify({'steps': [], 'path': [], 'message': f"Tmap 요청 실패: {str(e)}"})
