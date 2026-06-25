# Backend README

## 1. Backend 개요

본 백엔드는 Django REST Framework 기반으로 구현되었습니다.

주요 역할은 다음과 같습니다.

```text
회원 인증
예적금 상품 데이터 저장 및 조회
맞춤 추천 데이터 처리
환율 데이터 저장 및 조회
커뮤니티 게시판 API 제공
지도 / 은행 정보 API 제공
챗봇 요청 처리
```

## 2. 기술 스택

```text
Python
Django
Django REST Framework
SQLite
Token Authentication
Django fixture
requests
openpyxl
```

## 3. 앱 구조

```text
backend/
├── accounts/       # 회원가입, 로그인, 로그아웃, 마이페이지
├── products/       # 예금, 적금 상품 및 금리 옵션
├── exchanges/      # 환율 데이터, 환율 계산, 환율 그래프
├── community/      # 게시글, 댓글, 좋아요
├── maps/           # 은행 지도, 주변 지점
├── chatbot/        # 금융 용어 챗봇
├── config/         # Django 설정
└── manage.py
```

## 4. 설치 및 실행

가상환경 생성:

```bash
python -m venv venv
```

가상환경 실행:

```bash
source venv/Scripts/activate
```

Windows PowerShell:

```bash
.\venv\Scripts\activate
```

패키지 설치:

```bash
pip install -r requirements.txt
```

마이그레이션:

```bash
python manage.py makemigrations
python manage.py migrate
```

서버 실행:

```bash
python manage.py runserver
```

## 5. 환경 변수

`backend/.env` 파일을 생성합니다.

```env
SECRET_KEY=your_django_secret_key
DEBUG=True

FINLIFE_API_KEY=금융감독원_API_KEY
EXCHANGE_API_KEY=한국수출입은행_환율_API_KEY
KAKAO_REST_API_KEY=카카오_REST_API_KEY
OPENAI_API_KEY=AI_API_KEY
```

주의:

```text
실제 API 키는 Git에 커밋하지 않습니다.
.env.example에는 변수명만 작성합니다.
```

## 6. 주요 모델

### accounts

회원 정보를 관리합니다.

주요 기능:

```text
회원가입
로그인
로그아웃
회원 정보 조회
주거래은행 정보 저장
관심상품 관리
```

### products

예금·적금 상품 정보를 관리합니다.

주요 모델:

```text
Bank
FinancialProduct
ProductOption
```

데이터 흐름:

```text
금융감독원 API 호출
→ 은행 정보 저장
→ 상품 기본 정보 저장
→ 상품 금리 옵션 저장
→ 프론트에 DB 데이터 반환
```

### exchanges

환율 정보를 관리합니다.

주요 모델:

```text
ExchangeRate
```

주요 필드:

```text
date
currency_code
normalized_code
currency_name
raw_rate
rate_per_unit
unit
display_unit
source
```

데이터 흐름:

```text
DB에 환율 데이터 있음
→ DB 데이터 반환

DB에 환율 데이터 없음
→ 한국수출입은행 API 호출
→ DB 저장
→ DB 데이터 반환

API 장애 발생
→ fixture 데이터 사용
```

### community

커뮤니티 게시글과 댓글을 관리합니다.

주요 기능:

```text
게시글 목록 조회
게시글 상세 조회
게시글 작성, 수정, 삭제
댓글 작성, 수정, 삭제
좋아요
조회수
```

## 7. Fixture 데이터 로드

### 예적금 상품 fixture

```bash
python manage.py loaddata products/fixtures/products.json
```

### 환율 fixture

```bash
python manage.py loaddata exchanges/fixtures/exchange_rates.json
```

### 커뮤니티 더미데이터

커뮤니티 seed command가 있는 경우:

```bash
python manage.py seed_community --reset
```

## 8. API 사용 방식

### 금융감독원 예적금 API

목적:

```text
정기예금 상품 조회
정기적금 상품 조회
은행별 상품 저장
금리 옵션 저장
```

DB 저장 방식:

```text
API 호출 결과를 그대로 프론트에 넘기지 않고,
Bank / FinancialProduct / ProductOption 모델에 저장한 뒤
DB 데이터를 serializer로 반환합니다.
```

장점:

```text
API 장애 시에도 fixture 데이터로 시연 가능
반복 API 호출 감소
상품 데이터 필터링 및 추천 로직 적용 용이
```

### 한국수출입은행 환율 API

요청 URL:

```text
https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON
```

요청 파라미터:

```text
authkey     API 인증키
searchdate  조회 날짜, YYYYMMDD
data        AP01
```

예시:

```text
https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=API_KEY&searchdate=20260625&data=AP01
```

저장 방식:

```text
API 성공 시 ExchangeRate 모델에 저장
환율 계산과 그래프는 DB 데이터를 기준으로 응답
```

## 9. 주요 API Endpoint 예시

### accounts

```text
POST /api/accounts/signup/
POST /api/accounts/login/
POST /api/accounts/logout/
GET  /api/accounts/mypage/
```

### products

```text
GET /api/products/deposits/
GET /api/products/savings/
GET /api/products/{id}/
```

### exchanges

```text
GET  /api/exchanges/rates/
GET  /api/exchanges/history/
POST /api/exchanges/calculate/
```

### community

```text
GET    /api/community/
POST   /api/community/
GET    /api/community/{id}/
PUT    /api/community/{id}/
DELETE /api/community/{id}/
POST   /api/community/{id}/comments/
POST   /api/community/{id}/like/
```

## 10. 발표 전 백엔드 실행 순서

```bash
cd backend

source venv/Scripts/activate

python manage.py migrate
python manage.py loaddata products/fixtures/products.json
python manage.py loaddata exchanges/fixtures/exchange_rates.json
python manage.py seed_community --reset

python manage.py runserver
```

## 11. 개발 시 주의사항

```text
.env 파일 커밋 금지
db.sqlite3 커밋 여부는 팀 규칙에 맞게 결정
API 키 노출 금지
fixture 파일은 발표 안정성을 위해 최신 상태 유지
마이그레이션 파일 누락 주의
```
