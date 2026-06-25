# Frontend README

## 1. Frontend 개요

본 프론트엔드는 Vue 3와 Vite를 기반으로 구현되었습니다.

사용자는 프론트 화면을 통해 예적금 상품 조회, 맞춤 추천, 주거래은행 찾기, 환율 계산, 금·은 시세 확인, 커뮤니티, 챗봇 기능을 이용할 수 있습니다.

## 2. 기술 스택

```text
Vue 3
Vite
Vue Router
Axios
Chart.js
JavaScript
CSS
```

## 3. 프로젝트 구조

```text
frontend/
├── src/
│   ├── api/             # axios API 요청 모듈
│   ├── assets/          # 이미지, 로고, 캐릭터
│   ├── components/      # 공통 컴포넌트
│   ├── router/          # Vue Router 설정
│   ├── utils/           # 공통 유틸 함수
│   ├── views/           # 페이지 단위 컴포넌트
│   ├── App.vue
│   └── main.js
│
├── package.json
└── vite.config.js
```

## 4. 설치 및 실행

패키지 설치:

```bash
npm install
```

개발 서버 실행:

```bash
npm run dev
```

기본 주소:

```text
http://localhost:5173/
```

빌드:

```bash
npm run build
```

## 5. 주요 화면

### HomeView

서비스의 메인 페이지입니다.

주요 구성:

```text
서비스 소개
기능 요약 슬라이더
맞춤추천 / 주거래은행 / 환율·금은 / 커뮤니티 바로가기
주연 캐릭터 이미지
```

### ProductListView

예금·적금 상품을 한눈에 볼 수 있는 페이지입니다.

주요 기능:

```text
전체 / 예금 / 적금 탭
은행 필터
가입 기간 필터
금리 범위 필터
가입 방식 필터
우대조건 필터
상품 검색
상품 비교
관심상품 등록
페이지네이션
```

### ProductDetailView

상품 상세 페이지입니다.

주요 기능:

```text
상품 기본 정보
금리 옵션
가입 정보
공시 정보
관심상품 등록
```

### RecommendView

로그인 사용자를 대상으로 맞춤 상품 추천을 제공합니다.

주요 기능:

```text
추천 조건 입력
추천 상품 유형 선택
사용자 조건 기반 상품 추천
추천 결과 조회
```

### MainBankView

주거래은행 찾기 페이지입니다.

주요 기능:

```text
금융 성향 테스트
주거래은행 추천
은행별 특징 확인
주변 은행 지점 확인
지도 기반 탐색
```

### ExchangeView

환율 계산 및 주요 통화 시세 페이지입니다.

주요 기능:

```text
KRW 기준 환율 계산
주요 통화 시세 조회
전체 통화 목록
기간별 환율 그래프
오늘의 환율 요약
```

### SpotAssetView

금·은 시세 확인 페이지입니다.

주요 기능:

```text
금 시세 확인
은 시세 확인
날짜별 가격 추이
```

### CommunityView

금융 커뮤니티 게시판입니다.

주요 기능:

```text
게시글 목록
게시글 상세
게시글 작성
댓글 작성
좋아요
검색
비회원 조회
```

### MyPageView

로그인 사용자의 개인 페이지입니다.

주요 기능:

```text
회원 정보 조회
관심 상품 조회
내가 작성한 게시글 확인
```

## 6. 라우터 구조

```text
/                 홈
/products         예적금 상품 목록
/products/:id     상품 상세
/recommend        맞춤 추천
/exchange         환율
/spot-assets      금·은 시세
/main-bank        주거래은행 찾기
/map              주변 은행 지도
/community        커뮤니티
/mypage           마이페이지
/login            로그인
/signup           회원가입
/find-username    아이디 찾기
/reset-password   비밀번호 재설정
```

## 7. 인증 처리

로그인 여부는 `localStorage`의 token 값을 기준으로 판단합니다.

로그인이 필요한 페이지:

```text
/recommend
/main-bank
/map
/mypage
```

로그인이 필요한 페이지에 비회원이 접근하면 공통 로그인 안내 메시지를 보여주고 로그인 페이지로 이동합니다.

커뮤니티는 게시글 조회는 비회원도 가능하지만, 아래 기능은 로그인 사용자만 이용할 수 있습니다.

```text
게시글 작성
댓글 작성
좋아요
```

챗봇은 로그인 사용자만 사용할 수 있으며, 비회원이 클릭하면 챗봇 아이콘 위에 안내 문구를 표시합니다.

## 8. API 요청 구조

프론트의 API 요청은 `src/api/` 폴더에서 관리합니다.

예시 구조:

```text
src/api/
├── api.js              # axios 기본 인스턴스
├── accounts.js         # 회원 API
├── products.js         # 상품 API
├── exchanges.js        # 환율 API
├── community.js        # 커뮤니티 API
├── recommendations.js  # 추천 API
└── maps.js             # 지도 API
```

Axios 기본 흐름:

```text
프론트 요청
→ axios instance
→ Django REST API
→ 응답 데이터 화면 렌더링
```

인증이 필요한 요청에는 token을 Authorization header에 담아 보냅니다.

```text
Authorization: Token {token}
```

## 9. 공통 UI

### NavBar

상단 네비게이션 컴포넌트입니다.

로그아웃 상태:

```text
로그인
회원가입
```

로그인 상태:

```text
내 정보
로그아웃
```

### AuthNotice

로그인이 필요한 기능에 접근했을 때 보여주는 공통 안내 메시지입니다.

사용 목적:

```text
브라우저 기본 alert 제거
상단 중앙 안내 메시지 통일
로그인 필요 기능 안내
```

### ChatbotFloatingButton

우측 하단 챗봇 플로팅 버튼입니다.

로그인 상태:

```text
챗봇 창 열림
```

로그아웃 상태:

```text
챗봇 아이콘 위에 로그인 안내 문구 표시
```

## 10. 발표 전 프론트 확인 순서

```bash
cd frontend

npm install
npm run dev
```

확인할 페이지:

```text
/
 /products
 /recommend
 /main-bank
 /exchange
 /spot-assets
 /community
 /login
 /signup
```

확인할 기능:

```text
로그인 / 로그아웃
회원가입 후 자동 로그인
예적금 상품 목록
상품 상세
관심상품
맞춤 추천
주거래은행 찾기
환율 계산
환율 그래프
금·은 시세
커뮤니티 글쓰기 / 댓글 / 좋아요
챗봇 로그인 제한
```

## 11. 개발 시 주의사항

```text
API_BASE_URL 확인
백엔드 서버 실행 상태 확인
localStorage token 상태 확인
브라우저 캐시 문제 발생 시 Ctrl + Shift + R
이미지 파일 경로 확인
라우터 name과 path 불일치 주의
```
