from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

# 회원 생성
ndef create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        password=user.password,  # 실제 서비스에서는 해시 필요
        name=user.name,
        bio=user.bio,
        role=user.role
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")
    return db_user

# 사용자 조회
ndef get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

# 전체 사용자 목록
ndef get_users(db: Session):
    return db.query(models.User).all()

# 매칭 생성
def create_match(db: Session, mentor_id: int, mentee_id: int):
    match = models.Match(mentor_id=mentor_id, mentee_id=mentee_id)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

# 내 매칭 목록
def get_my_matches(db: Session, user_id: int, role: str):
    if role == 'mentor':
        return db.query(models.Match).filter(models.Match.mentor_id == user_id).all()
    else:
        return db.query(models.Match).filter(models.Match.mentee_id == user_id).all()
