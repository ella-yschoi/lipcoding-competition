from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'mentor' 또는 'mentee'
    name = Column(String, nullable=False)
    bio = Column(Text)

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey("users.id"))
    mentee_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="pending")  # pending, accepted, rejected

    mentor = relationship("User", foreign_keys=[mentor_id])
    mentee = relationship("User", foreign_keys=[mentee_id])
