# 주연 - 금융생활 시작 가이드

> 사회초년생과 금융 초보자가 예적금 상품, 주거래은행, 환율, 금·은 시세, 커뮤니티를 한 번에 확인하고 비교할 수 있는 금융생활 가이드 서비스입니다.

## 1. 프로젝트 개요

**주연**은 금융을 어렵게 느끼는 사용자가 자신의 조건과 성향에 맞는 금융 상품과 은행을 쉽게 탐색할 수 있도록 돕는 웹 서비스입니다.

사용자는 예금·적금 상품을 한눈에 비교하고, 맞춤 추천을 받을 수 있으며, 주거래은행 테스트를 통해 자신에게 어울리는 은행을 확인할 수 있습니다. 또한 환율 계산, 주요 통화 시세, 금·은 시세, 금융 커뮤니티, 금융 용어 챗봇을 함께 제공하여 금융생활을 시작하는 데 필요한 정보를 통합적으로 제공합니다.

## 2. 주요 기능

### 예적금 상품 조회

금융감독원 API 기반 예금·적금 상품 데이터를 조회하고, DB에 저장된 상품 정보를 기반으로 목록, 필터, 정렬, 상세 정보를 제공합니다.

주요 기능:

* 예금 / 적금 상품 목록 조회
* 은행별, 가입기간별, 가입방식별 필터링
* 기본금리 / 최고금리 비교
* 상품 상세 정보 확인
* 관심상품 등록
* 상품 비교

### 맞춤 상품 추천

사용자의 목적, 예치 방식, 기간, 선호 조건을 바탕으로 적합한 예금·적금 상품을 추천합니다.

주요 기능:

* 예금 / 적금 추천
* 목돈 예치 / 매달 저축 목적 구분
* 선호 은행 및 가입 조건 반영
* 추천 점수 기반 상품 정렬

### 주거래은행 찾기

사용자의 금융 성향과 은행 접근성을 기준으로 주거래은행을 추천합니다.

주요 기능:

* 주거래은행 성향 테스트
* 은행별 특징 비교
* 주변 은행 지점 확인
* 지도 기반 은행 탐색

### 환율 계산 및 주요 통화 시세

한국수출입은행 환율 API를 기반으로 주요 통화 시세를 확인하고, 환율 계산과 기간별 그래프를 제공합니다.

주요 기능:

* 주요 통화 환율 조회
* KRW 기준 환율 계산
* 기간별 환율 추이 그래프
* 전체 통화 목록
* API 장애 대비 fixture 데이터 fallback

### 금·은 시세 확인

금과 은 가격 흐름을 날짜별로 확인할 수 있는 시세 페이지를 제공합니다.

주요 기능:

* 금 시세 조회
* 은 시세 조회
* 날짜별 가격 흐름 확인
* 환율 페이지와 분리된 독립 시세 페이지

### 커뮤니티

사용자들이 금융 관련 고민, 상품 후기, 은행 이용 경험을 공유할 수 있는 게시판입니다.

주요 기능:

* 게시글 목록 조회
* 게시글 작성, 수정, 삭제
* 댓글 작성, 수정, 삭제
* 좋아요 기능
* 비회원 게시글 조회 가능
* 로그인 사용자만 글쓰기, 댓글, 좋아요 가능

### 금융 용어 챗봇

예금, 적금, 금리, 환율 등 금융 용어를 쉽게 설명해주는 챗봇입니다.

주요 기능:

* 금융 용어 설명
* 추천 질문 제공
* 로그인 사용자만 이용 가능

## 3. 기술 스택

### Backend

* Python
* Django
* Django REST Framework
* SQLite
* Token Authentication
* Django fixture

### Frontend

* Vue 3
* Vite
* Vue Router
* Axios
* Chart.js

### External API

* 금융감독원 예적금 상품 API
* 한국수출입은행 환율 API
* 지도 API
* AI / 챗봇 API

## 4. 프로젝트 구조

```text
13-pjt/
├── backend/
│   ├── accounts/
│   ├── products/
│   ├── exchanges/
│   ├── community/
│   ├── maps/
│   ├── chatbot/
│   ├── config/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── router/
│   │   ├── views/
│   │   └── App.vue
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 5. 실행 방법

### 5-1. Backend 실행

```bash
cd backend

python -m venv venv
source venv/Scripts/activate

pip install -r requirements.txt
```

Windows PowerShell을 사용하는 경우:

```bash
.\venv\Scripts\activate
```

DB 마이그레이션:

```bash
python manage.py makemigrations
python manage.py migrate
```

fixture 데이터 로드:

```bash
python manage.py loaddata products/fixtures/products.json
python manage.py loaddata exchanges/fixtures/exchange_rates.json
```

커뮤니티 더미데이터를 사용하는 경우:

```bash
python manage.py seed_community --reset
```

서버 실행:

```bash
python manage.py runserver
```

기본 서버 주소:

```text
http://127.0.0.1:8000/
```

### 5-2. Frontend 실행

```bash
cd frontend

npm install
npm run dev
```

기본 프론트 주소:

```text
http://localhost:5173/
```

## 6. 환경 변수 설정

백엔드에서 외부 API를 사용하기 위해 `.env` 파일을 생성해야 합니다.

예시:

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
.env 파일은 절대 Git에 커밋하지 않습니다.
.env.example 파일에는 변수명만 남기고 실제 키 값은 작성하지 않습니다.
```

## 7. API 사용 방식

### 예적금 상품 API

예적금 상품 데이터는 금융감독원 API를 통해 가져옵니다.

서비스 흐름:

```text
금융감독원 API 호출
→ Bank / FinancialProduct / ProductOption 모델에 저장
→ 이후 프론트에서는 DB에 저장된 상품 데이터 조회
```

API가 불안정하거나 네트워크 문제가 발생할 경우를 대비해 `products/fixtures/products.json` fixture 파일을 제공합니다.

fixture 로드:

```bash
python manage.py loaddata products/fixtures/products.json
```

### 환율 API

환율 데이터는 한국수출입은행 API를 통해 가져옵니다.

현재 요청 URL:

```text
https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON
```

서비스 흐름:

```text
DB에 환율 데이터 있음
→ DB 데이터 반환

DB에 환율 데이터 없음
→ 한국수출입은행 API 호출
→ ExchangeRate 모델에 저장
→ DB 데이터 반환

API 장애 발생
→ fixture 데이터 사용
```

환율 fixture 로드:

```bash
python manage.py loaddata exchanges/fixtures/exchange_rates.json
```

환율 fixture는 API 장애 시에도 환율 계산, 주요 통화 시세, 환율 그래프가 동작하도록 하기 위한 시연 안정화 데이터입니다.

### 지도 API

주변 은행 지점 확인과 지도 기능을 위해 지도 API를 사용합니다.

사용 목적:

* 사용자의 위치 기반 은행 탐색
* 주변 지점 표시
* 지도 / 거리뷰 기능 제공

### 챗봇 API

금융 용어를 쉽게 설명하기 위해 AI API를 사용합니다.

사용 목적:

* 금융 용어 설명
* 예금, 적금, 금리, 환율 등 기초 금융 개념 안내
* 사용자의 질문에 대한 쉬운 답변 제공

## 8. Fixture 데이터 관리

프로젝트에서는 외부 API 장애에 대비해 fixture 데이터를 사용합니다.

### 상품 fixture

```text
backend/products/fixtures/products.json
```

로드 명령어:

```bash
python manage.py loaddata products/fixtures/products.json
```

### 환율 fixture

```text
backend/exchanges/fixtures/exchange_rates.json
```

로드 명령어:

```bash
python manage.py loaddata exchanges/fixtures/exchange_rates.json
```

### 발표 전 권장 실행 순서

```bash
cd backend

python manage.py migrate
python manage.py loaddata products/fixtures/products.json
python manage.py loaddata exchanges/fixtures/exchange_rates.json
python manage.py seed_community --reset
python manage.py runserver
```

프론트:

```bash
cd frontend
npm install
npm run dev
```

## 9. 인증 정책

로그인하지 않은 사용자는 일부 기능을 제한합니다.

비회원 가능:

* 메인 페이지 조회
* 예적금 상품 목록 조회
* 예적금 상품 상세 조회
* 환율 조회
* 금·은 시세 조회
* 커뮤니티 게시글 조회

로그인 필요:

* 맞춤 추천
* 주거래은행 찾기
* 마이페이지
* 관심상품 등록
* 상품 비교
* 커뮤니티 글쓰기
* 댓글 작성
* 좋아요
* 챗봇 사용

로그인이 필요한 기능에 접근하면 공통 안내 메시지를 보여주고, 필요한 경우 로그인 페이지로 이동합니다.

## 10. 팀 프로젝트 의의

이 프로젝트는 단순히 예적금 상품을 나열하는 서비스가 아니라, 사회초년생이 금융생활을 시작할 때 필요한 정보를 하나의 흐름으로 연결하는 데 초점을 두었습니다.

사용자는 상품 조회에서 끝나는 것이 아니라, 자신의 조건에 맞는 상품을 추천받고, 주거래은행을 찾고, 환율과 금·은 시세를 확인하며, 커뮤니티와 챗봇을 통해 금융 정보를 쉽게 이해할 수 있습니다.
