# 전체 서비스 아키텍처

본 서비스는 Vue 3 기반의 프론트엔드와 Django REST Framework 기반의 백엔드 서버를 중심으로 구성된다.  
사용자는 프론트엔드 화면을 통해 회원가입, 로그인, 예적금 상품 조회, 관심상품 등록, 상품 추천, 커뮤니티, 환율 계산, 지도 검색, 챗봇 기능을 이용한다.

프론트엔드는 Axios를 통해 백엔드 API 서버와 통신하며, 백엔드 서버는 회원 정보, 상품 정보, 관심상품, 커뮤니티, 저장 영상, 추천 이력 등의 데이터를 데이터베이스에 저장하고 관리한다.  
또한 금융감독원 예적금 상품 API, 수출입은행 환율 API, 카카오 지도 API, YouTube API, AI 챗봇 API 등 외부 서비스를 연동하여 사용자에게 필요한 정보를 제공한다.

## 아키텍처 구성

- Frontend
  - Vue 3
  - Vite
  - Vue Router
  - Axios
  - Pinia 또는 상태 관리 로직

- Backend
  - Django
  - Django REST Framework
  - JWT 기반 인증
  - ORM 기반 데이터 처리

- Database
  - SQLite 또는 MySQL
  - 회원, 금융상품, 관심상품, 추천 이력, 커뮤니티, 저장 영상 데이터 저장

- External API
  - 금융감독원 API: 예금/적금 상품 데이터 수집
  - 수출입은행 API: 환율 정보 조회
  - 카카오 지도 API: 은행 및 주변 위치 검색
  - YouTube API: 금융 관련 영상 검색 및 저장
  - AI API: 금융상품 설명 및 금융용어 풀이 챗봇 응답 생성