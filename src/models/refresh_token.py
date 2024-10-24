from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from src.database.database_config import Base

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable = False)
    refresh_token = Column(String(255), unique = True, index = True, nullable = False)
    expires_in = Column(DateTime, nullable = False)
