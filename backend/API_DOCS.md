# 멘토-멘티 매칭 앱 API 문서

## 인증

- 회원가입: `POST /api/signup`
- 로그인: `POST /api/login` (JWT 반환)

## 프로필

- 내 정보 조회: `GET /api/me`
- 프로필 등록/수정: `PUT /api/profile` (name, bio, skills, image 업로드)
- 프로필 이미지 조회: `GET /api/images/{role}/{user_id}`

## 멘토

- 멘토 리스트 조회: `GET /api/mentors?skill=...&order_by=...`

## 매칭

- 매칭 요청 생성: `POST /api/match-requests` (멘티만, message 포함)
- 받은 요청 목록: `GET /api/match-requests/incoming` (멘토)
- 보낸 요청 목록: `GET /api/match-requests/outgoing` (멘티)
- 요청 수락: `PUT /api/match-requests/{id}/accept` (멘토)
- 요청 거절: `PUT /api/match-requests/{id}/reject` (멘토)
- 요청 삭제/취소: `DELETE /api/match-requests/{id}` (멘티)

## 기타

- Swagger UI: `/docs` (모든 API 테스트 가능)
- 모든 API는 `/api` 하위에 위치
- JWT Bearer 인증 필요 (Authorization 헤더)

---

### 예시 요청/응답, 파라미터 등은 Swagger UI에서 확인 가능

---

문의: [GitHub 리포지토리](https://github.com/ella-yschoi/lipcoding-competition)
