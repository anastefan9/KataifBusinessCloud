from typing import Optional

from pydantic import BaseModel

# we send this restaurant_base model to the DB

class Coordinates(BaseModel):
    latitude: float
    longitude: float

    class Config:
        orm_mode = True

class Schedule(BaseModel):
    week_open: str
    week_close: str
    weekend_open: str
    weekend_close: str

    class Config:
        orm_mode = True

class Address(BaseModel):
    street_number: Optional[str] = None
    route: Optional[str] = None
    neighborhood: Optional[str] = None
    sublocality_level1: Optional[str] = None
    administrative_area_level2: Optional[str] = None
    administrative_area_level1: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

    class Config:
        orm_mode = True

class RestaurantResponseBase(BaseModel):
    id: int
    owner_id: int
    name: str
    cuisine_type: str
    culinary_style: str
    price_range: str
    coordinates: Coordinates
    address: Address
    schedule: Schedule
    restaurant_avatar: str

    class Config:
        orm_mode = True