# Campick: 사용자 맞춤형 학사 정보 통합 앱

시간표, 공지, 할 일, 학식, 지도 등 대학 생활 전반의 정보를  
한 곳에서 관리하고 AI 추천으로 효율적인 학습을 지원하는 통합 플랫폼

---

## 홈 화면 구성

| 기능 | 설명 |
|------|------|
| 🗺️ 지도 | 건물 정보 표시, 출발·도착 선택 후 도보 길찾기 경로 시각화 | 
| 🍱 학식 | 기식 / 학식 / 맛집 탭 메뉴 제공 |
| 🗓️ 시간표 | 수업 등록, 시간표 UI 표시, AI 기반 학습 계획 추천 (Cohere) |
| ✅ 할일 | 플래너 & 일정 완료율 확인 |

---

## MSA 아키텍처 요약

| 서비스명 | 주요 역할 | DB | 외부 연계 | 비고 |
|----------|-----------|----|-----------|------|
| 🔐 Auth | 로그인, JWT 토큰 | ✅ | 모든 서비스 | 인증 공통 처리 |
| 📝 Registration | 회원가입, 계정 생성 | ✅ | Auth, Profile | 가입 시 프로필 초기화 |
| 👤 Profile | 사용자 정보 (이름, 신체 등) | ✅ | AI, Auth | Cohere 추천에 활용 |
| 📆 TodoList | 일정, 할 일, 통계 | ✅ | AI, Storage | 완료율 계산 포함 |
| 🗓️ Timetable | 시간표 등록 및 UI 렌더링, AI 추천 트리거 | ✅ | AI(Cohere) | redraw(), GPT 버튼 통한 학습 계획 요청 |
| 🤖 AI | Cohere 기반 일정/학습 추천 | ❌ | Cohere API, Planning, Profile | GPT → Cohere |
| 🍱 Meal | 기식/학식/맛집 정보 제공 | ✅ | 학교 웹 크롤링, 지역 API | UI에서 탭 구분 제공 |
| 🗺️ Map | 건물 정보 표시 및 출발-도착 기반 경로 시각화 | ✅ | 지도 API (Kakao, Tmap) | 도보 길찾기 연동 |
| 🏠 Main | 홈 UI, 진입 라우터 | ❌ | 모든 서비스 | SPA 구성 (버튼 UI 등)

---

## 사용자 흐름 예시
### 학식/맛집 조회

```
‘학식’ 버튼 선택
기식 / 학식 / 맛집 탭 선택
식당별 메뉴 표시
```

### 지도 기능

```
'지도' 버튼 클릭
'출발지', '도착지' 건물 선택
'길찾기' 버튼 클릭
도보 경로 시각화
```

### 할 일 기능

```
‘할일’ 버튼 클릭
일정 추가 / 완료 체크
캘린더에 일정 표시
```

### 시간표 기능

```
‘시간표’ 버튼 클릭
수업 추가
시간표 시각화
```

### 학습 추천 (Cohere)

```
‘GPT 추천’ 버튼 클릭
시간표 및 할 일 분석
학습 계획 5개 생성
플래너에 자동 등록
```

### 로그인 / 로그아웃

```
‘체험하기’ 버튼 클릭
로그인 없이 사용

‘로그인’ 버튼 클릭
인증 완료 후 메인 진입

‘로그아웃’ 버튼 클릭
세션 종료
```

---

## 특징

- 모바일 UI 최적화 (버튼 기반 홈 + 하단 네비게이션)
- MSA 구조 기반 서비스 분리 및 독립 배포
- Cohere 기반 AI 추천 도입 (GPT 대체)
- FullCalendar 기반 시간표 UI 갱신
- Tmap API 기반 실시간 도보 경로 안내

---

## 기술 스택

- Python, Flask, Cohere API, HTML/CSS, JavaScript
- Jinja2, Feather Icons, FullCalendar, JSON
- RESTful API, Session, JWT, Blueprint
- Docker, GitHub, .env
- 크롤링: requests, BeautifulSoup
- 지도: Kakao Maps SDK, Tmap API (도보 길찾기)

---

## 팀원

| 이름 | 역할 |
|------|------|
| 고유민 | 팀장, To-Do List, 홈, 로그인 기능 |
| 김세림 | 시간표 기능 |
| 이민우 | 지도 기능 |
| 임현지 | 학식 기식 맛집 기능 |

---

## 시연 영상

(https://youtube.com/shorts/S0WYMJdQDq0)]()]](https://youtube.com/shorts/S0WYMJdQDq0)

---
