class Building:
    def __init__(self, id, name, description, lat, lng):
        self.id = id
        self.name = name
        self.description = description
        self.lat = lat
        self.lng = lng

_buildings = [
    Building("central_library", "중앙도서관", "도서 및 학술 자료 제공", 37.0150, 127.2700),
    Building("humanities_social_science", "인문사회과학관", "인문사회계열 강의 및 연구", 37.0155, 127.2695),
    Building("gymnasium", "체육관", "체육 수업 및 행사 진행", 37.0160, 127.2690),
    Building("agriculture_1", "제1농학관", "농학 관련 강의 및 실습", 37.0165, 127.2685),
    Building("agriculture_2", "제2농학관(축산기술지원센터)", "축산기술 지원 및 연구", 37.0170, 127.2680),
    Building("engineering_2", "제2공학관", "공학계열 강의 및 연구", 37.0175, 127.2675),
    Building("engineering_1", "제1공학관", "공학계열 강의 및 연구", 37.0180, 127.2670),
    Building("engineering_3", "제3공학관", "공학계열 강의 및 연구", 37.0185, 127.2665),
    Building("joint_lab", "공동실험실습관", "실험 및 실습 공간", 37.0190, 127.2660),
    Building("university_headquarters", "대학본부", "행정 업무 및 대학 운영", 37.0195, 127.2655),
    Building("bibong_dormitory", "비봉관", "기숙사 시설", 37.0200, 127.2650),
    Building("narae_dormitory", "나래관", "기숙사 시설", 37.0205, 127.2645),
    Building("hoyeon_dormitory", "호연관", "기숙사 시설", 37.0210, 127.2640),
    Building("changjo_dormitory", "창조관", "기숙사 시설", 37.0215, 127.2635),
    Building("mechanical_engineering", "기계공학관", "기계공학 강의 및 연구", 37.0220, 127.2630),
    Building("student_union", "학생회관", "학생 활동 및 복지 공간", 37.0225, 127.2625),
    Building("future_convergence", "미래융합기술센터", "융합기술 연구 및 개발", 37.0230, 127.2620),
    Building("natural_science", "자연과학관", "자연과학계열 강의 및 연구", 37.0235, 127.2615),
    Building("cultural_complex", "지역문화복합관", "문화 행사 및 지역 교류", 37.0240, 127.2610),
    Building("industry_academic", "산학협력관", "산학 협력 및 창업 지원", 37.0245, 127.2605),
    Building("green_dairy", "그린낙농기술센터", "낙농 기술 연구 및 지원", 37.0250, 127.2600),
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
