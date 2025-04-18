class Building:
    def __init__(self, id, name, description, lat, lng):
        self.id = id
        self.name = name
        self.description = description
        self.lat = lat
        self.lng = lng

_buildings = [
    Building("student_union", "학생회관", "어깨구름터 위치, 학생활동 및 식당, 카페 위치", 37.0157, 127.2701),
    Building("academic_1", "1공학관", "전자공학과, 기계공학과 등...", 37.0165, 127.2710),
    Building("academic_2", "2공학관", "컴퓨터공학과, 소프트웨어융합학과...", 37.0170, 127.2705),
    Building("humanities", "인문사회관", "인문대학 및 사회과학대학 강의실 및 연구실", 37.0155, 127.2695),
    Building("cultural", "지역문화복합관", "지역문화연구소 및 문화예술 관련 시설", 37.0162, 127.2690),
    Building("future_tech", "미래융합기술센터", "첨단 기술 연구 및 산학협력 공간", 37.0175, 127.2715),
]

def get_buildings():
    return _buildings

def get_building_by_id(building_id):
    for b in _buildings:
        if b.id == building_id:
            return b
    return None

def get_path_to_building(current_location, target_building):
    if not target_building:
        return {
            'distance': '0m',
            'duration': '알 수 없음',
            'steps': [{'instruction': '건물이 존재하지 않습니다.', 'distance': '0m'}]
        }
    return {
        'distance': '약 300m',
        'duration': '약 5분',
        'steps': [
            {'instruction': '동쪽으로 100m 이동', 'distance': '100m'},
            {'instruction': '횡단보도 건너 북쪽으로 100m 이동', 'distance': '100m'},
            {'instruction': f'{target_building.name} 정문까지 100m 더 이동', 'distance': '100m'}
        ]
    }
