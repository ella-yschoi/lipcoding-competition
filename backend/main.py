# 프로필 등록/수정 (PUT /api/profile)
from fastapi import UploadFile, File, Form
import os

PROFILE_IMAGE_DIR = "profile_images"
os.makedirs(PROFILE_IMAGE_DIR, exist_ok=True)

@api_router.put("/profile")
async def update_profile(
    name: str = Form(...),
    bio: str = Form(None),
    skills: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    user.name = name
    user.bio = bio
    user.skills = skills
    if image:
        ext = os.path.splitext(image.filename)[-1].lower()
        if ext not in [".jpg", ".jpeg", ".png"]:
            raise HTTPException(status_code=400, detail="이미지 형식 오류")
        filename = f"{user.role}_{user.id}{ext}"
        filepath = os.path.join(PROFILE_IMAGE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(await image.read())
        user.image = filename
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name, "bio": user.bio, "skills": user.skills, "image": user.image}

# 프로필 이미지 조회 (GET /api/images/{role}/{id})
from fastapi.responses import FileResponse
@api_router.get("/images/{role}/{user_id}")
def get_profile_image(role: str, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.role == role).first()
    if user and user.image:
        filepath = os.path.join(PROFILE_IMAGE_DIR, user.image)
        if os.path.exists(filepath):
            return FileResponse(filepath)
    # 기본 이미지 제공
    if role == "mentor":
        return FileResponse("default_mentor.jpg")
    else:
        return FileResponse("default_mentee.jpg")
# 매칭 요청 생성 (멘티 전용, /api/match-requests)
from fastapi import Body

# 매칭 요청 생성 (멘티 전용, /api/match-requests)
@api_router.post("/match-requests")
def create_match_request(
    payload: dict = Body(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != 'mentee':
        raise HTTPException(status_code=403, detail="멘티만 매칭 요청 가능")
    mentor_id = payload.get("mentorId")
    message = payload.get("message", "")
    # 중복 요청 방지: 대기중 요청이 있으면 불가
    exists = db.query(models.Match).filter(
        models.Match.mentee_id == current_user.id,
        models.Match.status == 'pending'
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="이미 대기중인 요청이 있습니다.")
    match = models.Match(mentor_id=mentor_id, mentee_id=current_user.id, status='pending', message=message)
    db.add(match)
    db.commit()
    db.refresh(match)
    return {
        "id": match.id,
        "mentorId": match.mentor_id,
        "menteeId": match.mentee_id,
        "message": match.message,
        "status": match.status
    }

# 받은 요청 목록 (멘토 전용, /api/match-requests/incoming)
@api_router.get("/match-requests/incoming")
def incoming_requests(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'mentor':
        raise HTTPException(status_code=403, detail="멘토만 접근 가능")
    matches = db.query(models.Match).filter(models.Match.mentor_id == current_user.id).all()
    return [
        {
            "id": m.id,
            "mentorId": m.mentor_id,
            "menteeId": m.mentee_id,
            "message": m.message,
            "status": m.status
        } for m in matches
    ]

# 보낸 요청 목록 (멘티 전용, /api/match-requests/outgoing)
@api_router.get("/match-requests/outgoing")
def outgoing_requests(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'mentee':
        raise HTTPException(status_code=403, detail="멘티만 접근 가능")
    matches = db.query(models.Match).filter(models.Match.mentee_id == current_user.id).all()
    return [
        {
            "id": m.id,
            "mentorId": m.mentor_id,
            "menteeId": m.mentee_id,
            "message": m.message,
            "status": m.status
        } for m in matches
    ]

# 요청 수락 (멘토 전용, /api/match-requests/{id}/accept)
@api_router.put("/match-requests/{id}/accept")
def accept_request(id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'mentor':
        raise HTTPException(status_code=403, detail="멘토만 접근 가능")
    match = db.query(models.Match).filter(models.Match.id == id, models.Match.mentor_id == current_user.id).first()
    if not match:
        raise HTTPException(status_code=404, detail="매칭 요청 없음")
    match.status = 'accepted'
    db.commit()
    db.refresh(match)
    return {
        "id": match.id,
        "mentorId": match.mentor_id,
        "menteeId": match.mentee_id,
        "message": match.message,
        "status": match.status
    }

# 요청 거절 (멘토 전용, /api/match-requests/{id}/reject)
@api_router.put("/match-requests/{id}/reject")
def reject_request(id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'mentor':
        raise HTTPException(status_code=403, detail="멘토만 접근 가능")
    match = db.query(models.Match).filter(models.Match.id == id, models.Match.mentor_id == current_user.id).first()
    if not match:
        raise HTTPException(status_code=404, detail="매칭 요청 없음")
    match.status = 'rejected'
    db.commit()
    db.refresh(match)
    return {
        "id": match.id,
        "mentorId": match.mentor_id,
        "menteeId": match.mentee_id,
        "message": match.message,
        "status": match.status
    }

# 요청 삭제/취소 (멘티 전용, /api/match-requests/{id})
@api_router.delete("/match-requests/{id}")
def cancel_request(id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'mentee':
        raise HTTPException(status_code=403, detail="멘티만 접근 가능")
    match = db.query(models.Match).filter(models.Match.id == id, models.Match.mentee_id == current_user.id).first()
    if not match:
        raise HTTPException(status_code=404, detail="매칭 요청 없음")
    match.status = 'cancelled'
    db.commit()
    db.refresh(match)
    return {
        "id": match.id,
        "mentorId": match.mentor_id,
        "menteeId": match.mentee_id,
        "message": match.message,
        "status": match.status
    }
# 멘토 리스트 조회 (멘티 전용, /api/mentors)
@api_router.get("/mentors")
def list_mentors(skill: str = None, order_by: str = None, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.role == 'mentor')
    if skill:
        # 기술 스택이 bio에 포함된 경우로 임시 처리 (실제는 별도 필드 필요)
        query = query.filter(models.User.bio.contains(skill))
    if order_by == 'name':
        query = query.order_by(models.User.name.asc())
    elif order_by == 'skill':
        query = query.order_by(models.User.bio.asc())
    else:
        query = query.order_by(models.User.id.asc())
    mentors = query.all()
    # skills 필드는 bio에서 쉼표로 분리해 임시 제공
    result = []
    for m in mentors:
        skills = m.bio.split(',') if m.bio else []
        result.append({
            "id": m.id,
            "email": m.username,
            "role": m.role,
            "profile": {
                "name": m.name,
                "bio": m.bio,
                "imageUrl": f"/images/mentor/{m.id}",
                "skills": skills
            }
        })
    return result
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

from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from . import models, schemas, crud, auth
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
import jwt
import datetime

app = FastAPI()
api_router = APIRouter(prefix="/api")

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 루트 접근시 Swagger UI로 리다이렉트
@app.get("/")
def root_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

# 회원가입 (명세에 맞게 /api/signup)
@api_router.post("/signup", status_code=201)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# 사용자 목록 (관리자/테스트용)
@api_router.get("/users/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

# 내 프로필 조회 (명세에 맞게 /api/me)
@api_router.get("/me", response_model=schemas.UserOut)
def get_my_profile(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# JWT 로그인 (명세에 맞게 /api/login)
JWT_SECRET = "secret"  # 실제 서비스에서는 환경변수로 관리
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600

@api_router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    user = auth.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호 오류")
    now = datetime.datetime.utcnow()
    payload = {
        "iss": "lipcoding-competition",
        "sub": str(user.id),
        "aud": "lipcoding-app",
        "exp": now + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
        "nbf": now,
        "iat": now,
        "jti": f"{user.id}-{now.timestamp()}",
        "name": getattr(user, "name", getattr(user, "username", "")),
        "email": user.email,
        "role": user.role
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"token": token}

# (기존 매칭/멘토 관련 API는 주석 처리, 이후 명세에 맞게 재구현 예정)
# from . import match_manage
# from . import match_crud
# ...

app.include_router(api_router)
