# API 명세서

본 문서는 예적금 추천 서비스의 백엔드 API 명세를 정리한 문서이다.
API는 Django REST Framework 기반으로 구현하며, 프론트엔드는 Vue에서 API를 호출하여 화면을 구성한다.

## 1. API 설계 기준

* Base URL: `/api/`
* 인증 방식: Token 기반 인증
* 요청 및 응답 형식: JSON
* 로그인한 사용자만 이용 가능한 기능은 `Authorization` Header에 Token을 포함한다.

```http
Authorization: Token {token}
```

> 현재 프론트 연결 기준은 `http://127.0.0.1:8000/api`이다.
> 프론트엔드 `src/api/api.js`에서 공통 baseURL을 설정하고, 로그인 후 발급받은 token을 요청 Header에 포함한다.

---

## 2. 공통 응답 형식

본 프로젝트의 API 응답은 기능별로 다음 두 가지 형태가 혼합되어 사용된다.

### 메시지 포함 응답

```json
{
  "message": "처리 결과 메시지"
}
```

### 데이터 직접 반환 응답

```json
[
  {
    "id": 1,
    "name": "상품명"
  }
]
```

### 챗봇 성공 응답

```json
{
  "success": true,
  "data": {
    "type": "llm",
    "question": "예금이 뭐야?",
    "answer": "예금은..."
  }
}
```

### 챗봇 실패 응답

```json
{
  "success": false,
  "message": "질문을 입력해주세요."
}
```

---

## 3. API 목록

| 구분   | Method | URL                                      | 설명                | 인증 |
| ---- | ------ | ---------------------------------------- | ----------------- | -- |
| 회원   | POST   | `/accounts/signup/`                      | 회원가입              | X  |
| 회원   | POST   | `/accounts/login/`                       | 로그인               | X  |
| 회원   | POST   | `/accounts/logout/`                      | 로그아웃              | O  |
| 회원   | POST   | `/accounts/find-username/`               | 아이디 찾기            | X  |
| 회원   | POST   | `/accounts/reset-password/`              | 비밀번호 재설정          | X  |
| 회원   | POST   | `/accounts/password/change/`             | 비밀번호 변경           | O  |
| 회원   | DELETE | `/accounts/withdraw/`                    | 회원탈퇴              | O  |
| 회원   | GET    | `/accounts/profile/`                     | 내 프로필 조회          | O  |
| 회원   | PATCH  | `/accounts/profile/update/`              | 내 프로필 수정          | O  |
| 회원   | GET    | `/accounts/profile/options/`             | 프로필 선택지 조회        | X  |
| 상품   | GET    | `/products/deposits/save/`               | 정기예금 상품 DB 저장     | X  |
| 상품   | GET    | `/products/deposits/`                    | 정기예금 상품 목록 조회     | X  |
| 상품   | GET    | `/products/deposits/{product_id}/`       | 정기예금 상품 상세 조회     | X  |
| 상품   | GET    | `/products/savings/save/`                | 적금 상품 DB 저장       | X  |
| 상품   | GET    | `/products/savings/`                     | 적금 상품 목록 조회       | X  |
| 상품   | GET    | `/products/savings/{product_id}/`        | 적금 상품 상세 조회       | X  |
| 관심상품 | GET    | `/favorites/`                            | 관심 상품 목록 조회       | O  |
| 관심상품 | POST   | `/favorites/{product_id}/`               | 관심 상품 등록/삭제 토글    | O  |
| 추천   | POST   | `/recommendations/products/`             | 예적금 상품 추천         | O  |
| 추천   | POST   | `/recommendations/main-bank/`            | 주거래은행 추천 결과 생성    | O  |
| 추천   | GET    | `/recommendations/history/`              | 주거래은행 추천 이력 조회    | O  |
| 환율   | GET    | `/exchanges/rates/`                      | 환율 목록 조회          | X  |
| 환율   | GET    | `/exchanges/history/`                    | 환율 기간별 히스토리 조회    | X  |
| 환율   | POST   | `/exchanges/calculate/`                  | 환율 계산             | X  |
| 지도   | GET    | `/maps/banks/`                           | 현재 위치 기준 은행 검색    | X  |
| 지도   | GET    | `/maps/routes/`                          | 은행까지 경로 검색        | X  |
| 챗봇   | POST   | `/chatbot/explain/`                      | 금융상품 및 금융용어 설명 요청 | X  |
| 게시판  | GET    | `/community/`                            | 게시글 목록 조회         | X  |
| 게시판  | POST   | `/community/`                            | 게시글 작성            | O  |
| 게시판  | GET    | `/community/{post_id}/`                  | 게시글 상세 조회         | X  |
| 게시판  | PUT    | `/community/{post_id}/`                  | 게시글 수정            | O  |
| 게시판  | DELETE | `/community/{post_id}/`                  | 게시글 삭제            | O  |
| 게시판  | POST   | `/community/{post_id}/like/`             | 게시글 좋아요 토글        | O  |
| 댓글   | POST   | `/community/{post_id}/comments/`         | 댓글 작성             | O  |
| 댓글   | PUT    | `/community/comments/{comment_id}/`      | 댓글 수정             | O  |
| 댓글   | DELETE | `/community/comments/{comment_id}/`      | 댓글 삭제             | O  |
| 댓글   | POST   | `/community/comments/{comment_id}/like/` | 댓글 좋아요 토글         | O  |
| 영상   | GET    | `/videos/search/`                        | 유튜브 영상 검색         | X  |
| 영상   | GET    | `/videos/{video_id}/`                    | 유튜브 영상 상세 조회      | X  |
| 영상   | GET    | `/videos/saved/`                         | 저장한 영상 목록 조회      | O  |
| 영상   | POST   | `/videos/saved/`                         | 영상 저장             | O  |
| 영상   | DELETE | `/videos/saved/{video_id}/`              | 저장한 영상 삭제         | O  |
| 자산   | GET    | `/assets/prices/`                        | 금/은 시세 조회         | X  |

---

## 4. 주요 API 상세

## 4.1 회원가입

| 항목     | 내용                                      |
| ------ | --------------------------------------- |
| Method | POST                                    |
| URL    | `/accounts/signup/`                     |
| 인증     | X                                       |
| 설명     | 아이디, 비밀번호, 이메일, 금융 프로필 정보를 입력하여 회원가입한다. |

### Request Body

```json
{
  "username": "user01",
  "password": "password123!",
  "password_confirm": "password123!",
  "email": "user01@example.com",
  "age": 25,
  "monthly_income_range": "200_300",
  "monthly_saving_amount": "30_50",
  "lump_sum_amount": "500_1000",
  "main_bank": "국민은행",
  "address": "서울특별시",
  "personal_info_agree": true
}
```

### Response

```json
{
  "message": "회원가입이 완료되었습니다.",
  "user": {
    "id": 1,
    "username": "user01",
    "email": "user01@example.com",
    "profile": {
      "profile_image": null,
      "profile_image_url": "",
      "age": 25,
      "monthly_income_range": "200_300",
      "monthly_saving_amount": "30_50",
      "lump_sum_amount": "500_1000",
      "main_bank": "국민은행",
      "address": "서울특별시",
      "personal_info_agree": true
    }
  }
}
```

---

## 4.2 로그인

| 항목     | 내용                                  |
| ------ | ----------------------------------- |
| Method | POST                                |
| URL    | `/accounts/login/`                  |
| 인증     | X                                   |
| 설명     | 아이디와 비밀번호를 이용하여 로그인하고 Token을 발급받는다. |

### Request Body

```json
{
  "username": "user01",
  "password": "password123!"
}
```

### Response

```json
{
  "message": "로그인되었습니다.",
  "token": "token_value",
  "user": {
    "id": 1,
    "username": "user01",
    "email": "user01@example.com",
    "profile": {
      "age": 25,
      "monthly_income_range": "200_300",
      "monthly_saving_amount": "30_50",
      "lump_sum_amount": "500_1000",
      "main_bank": "국민은행",
      "address": "서울특별시"
    }
  }
}
```

---

## 4.3 로그아웃

| 항목     | 내용                   |
| ------ | -------------------- |
| Method | POST                 |
| URL    | `/accounts/logout/`  |
| 인증     | O                    |
| 설명     | 로그인한 사용자를 로그아웃 처리한다. |

### Response

```json
{
  "message": "로그아웃되었습니다."
}
```

---

## 4.4 아이디 찾기

| 항목     | 내용                             |
| ------ | ------------------------------ |
| Method | POST                           |
| URL    | `/accounts/find-username/`     |
| 인증     | X                              |
| 설명     | 이메일을 기준으로 가입된 아이디를 마스킹하여 조회한다. |

### Request Body

```json
{
  "email": "user01@example.com"
}
```

### Response

```json
{
  "message": "아이디 찾기가 완료되었습니다.",
  "usernames": [
    {
      "username": "user**",
      "created_at": "2026-06-20"
    }
  ]
}
```

---

## 4.5 비밀번호 재설정

| 항목     | 내용                                      |
| ------ | --------------------------------------- |
| Method | POST                                    |
| URL    | `/accounts/reset-password/`             |
| 인증     | X                                       |
| 설명     | 아이디와 이메일이 일치하는 계정의 비밀번호를 새 비밀번호로 재설정한다. |

### Request Body

```json
{
  "username": "user01",
  "email": "user01@example.com",
  "new_password": "newpassword123!",
  "new_password_confirm": "newpassword123!"
}
```

### Response

```json
{
  "message": "비밀번호가 재설정되었습니다. 새 비밀번호로 로그인해주세요."
}
```

---

## 4.6 비밀번호 변경

| 항목     | 내용                                   |
| ------ | ------------------------------------ |
| Method | POST                                 |
| URL    | `/accounts/password/change/`         |
| 인증     | O                                    |
| 설명     | 로그인한 사용자가 현재 비밀번호 확인 후 새 비밀번호로 변경한다. |

### Request Body

```json
{
  "current_password": "password123!",
  "new_password": "newpassword123!",
  "new_password_confirm": "newpassword123!"
}
```

### Response

```json
{
  "message": "비밀번호가 변경되었습니다. 다시 로그인해주세요."
}
```

---

## 4.7 회원탈퇴

| 항목     | 내용                                |
| ------ | --------------------------------- |
| Method | DELETE                            |
| URL    | `/accounts/withdraw/`             |
| 인증     | O                                 |
| 설명     | 로그인한 사용자의 비밀번호를 확인한 뒤 계정을 비활성화한다. |

### Request Body

```json
{
  "password": "password123!"
}
```

### Response

```json
{
  "message": "회원탈퇴가 완료되었습니다."
}
```

---

## 4.8 내 프로필 조회

| 항목     | 내용                                |
| ------ | --------------------------------- |
| Method | GET                               |
| URL    | `/accounts/profile/`              |
| 인증     | O                                 |
| 설명     | 로그인한 사용자의 계정 정보와 금융 프로필 정보를 조회한다. |

### Response

```json
{
  "id": 1,
  "username": "user01",
  "email": "user01@example.com",
  "profile": {
    "profile_image": null,
    "profile_image_url": "",
    "age": 25,
    "monthly_income_range": "200_300",
    "monthly_saving_amount": "30_50",
    "lump_sum_amount": "500_1000",
    "main_bank": "국민은행",
    "address": "서울특별시",
    "personal_info_agree": true
  }
}
```

---

## 4.9 내 프로필 수정

| 항목     | 내용                                       |
| ------ | ---------------------------------------- |
| Method | PATCH                                    |
| URL    | `/accounts/profile/update/`              |
| 인증     | O                                        |
| 설명     | 로그인한 사용자의 이메일, 프로필 이미지, 금융 프로필 정보를 수정한다. |

### Request Body

```json
{
  "email": "new@example.com",
  "age": 26,
  "monthly_income_range": "300_400",
  "monthly_saving_amount": "50_100",
  "lump_sum_amount": "1000_3000",
  "main_bank": "신한은행",
  "address": "경기도",
  "personal_info_agree": true
}
```

### Response

```json
{
  "message": "회원정보가 수정되었습니다.",
  "user": {
    "id": 1,
    "username": "user01",
    "email": "new@example.com",
    "profile": {
      "age": 26,
      "monthly_income_range": "300_400",
      "monthly_saving_amount": "50_100",
      "lump_sum_amount": "1000_3000",
      "main_bank": "신한은행",
      "address": "경기도"
    }
  }
}
```

---

## 4.10 프로필 선택지 조회

| 항목     | 내용                                                           |
| ------ | ------------------------------------------------------------ |
| Method | GET                                                          |
| URL    | `/accounts/profile/options/`                                 |
| 인증     | X                                                            |
| 설명     | 회원가입과 마이페이지에서 사용할 나이, 소득, 저축 가능 금액, 목돈, 주거래은행, 지역 선택지를 조회한다. |

### Response

```json
{
  "age": [
    {
      "value": 19,
      "label": "19세"
    }
  ],
  "monthly_income_range": [
    {
      "value": "200_300",
      "label": "200만원 이상 300만원 미만"
    }
  ],
  "monthly_saving_amount": [
    {
      "value": "30_50",
      "label": "30만원 이상 50만원 미만"
    }
  ],
  "lump_sum_amount": [
    {
      "value": "500_1000",
      "label": "500만원 이상 1000만원 미만"
    }
  ],
  "main_bank": [
    {
      "value": "국민은행",
      "label": "국민은행"
    }
  ],
  "address": [
    {
      "value": "서울특별시",
      "label": "서울특별시"
    }
  ]
}
```

---

## 4.11 정기예금 상품 DB 저장

| 항목     | 내용                                    |
| ------ | ------------------------------------- |
| Method | GET                                   |
| URL    | `/products/deposits/save/`            |
| 인증     | X                                     |
| 설명     | 금융감독원 API에서 정기예금 상품 정보를 가져와 DB에 저장한다. |

### Response

```json
{
  "success": true,
  "message": "deposit 상품 저장이 완료되었습니다.",
  "created_count": 10,
  "updated_count": 5
}
```

---

## 4.12 정기예금 상품 목록 조회

| 항목     | 내용                                                  |
| ------ | --------------------------------------------------- |
| Method | GET                                                 |
| URL    | `/products/deposits/`                               |
| 인증     | X                                                   |
| 설명     | DB에 저장된 정기예금 상품 목록을 조회한다. 데이터가 없으면 저장 API를 먼저 실행한다. |

### Response

```json
[
  {
    "id": 1,
    "bank": {
      "id": 1,
      "name": "국민은행",
      "code": "001"
    },
    "product_type": "deposit",
    "fin_prdt_cd": "WR0001B",
    "name": "KB Star 정기예금",
    "join_way": "인터넷, 스마트폰",
    "join_member": "실명의 개인",
    "max_interest_rate": 3.5,
    "options": [
      {
        "id": 1,
        "intr_rate_type": "S",
        "intr_rate_type_nm": "단리",
        "rsrv_type": null,
        "rsrv_type_nm": null,
        "save_trm": 12,
        "intr_rate": 3.2,
        "intr_rate2": 3.5
      }
    ]
  }
]
```

---

## 4.13 정기예금 상품 상세 조회

| 항목     | 내용                                 |
| ------ | ---------------------------------- |
| Method | GET                                |
| URL    | `/products/deposits/{product_id}/` |
| 인증     | X                                  |
| 설명     | 특정 정기예금 상품의 상세 정보와 금리 옵션을 조회한다.    |

### Response

```json
{
  "id": 1,
  "bank": {
    "id": 1,
    "name": "국민은행",
    "code": "001"
  },
  "product_type": "deposit",
  "fin_prdt_cd": "WR0001B",
  "name": "KB Star 정기예금",
  "join_way": "인터넷, 스마트폰",
  "mtrt_int": "만기 후 이자율 안내",
  "spcl_cnd": "우대 조건 안내",
  "join_deny": "1",
  "join_member": "실명의 개인",
  "etc_note": "기타 유의사항",
  "max_limit": 10000000,
  "dcls_month": "202606",
  "dcls_strt_day": "20260601",
  "dcls_end_day": null,
  "fin_co_subm_day": "202606010000",
  "max_interest_rate": 3.5,
  "options": [
    {
      "id": 1,
      "save_trm": 12,
      "intr_rate": 3.2,
      "intr_rate2": 3.5
    }
  ]
}
```

---

## 4.14 적금 상품 DB 저장

| 항목     | 내용                                  |
| ------ | ----------------------------------- |
| Method | GET                                 |
| URL    | `/products/savings/save/`           |
| 인증     | X                                   |
| 설명     | 금융감독원 API에서 적금 상품 정보를 가져와 DB에 저장한다. |

### Response

```json
{
  "success": true,
  "message": "saving 상품 저장이 완료되었습니다.",
  "created_count": 10,
  "updated_count": 5
}
```

---

## 4.15 적금 상품 목록 조회

| 항목     | 내용                                                |
| ------ | ------------------------------------------------- |
| Method | GET                                               |
| URL    | `/products/savings/`                              |
| 인증     | X                                                 |
| 설명     | DB에 저장된 적금 상품 목록을 조회한다. 데이터가 없으면 저장 API를 먼저 실행한다. |

### Response

```json
[
  {
    "id": 2,
    "bank": {
      "id": 1,
      "name": "국민은행",
      "code": "001"
    },
    "product_type": "saving",
    "fin_prdt_cd": "WR0002B",
    "name": "KB Star 적금",
    "join_way": "인터넷, 스마트폰",
    "join_member": "실명의 개인",
    "max_interest_rate": 4.0,
    "options": [
      {
        "id": 2,
        "rsrv_type": "S",
        "rsrv_type_nm": "정액적립식",
        "save_trm": 12,
        "intr_rate": 3.5,
        "intr_rate2": 4.0
      }
    ]
  }
]
```

---

## 4.16 적금 상품 상세 조회

| 항목     | 내용                                |
| ------ | --------------------------------- |
| Method | GET                               |
| URL    | `/products/savings/{product_id}/` |
| 인증     | X                                 |
| 설명     | 특정 적금 상품의 상세 정보와 금리 옵션을 조회한다.     |

### Response

```json
{
  "id": 2,
  "bank": {
    "id": 1,
    "name": "국민은행",
    "code": "001"
  },
  "product_type": "saving",
  "fin_prdt_cd": "WR0002B",
  "name": "KB Star 적금",
  "join_way": "인터넷, 스마트폰",
  "spcl_cnd": "우대 조건 안내",
  "join_member": "실명의 개인",
  "max_interest_rate": 4.0,
  "options": [
    {
      "id": 2,
      "rsrv_type": "S",
      "rsrv_type_nm": "정액적립식",
      "save_trm": 12,
      "intr_rate": 3.5,
      "intr_rate2": 4.0
    }
  ]
}
```

---

## 4.17 관심 상품 목록 조회

| 항목     | 내용                            |
| ------ | ----------------------------- |
| Method | GET                           |
| URL    | `/favorites/`                 |
| 인증     | O                             |
| 설명     | 로그인한 사용자가 저장한 관심 상품 목록을 조회한다. |

### Response

```json
[
  {
    "id": 1,
    "product": {
      "id": 1,
      "bank": {
        "id": 1,
        "name": "국민은행",
        "code": "001"
      },
      "product_type": "deposit",
      "name": "KB Star 정기예금",
      "max_interest_rate": 3.5
    },
    "created_at": "2026-06-20T10:00:00"
  }
]
```

---

## 4.18 관심 상품 등록/삭제 토글

| 항목     | 내용                                 |
| ------ | ---------------------------------- |
| Method | POST                               |
| URL    | `/favorites/{product_id}/`         |
| 인증     | O                                  |
| 설명     | 관심 상품에 없으면 등록하고, 이미 등록되어 있으면 삭제한다. |

### Response - 등록

```json
{
  "message": "관심상품에 추가되었습니다.",
  "is_favorite": true
}
```

### Response - 삭제

```json
{
  "message": "관심상품에서 삭제되었습니다.",
  "is_favorite": false
}
```

---

## 4.19 예적금 상품 추천

| 항목     | 내용                                       |
| ------ | ---------------------------------------- |
| Method | POST                                     |
| URL    | `/recommendations/products/`             |
| 인증     | O                                        |
| 설명     | 사용자의 프로필과 입력 조건을 기준으로 예금 또는 적금 상품을 추천한다. |

### Request Body

```json
{
  "saving_style": "monthly",
  "product_type": "saving",
  "preferred_term": "12",
  "main_bank": "국민은행",
  "bank_filter": "all",
  "condition_preference": "high_rate",
  "join_preference": "online"
}
```

### Request Body 필드 설명

| 이름                   | 타입     | 필수 | 설명                                  |
| -------------------- | ------ | -- | ----------------------------------- |
| saving_style         | string | X  | 저축 방식, `lump`, `monthly`, `unknown` |
| product_type         | string | X  | 상품 유형, `deposit`, `saving`, `auto`  |
| preferred_term       | string | X  | 희망 가입 기간, 예: `6`, `12`, `24`, `any` |
| main_bank            | string | X  | 주거래은행명                              |
| bank_filter          | string | X  | 전체 은행 또는 주거래은행만 보기                  |
| condition_preference | string | X  | 우대조건 선호                             |
| join_preference      | string | X  | 가입 방식 선호                            |

### Response

```json
{
  "recommendations": [
    {
      "product_id": 1,
      "option_id": 1,
      "bank_name": "국민은행",
      "product_name": "KB Star 적금",
      "product_type": "saving",
      "product_type_label": "적금",
      "save_trm": 12,
      "base_rate": 3.5,
      "max_rate": 4.0,
      "effective_rate": 4.0,
      "score": 95,
      "condition_label": "우대금리형",
      "condition_description": "우대 조건 안내",
      "join_way": "인터넷, 스마트폰",
      "join_member": "실명의 개인",
      "reasons": [
        "희망 가입 기간과 일치합니다.",
        "최고금리가 높은 상품입니다."
      ]
    }
  ],
  "profile_used": {
    "age": 25,
    "monthly_income_range": "200_300",
    "monthly_saving_amount": "30_50",
    "lump_sum_amount": "500_1000",
    "main_bank": "국민은행",
    "address": "서울특별시"
  }
}
```

---

## 4.20 주거래은행 추천 결과 생성

| 항목     | 내용                                           |
| ------ | -------------------------------------------- |
| Method | POST                                         |
| URL    | `/recommendations/main-bank/`                |
| 인증     | O                                            |
| 설명     | 사용자의 은행 이용 성향 답변을 바탕으로 주거래은행을 추천하고 결과를 저장한다. |

### Request Body

```json
{
  "access_preference": "mobile",
  "benefit_preference": "interest",
  "stability_preference": "high",
  "usage_purpose": "saving"
}
```

### Response

```json
{
  "id": 1,
  "access_preference": "mobile",
  "benefit_preference": "interest",
  "stability_preference": "high",
  "usage_purpose": "saving",
  "recommended_bank": 1,
  "recommended_bank_name": "국민은행",
  "reason": "모바일 접근성과 예적금 혜택을 고려하여 추천되었습니다.",
  "created_at": "2026-06-20T10:00:00"
}
```

---

## 4.21 주거래은행 추천 이력 조회

| 항목     | 내용                           |
| ------ | ---------------------------- |
| Method | GET                          |
| URL    | `/recommendations/history/`  |
| 인증     | O                            |
| 설명     | 로그인한 사용자의 주거래은행 추천 이력을 조회한다. |

### Response

```json
[
  {
    "id": 1,
    "access_preference": "mobile",
    "benefit_preference": "interest",
    "stability_preference": "high",
    "usage_purpose": "saving",
    "recommended_bank": 1,
    "recommended_bank_name": "국민은행",
    "reason": "모바일 접근성과 예적금 혜택을 고려하여 추천되었습니다.",
    "created_at": "2026-06-20T10:00:00"
  }
]
```

---

## 4.22 환율 정보 조회

| 항목     | 내용                                  |
| ------ | ----------------------------------- |
| Method | GET                                 |
| URL    | `/exchanges/rates/`                 |
| 인증     | X                                   |
| 설명     | 한국수출입은행 API를 통해 특정 날짜의 환율 정보를 조회한다. |

### Query Parameters

| 이름   | 타입     | 필수 | 설명                  |
| ---- | ------ | -- | ------------------- |
| date | string | O  | 조회 날짜, `YYYY-MM-DD` |

### Request Example

```http
GET /api/exchanges/rates/?date=2026-06-20
```

### Response

```json
{
  "requested_date": "2026-06-20",
  "date": "2026-06-20",
  "rates": [
    {
      "currency_code": "USD",
      "currency_name": "미국 달러",
      "rate": 1380.5,
      "display_unit": "1 USD"
    }
  ]
}
```

---

## 4.23 환율 기간별 히스토리 조회

| 항목     | 내용                                      |
| ------ | --------------------------------------- |
| Method | GET                                     |
| URL    | `/exchanges/history/`                   |
| 인증     | X                                       |
| 설명     | 선택한 통화의 기간별 환율 데이터를 조회한다. 환율 그래프에 사용한다. |

### Query Parameters

| 이름         | 타입     | 필수 | 설명                |
| ---------- | ------ | -- | ----------------- |
| currency   | string | X  | 통화 코드, 기본값 `USD`  |
| start_date | string | O  | 시작일, `YYYY-MM-DD` |
| end_date   | string | O  | 종료일, `YYYY-MM-DD` |

### Request Example

```http
GET /api/exchanges/history/?currency=USD&start_date=2026-06-01&end_date=2026-06-20
```

### Response

```json
{
  "currency": "USD",
  "start_date": "2026-06-01",
  "end_date": "2026-06-20",
  "count": 10,
  "rows": [
    {
      "date": "2026-06-03",
      "currency_code": "USD",
      "currency_name": "미국 달러",
      "rate": 1380.5,
      "display_unit": "1 USD"
    }
  ]
}
```

---

## 4.24 환율 계산

| 항목     | 내용                              |
| ------ | ------------------------------- |
| Method | POST                            |
| URL    | `/exchanges/calculate/`         |
| 인증     | X                               |
| 설명     | 원화 금액과 통화 코드를 기준으로 환전 금액을 계산한다. |

### Request Body

```json
{
  "amount": 100000,
  "currency": "USD",
  "date": "2026-06-20"
}
```

### Response

```json
{
  "date": "2026-06-20",
  "amount_krw": 100000,
  "currency": "USD",
  "currency_name": "미국 달러",
  "rate": 1380.5,
  "converted_amount": 72.43
}
```

---

## 4.25 은행 위치 검색

| 항목     | 내용                                     |
| ------ | -------------------------------------- |
| Method | GET                                    |
| URL    | `/maps/banks/`                         |
| 인증     | X                                      |
| 설명     | 사용자의 현재 위치와 은행명을 기준으로 가까운 은행 지점을 검색한다. |

### Query Parameters

| 이름   | 타입     | 필수 | 설명                |
| ---- | ------ | -- | ----------------- |
| bank | string | X  | 검색할 은행명, 기본값 `은행` |
| lat  | number | O  | 현재 위치 위도          |
| lng  | number | O  | 현재 위치 경도          |

### Request Example

```http
GET /api/maps/banks/?bank=국민은행&lat=37.5665&lng=126.9780
```

### Response

```json
{
  "keyword": "국민은행",
  "lat": "37.5665",
  "lng": "126.9780",
  "count": 1,
  "branches": [
    {
      "id": "123456",
      "place_name": "국민은행 광화문지점",
      "address_name": "서울 종로구 세종대로 172",
      "road_address_name": "서울 종로구 세종대로 172",
      "phone": "02-0000-0000",
      "x": "126.9780",
      "y": "37.5665",
      "distance": "120",
      "place_url": "https://place.map.kakao.com/..."
    }
  ]
}
```

---

## 4.26 은행 경로 검색

| 항목     | 내용                                  |
| ------ | ----------------------------------- |
| Method | GET                                 |
| URL    | `/maps/routes/`                     |
| 인증     | X                                   |
| 설명     | 사용자의 현재 위치에서 선택한 은행 지점까지의 경로를 조회한다. |

### Query Parameters

| 이름              | 타입     | 필수 | 설명                       |
| --------------- | ------ | -- | ------------------------ |
| origin_lat      | number | O  | 출발지 위도                   |
| origin_lng      | number | O  | 출발지 경도                   |
| destination_lat | number | O  | 도착지 위도                   |
| destination_lng | number | O  | 도착지 경도                   |
| priority        | string | X  | 경로 우선순위, 기본값 `RECOMMEND` |

### Request Example

```http
GET /api/maps/routes/?origin_lat=37.5665&origin_lng=126.9780&destination_lat=37.5700&destination_lng=126.9820
```

### Response

```json
{
  "routes": [
    {
      "result_code": 0,
      "result_msg": "길찾기 성공",
      "sections": []
    }
  ]
}
```

---

## 4.27 금융 설명 챗봇

| 항목     | 내용                                                  |
| ------ | --------------------------------------------------- |
| Method | POST                                                |
| URL    | `/chatbot/explain/`                                 |
| 인증     | X                                                   |
| 설명     | 사용자가 입력한 금융상품명 또는 금융용어를 백엔드로 전송하고, 챗봇이 쉬운 설명을 반환한다. |

### Request Body

```json
{
  "message": "예금자보호가 뭐야?"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "type": "llm",
    "question": "예금자보호가 뭐야?",
    "answer": "예금자보호는 금융회사가 파산하거나 예금을 돌려주기 어려운 상황에서 일정 한도 내에서 예금자를 보호해주는 제도입니다."
  }
}
```

---

## 4.28 게시글 목록 조회

| 항목     | 내용                 |
| ------ | ------------------ |
| Method | GET                |
| URL    | `/community/`      |
| 인증     | X                  |
| 설명     | 커뮤니티 게시글 목록을 조회한다. |

### Response

```json
[
  {
    "id": 1,
    "title": "적금 추천 부탁드립니다.",
    "content": "사회초년생에게 맞는 적금이 궁금합니다.",
    "category": "상품추천",
    "user_id": 1,
    "username": "user01",
    "view_count": 0,
    "comment_count": 2,
    "like_count": 3,
    "is_liked": false,
    "is_author": false,
    "created_at": "2026-06-20T10:00:00",
    "updated_at": "2026-06-20T10:00:00"
  }
]
```

---

## 4.29 게시글 작성

| 항목     | 내용                        |
| ------ | ------------------------- |
| Method | POST                      |
| URL    | `/community/`             |
| 인증     | O                         |
| 설명     | 로그인한 사용자가 커뮤니티 게시글을 작성한다. |

### Request Body

```json
{
  "title": "적금 추천 부탁드립니다.",
  "content": "사회초년생에게 맞는 적금이 궁금합니다.",
  "category": "상품추천"
}
```

### Response

```json
{
  "id": 1,
  "title": "적금 추천 부탁드립니다.",
  "content": "사회초년생에게 맞는 적금이 궁금합니다.",
  "category": "상품추천",
  "user_id": 1,
  "username": "user01",
  "view_count": 0,
  "like_count": 0,
  "is_liked": false,
  "is_author": true,
  "comments": [],
  "created_at": "2026-06-20T10:00:00",
  "updated_at": "2026-06-20T10:00:00"
}
```

---

## 4.30 게시글 상세 조회

| 항목     | 내용                                          |
| ------ | ------------------------------------------- |
| Method | GET                                         |
| URL    | `/community/{post_id}/`                     |
| 인증     | X                                           |
| 설명     | 특정 게시글의 상세 내용과 댓글 목록을 조회한다. 조회 시 조회수가 증가한다. |

### Response

```json
{
  "id": 1,
  "title": "적금 추천 부탁드립니다.",
  "content": "사회초년생에게 맞는 적금이 궁금합니다.",
  "category": "상품추천",
  "user_id": 1,
  "username": "user01",
  "view_count": 1,
  "like_count": 3,
  "is_liked": false,
  "is_author": false,
  "comments": [
    {
      "id": 1,
      "post": 1,
      "user": 2,
      "user_id": 2,
      "username": "user02",
      "content": "12개월 적금을 추천합니다.",
      "like_count": 1,
      "is_liked": false,
      "is_author": false,
      "created_at": "2026-06-20T10:20:00"
    }
  ],
  "created_at": "2026-06-20T10:00:00",
  "updated_at": "2026-06-20T10:00:00"
}
```

---

## 4.31 게시글 수정

| 항목     | 내용                           |
| ------ | ---------------------------- |
| Method | PUT                          |
| URL    | `/community/{post_id}/`      |
| 인증     | O                            |
| 설명     | 로그인한 사용자가 자신이 작성한 게시글을 수정한다. |

### Request Body

```json
{
  "title": "적금 추천 다시 부탁드립니다.",
  "content": "12개월 기준으로 추천받고 싶습니다.",
  "category": "상품추천"
}
```

### Response

```json
{
  "id": 1,
  "title": "적금 추천 다시 부탁드립니다.",
  "content": "12개월 기준으로 추천받고 싶습니다.",
  "category": "상품추천",
  "updated_at": "2026-06-20T11:00:00"
}
```

---

## 4.32 게시글 삭제

| 항목     | 내용                           |
| ------ | ---------------------------- |
| Method | DELETE                       |
| URL    | `/community/{post_id}/`      |
| 인증     | O                            |
| 설명     | 로그인한 사용자가 자신이 작성한 게시글을 삭제한다. |

### Response

```json
{
  "message": "게시글이 삭제되었습니다."
}
```

---

## 4.33 게시글 좋아요 토글

| 항목     | 내용                           |
| ------ | ---------------------------- |
| Method | POST                         |
| URL    | `/community/{post_id}/like/` |
| 인증     | O                            |
| 설명     | 특정 게시글의 좋아요를 등록하거나 취소한다.     |

### Response

```json
{
  "liked": true,
  "like_count": 4
}
```

---

## 4.34 댓글 작성

| 항목     | 내용                               |
| ------ | -------------------------------- |
| Method | POST                             |
| URL    | `/community/{post_id}/comments/` |
| 인증     | O                                |
| 설명     | 로그인한 사용자가 특정 게시글에 댓글을 작성한다.      |

### Request Body

```json
{
  "content": "저는 12개월 적금을 추천합니다."
}
```

### Response

```json
{
  "id": 1,
  "post": 1,
  "user": 1,
  "user_id": 1,
  "username": "user01",
  "content": "저는 12개월 적금을 추천합니다.",
  "like_count": 0,
  "is_liked": false,
  "is_author": true,
  "created_at": "2026-06-20T10:20:00"
}
```

---

## 4.35 댓글 수정

| 항목     | 내용                                  |
| ------ | ----------------------------------- |
| Method | PUT                                 |
| URL    | `/community/comments/{comment_id}/` |
| 인증     | O                                   |
| 설명     | 로그인한 사용자가 자신이 작성한 댓글을 수정한다.         |

### Request Body

```json
{
  "content": "저는 12개월 자유적금을 추천합니다."
}
```

### Response

```json
{
  "id": 1,
  "content": "저는 12개월 자유적금을 추천합니다.",
  "like_count": 0,
  "is_liked": false,
  "is_author": true
}
```

---

## 4.36 댓글 삭제

| 항목     | 내용                                  |
| ------ | ----------------------------------- |
| Method | DELETE                              |
| URL    | `/community/comments/{comment_id}/` |
| 인증     | O                                   |
| 설명     | 로그인한 사용자가 자신이 작성한 댓글을 삭제한다.         |

### Response

```json
{
  "message": "댓글이 삭제되었습니다."
}
```

---

## 4.37 댓글 좋아요 토글

| 항목     | 내용                                       |
| ------ | ---------------------------------------- |
| Method | POST                                     |
| URL    | `/community/comments/{comment_id}/like/` |
| 인증     | O                                        |
| 설명     | 특정 댓글의 좋아요를 등록하거나 취소한다.                  |

### Response

```json
{
  "liked": true,
  "like_count": 2
}
```

---

## 4.38 유튜브 영상 검색

| 항목     | 내용                                |
| ------ | --------------------------------- |
| Method | GET                               |
| URL    | `/videos/search/`                 |
| 인증     | X                                 |
| 설명     | YouTube API를 이용하여 금융 관련 영상을 검색한다. |

### Query Parameters

| 이름          | 타입      | 필수 | 설명                     |
| ----------- | ------- | -- | ---------------------- |
| q           | string  | X  | 검색어, 기본값 `주거래은행 선택 기준` |
| max_results | integer | X  | 검색 결과 개수, 기본값 `3`      |

### Request Example

```http
GET /api/videos/search/?q=주거래은행 선택 기준&max_results=3
```

### Response

```json
[
  {
    "video_id": "abc123",
    "title": "주거래은행 고르는 방법",
    "description": "영상 설명",
    "channel_title": "금융채널",
    "channel_id": "channel123",
    "published_at": "2026-06-20T10:00:00Z",
    "thumbnail_url": "https://img.youtube.com/..."
  }
]
```

---

## 4.39 유튜브 영상 상세 조회

| 항목     | 내용                      |
| ------ | ----------------------- |
| Method | GET                     |
| URL    | `/videos/{video_id}/`   |
| 인증     | X                       |
| 설명     | 특정 유튜브 영상의 상세 정보를 조회한다. |

### Response

```json
{
  "video_id": "abc123",
  "title": "주거래은행 고르는 방법",
  "description": "영상 설명",
  "channel_title": "금융채널",
  "channel_id": "channel123",
  "published_at": "2026-06-20T10:00:00Z",
  "thumbnail_url": "https://img.youtube.com/...",
  "view_count": "1000"
}
```

---

## 4.40 저장한 영상 목록 조회

| 항목     | 내용                             |
| ------ | ------------------------------ |
| Method | GET                            |
| URL    | `/videos/saved/`               |
| 인증     | O                              |
| 설명     | 로그인한 사용자가 저장한 유튜브 영상 목록을 조회한다. |

### Response

```json
[
  {
    "id": 1,
    "video_id": "abc123",
    "title": "주거래은행 고르는 방법",
    "channel_title": "금융채널",
    "channel_id": "channel123",
    "description": "영상 설명",
    "thumbnail_url": "https://img.youtube.com/...",
    "published_at": "2026-06-20T10:00:00Z",
    "saved_at": "2026-06-20T11:00:00"
  }
]
```

---

## 4.41 영상 저장

| 항목     | 내용                      |
| ------ | ----------------------- |
| Method | POST                    |
| URL    | `/videos/saved/`        |
| 인증     | O                       |
| 설명     | 로그인한 사용자가 유튜브 영상을 저장한다. |

### Request Body

```json
{
  "video_id": "abc123",
  "title": "주거래은행 고르는 방법",
  "channel_title": "금융채널",
  "channel_id": "channel123",
  "description": "영상 설명",
  "thumbnail_url": "https://img.youtube.com/...",
  "published_at": "2026-06-20T10:00:00Z"
}
```

### Response

```json
{
  "id": 1,
  "video_id": "abc123",
  "title": "주거래은행 고르는 방법",
  "channel_title": "금융채널",
  "channel_id": "channel123",
  "description": "영상 설명",
  "thumbnail_url": "https://img.youtube.com/...",
  "published_at": "2026-06-20T10:00:00Z",
  "saved_at": "2026-06-20T11:00:00"
}
```

---

## 4.42 저장한 영상 삭제

| 항목     | 내용                          |
| ------ | --------------------------- |
| Method | DELETE                      |
| URL    | `/videos/saved/{video_id}/` |
| 인증     | O                           |
| 설명     | 로그인한 사용자가 저장한 영상을 삭제한다.     |

### Response

```json
{
  "message": "저장한 영상을 삭제했습니다."
}
```

---

## 4.43 금/은 시세 조회

| 항목     | 내용                        |
| ------ | ------------------------- |
| Method | GET                       |
| URL    | `/assets/prices/`         |
| 인증     | X                         |
| 설명     | 금 또는 은의 기간별 시세 데이터를 조회한다. |

### Query Parameters

| 이름         | 타입     | 필수 | 설명                                    |
| ---------- | ------ | -- | ------------------------------------- |
| asset      | string | X  | 자산 유형, `gold` 또는 `silver`, 기본값 `gold` |
| start_date | string | X  | 시작일, `YYYY-MM-DD`                     |
| end_date   | string | X  | 종료일, `YYYY-MM-DD`                     |

### Request Example

```http
GET /api/assets/prices/?asset=gold&start_date=2026-06-01&end_date=2026-06-20
```

### Response

```json
{
  "asset": "gold",
  "asset_label": "금",
  "english_label": "Gold",
  "count": 10,
  "rows": [
    {
      "date": "2026-06-01",
      "price": 100000
    }
  ],
  "summary": {
    "latest_price": 100000,
    "min_price": 95000,
    "max_price": 105000
  }
}
```

---

## 5. 프론트엔드 구현 및 API 연동 기준

아래 기능은 Vue 프론트엔드에서 화면과 사용자 인터랙션을 구현하고, 필요한 데이터는 백엔드 API를 호출하여 처리한다.

| 기능       | 프론트엔드 역할               | 백엔드 API 연동                                                            |
| -------- | ---------------------- | --------------------------------------------------------------------- |
| 회원가입     | 입력값 관리, 유효성 메시지 표시     | `/accounts/signup/`                                                   |
| 로그인      | 로그인 요청, token 저장       | `/accounts/login/`                                                    |
| 아이디 찾기   | 이메일 입력 후 아이디 조회        | `/accounts/find-username/`                                            |
| 비밀번호 재설정 | 아이디/이메일 확인 후 새 비밀번호 설정 | `/accounts/reset-password/`                                           |
| 마이페이지    | 프로필 조회 및 수정            | `/accounts/profile/`, `/accounts/profile/update/`                     |
| 프로필 선택지  | select 옵션 표시           | `/accounts/profile/options/`                                          |
| 예금 상품 목록 | 예금 상품 카드/필터/상세 이동      | `/products/deposits/`                                                 |
| 예금 상품 상세 | 상품 상세 정보 및 금리 옵션 표시    | `/products/deposits/{product_id}/`                                    |
| 적금 상품 목록 | 적금 상품 카드/필터/상세 이동      | `/products/savings/`                                                  |
| 적금 상품 상세 | 상품 상세 정보 및 금리 옵션 표시    | `/products/savings/{product_id}/`                                     |
| 관심상품     | 관심상품 목록 조회 및 토글        | `/favorites/`, `/favorites/{product_id}/`                             |
| 예적금 추천   | 추천 조건 입력 및 추천 결과 표시    | `/recommendations/products/`                                          |
| 주거래은행 추천 | 사용자 성향 입력 후 추천 은행 표시   | `/recommendations/main-bank/`                                         |
| 추천 이력    | 주거래은행 추천 이력 표시         | `/recommendations/history/`                                           |
| 환율 조회    | 날짜별 환율 목록 표시           | `/exchanges/rates/`                                                   |
| 환율 계산    | 원화 기준 환전 금액 계산         | `/exchanges/calculate/`                                               |
| 환율 그래프   | 기간별 환율 데이터 그래프 표시      | `/exchanges/history/`                                                 |
| 지도       | 현재 위치 기준 은행 검색 및 마커 표시 | `/maps/banks/`                                                        |
| 경로 검색    | 선택 은행까지 경로 조회          | `/maps/routes/`                                                       |
| 챗봇       | 플로팅 버튼, 질문 입력, 답변 출력   | `/chatbot/explain/`                                                   |
| 게시판      | 게시글 목록, 상세, 작성, 수정, 삭제 | `/community/`                                                         |
| 게시글 좋아요  | 게시글 좋아요 토글             | `/community/{post_id}/like/`                                          |
| 댓글       | 댓글 작성, 수정, 삭제          | `/community/{post_id}/comments/`, `/community/comments/{comment_id}/` |
| 댓글 좋아요   | 댓글 좋아요 토글              | `/community/comments/{comment_id}/like/`                              |
| 유튜브 검색   | 금융 관련 영상 검색            | `/videos/search/`                                                     |
| 영상 저장    | 관심 영상 저장 및 삭제          | `/videos/saved/`                                                      |
| 금/은 시세   | 금/은 가격 데이터 조회 및 그래프 표시 | `/assets/prices/`                                                     |

챗봇은 모든 화면에서 접근할 수 있도록 `App.vue`에 플로팅 컴포넌트를 배치한다.
사용자가 챗봇에 금융상품명 또는 금융용어를 입력하면 프론트엔드는 `/chatbot/explain/` API로 요청을 보내고, 응답받은 설명을 챗봇 창에 출력한다.

---

## 6. API Key 관리 기준

외부 API Key는 보안을 위해 프론트엔드 코드에 직접 작성하지 않는다.

| 구분                 | 관리 위치                          | 설명             |
| ------------------ | ------------------------------ | -------------- |
| 금융감독원 API Key      | Django `.env`                  | 예금/적금 상품 정보 조회 |
| 한국수출입은행 환율 API Key | Django `.env`                  | 환율 정보 조회       |
| 카카오 REST API Key   | Django `.env`                  | 은행 위치 검색       |
| 카카오 모빌리티 API Key   | Django `.env`                  | 은행 경로 검색       |
| YouTube API Key    | Django `.env`                  | 금융 관련 영상 검색    |
| GMS API Key        | Django `.env`                  | 챗봇 설명 생성       |
| Vue API Base URL   | Vue `.env` 또는 `src/api/api.js` | 백엔드 서버 주소 저장   |

### Backend `.env` 예시

```env
SECRET_KEY=django-secret-key
FSS_API_KEY=금융감독원_API_KEY
EXCHANGE_API_KEY=한국수출입은행_API_KEY
KAKAO_REST_API_KEY=카카오_REST_API_KEY
YOUTUBE_API_KEY=YOUTUBE_API_KEY
GMS_API_KEY=GMS_API_KEY
GMS_MODEL=gpt-5-nano
```

### Frontend `.env` 예시

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

프론트엔드에는 실제 외부 API Key를 저장하지 않는다.
프론트엔드는 백엔드 API 주소만 알고, 백엔드가 외부 API와 통신한다.

---

## 7. 구현 우선순위

다음 순서대로 구현한다.

| 우선순위 | 기능                              |
| ---- | ------------------------------- |
| 1순위  | 회원가입, 로그인, 로그아웃                 |
| 2순위  | 프로필 조회/수정, 프로필 선택지              |
| 3순위  | 예금 상품 저장/목록/상세 조회               |
| 4순위  | 적금 상품 저장/목록/상세 조회               |
| 5순위  | 관심상품 등록/삭제/목록 조회                |
| 6순위  | 예적금 상품 추천                       |
| 7순위  | 주거래은행 추천 및 추천 이력                |
| 8순위  | 게시판, 댓글, 좋아요                    |
| 9순위  | 환율 조회, 환율 계산, 환율 그래프            |
| 10순위 | 지도 은행 검색, 경로 검색                 |
| 11순위 | 유튜브 영상 검색, 저장 영상 관리             |
| 12순위 | 챗봇 API 연결                       |
| 13순위 | 금/은 시세 조회                       |
| 14순위 | 아이디 찾기, 비밀번호 재설정, 비밀번호 변경, 회원탈퇴 |

---
