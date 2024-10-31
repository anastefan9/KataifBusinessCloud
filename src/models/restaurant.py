from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship

from src.database.database_config import Base


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    cuisine_type = Column(String(255), nullable=False)
    culinary_style = Column(String(255), nullable=False)
    price_range = Column(String(255), nullable=False)
    restaurant_avatar = Column(String(255))

    # Foreign key references to other tables
    owner = relationship('User', back_populates='restaurants')
    coordinates = relationship('Coordinates', back_populates='restaurant', uselist=False)
    schedule = relationship('Schedule', back_populates='restaurant', uselist=False)
    address = relationship('Address', back_populates='restaurant', uselist=False)

class Coordinates(Base):
    __tablename__ = 'coordinates'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Relationship back to restaurant
    restaurant = relationship('Restaurant', back_populates='coordinates', uselist=False)

class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False, unique=True)
    week_open = Column(String(50), nullable=False)
    week_close = Column(String(50), nullable=False)
    weekend_open = Column(String(50), nullable=False)
    weekend_close = Column(String(50), nullable=False)

    # Relationship back with the restaurant
    restaurant = relationship('Restaurant', back_populates='schedule', uselist=False)

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False, unique=True)
    street_number = Column(String(255), nullable=True)
    route = Column(String(255), nullable=True)
    neighborhood = Column(String(255), nullable=True)
    sublocality_level1 = Column(String(255), nullable=True)
    administrative_area_level2 = Column(String(255), nullable=True)
    administrative_area_level1 = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    postal_code = Column(String(50), nullable=True)

    restaurant = relationship('Restaurant', back_populates='address', uselist=False)