from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from src.database.database_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    first_name = Column(String(255), nullable = False)
    last_name = Column(String(255), nullable = False)
    email = Column(String(255), unique = True, nullable = False)
    profile_image = Column(String(255))
    created_at = Column(DateTime(timezone = True), server_default=func.now())

    # One-to-many relationship: One user can have multiple restaurants
    restaurants = relationship('Restaurant', back_populates = 'owner')