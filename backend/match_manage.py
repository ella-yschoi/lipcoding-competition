from sqlalchemy.orm import Session
from . import models
from fastapi import HTTPException

def get_pending_requests_for_mentor(db: Session, mentor_id: int):
    return db.query(models.Match).filter(
        models.Match.mentor_id == mentor_id,
        models.Match.status == 'pending'
    ).all()

def update_match_status(db: Session, match_id: int, mentor_id: int, status: str):
    match = db.query(models.Match).filter(models.Match.id == match_id, models.Match.mentor_id == mentor_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="매칭 요청을 찾을 수 없습니다.")
    if status not in ['accepted', 'rejected']:
        raise HTTPException(status_code=400, detail="잘못된 상태입니다.")
    match.status = status
    db.commit()
    db.refresh(match)
    return match
