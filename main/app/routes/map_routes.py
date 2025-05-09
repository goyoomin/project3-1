from flask import Blueprint, render_template, jsonify, redirect, url_for, request
from main.app.services.map_service import get_buildings, get_building_by_id, get_path_to_building

map_bp = Blueprint('map', __name__, url_prefix='/map')

@map_bp.route('/')
def map_view():
    """지도 메인 페이지"""
    buildings = get_buildings()
    return render_template(
        'map.html',
        buildings=buildings,
        selected_building=None
    )

@map_bp.route('/select/<building_id>')
def select_building(building_id):
    """건물 선택 처리 (AJAX)"""
    building = get_building_by_id(building_id)
    if building:
        return jsonify({
            'success': True,
            'name': building.name,
            'description': building.description
        })
    return jsonify({
        'success': False,
        'message': '해당 건물을 찾을 수 없습니다.'
    })

@map_bp.route('/path/<building_id>')
def path_view(building_id):
    """길찾기 페이지 - 현재는 미구현"""
    return redirect(url_for('map.map_view'))
