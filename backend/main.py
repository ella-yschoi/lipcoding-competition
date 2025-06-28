from fastapi import FastAPI

from . import models, schemas, crud
from .database import engine, SessionLocal
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

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
