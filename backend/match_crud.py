from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def create_match(db: Session, mentor_id: int, mentee_id: int):
    # 멘토, 멘티 존재 여부 확인
    mentor = db.query(models.User).filter(models.User.id == mentor_id, models.User.role == 'mentor').first()
    mentee = db.query(models.User).filter(models.User.id == mentee_id, models.User.role == 'mentee').first()
    if not mentor or not mentee:
        raise HTTPException(status_code=404, detail="멘토 또는 멘티를 찾을 수 없습니다.")
    match = models.Match(mentor_id=mentor_id, mentee_id=mentee_id)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

def get_matches_by_user(db: Session, user_id: int):
    return db.query(models.Match).filter(
        (models.Match.mentor_id == user_id) | (models.Match.mentee_id == user_id)
    ).all()
