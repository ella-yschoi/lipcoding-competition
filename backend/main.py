# 매칭 관리 API (멘토용)
from . import match_manage
# 멘토가 받은 매칭 신청 목록 (대기중)
@app.get("/mentor/match-requests/", response_model=list[schemas.MatchOut])
def get_pending_requests(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'mentor':
        raise HTTPException(status_code=403, detail="멘토만 접근 가능합니다.")
    return match_manage.get_pending_requests_for_mentor(db, mentor_id=current_user.id)

# 멘토가 매칭 신청 수락/거절
@app.post("/mentor/match-requests/{match_id}/status", response_model=schemas.MatchOut)
def update_match_status(match_id: int, status: str, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'mentor':
        raise HTTPException(status_code=403, detail="멘토만 접근 가능합니다.")
    return match_manage.update_match_status(db, match_id=match_id, mentor_id=current_user.id, status=status)
# 매칭 관련 API
from . import match_crud
# 매칭 생성 (멘티가 멘토에게 신청)
@app.post("/matches/", response_model=schemas.MatchOut)
def create_match(match: schemas.MatchCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # 멘티만 신청 가능
    if current_user.role != 'mentee':
        raise HTTPException(status_code=403, detail="멘티만 매칭을 신청할 수 있습니다.")
    return match_crud.create_match(db, mentor_id=match.mentor_id, mentee_id=current_user.id)

# 내 매칭 목록 조회
@app.get("/matches/", response_model=list[schemas.MatchOut])
def get_my_matches(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return match_crud.get_matches_by_user(db, user_id=current_user.id)
from fastapi import FastAPI

from . import models, schemas, crud, auth
from .database import engine, SessionLocal
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)


# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "멘토-멘티 매칭 앱 백엔드가 정상 동작 중입니다."}

# 회원가입
@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# 사용자 목록
@app.get("/users/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

# 내 프로필 조회 (토큰 필요)
@app.get("/me", response_model=schemas.UserOut)
def get_my_profile(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# 로그인 (토큰 발급)
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호 오류")
    # 실제 서비스라면 JWT 등 발급, 여기선 username을 토큰처럼 반환
    return {"access_token": user.username, "token_type": "bearer"}
