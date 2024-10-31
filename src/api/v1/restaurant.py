import json
import os
import uuid
from typing import List
from urllib.parse import urlunparse

from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException, Request
from httpx import request
from sqlalchemy.orm import Session, joinedload
from starlette.staticfiles import StaticFiles


from src.database.session import get_db
from src.models.restaurant import Restaurant, Coordinates, Schedule, Address
from src.schemas.restaurant_base import RestaurantResponseBase

restaurant_router = APIRouter()

UPLOAD_DIRECTORY = "images"

BASE_URL = f"http://127.0.0.1:8090"

@restaurant_router.post("/restaurant/add_restaurant")
async def add_restaurant(
        restaurantData: str = Form(...),
        avatarImage: UploadFile = File(...),
        db: Session = Depends(get_db)
) :
    # Step 1: Parse the Json Data
    try:
        restaurant_dict = json.loads(restaurantData)
    except json.JSONDecodeError:
        return {"message": "Invalid JSON data"}

    # Step 2: Save the avatar image to the file system
    filename = f"{uuid.uuid4()}_{avatarImage.filename}"
    image_path = os.path.join(UPLOAD_DIRECTORY, filename)
    with open(image_path, "wb") as buffer:
        buffer.write(avatarImage.file.read())

    image_url = f"{BASE_URL}/{image_path}"

    # Step 3: save data in the DB
    restaurant = Restaurant(
        owner_id = restaurant_dict["owner_id"],
        name = restaurant_dict["name"],
        cuisine_type = restaurant_dict["cuisine_type"],
        culinary_style = restaurant_dict["culinary_style"],
        price_range = restaurant_dict["price_range"],
        restaurant_avatar = image_url
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    coordinates_data = restaurant_dict["coordinates"]
    coordinates = Coordinates(
        restaurant_id=restaurant.id,
        latitude=coordinates_data["latitude"],
        longitude=coordinates_data["longitude"]
    )
    db.add(coordinates)
    db.commit()

    schedule_data = restaurant_dict["schedule"]
    schedule = Schedule(
        restaurant_id=restaurant.id,
        week_open=schedule_data["week_open"],
        week_close=schedule_data["week_close"],
        weekend_open=schedule_data["weekend_open"],
        weekend_close=schedule_data["weekend_close"],
    )
    db.add(schedule)
    db.commit()

    address_dict = restaurant_dict["address"]
    address = Address(
        restaurant_id=restaurant.id,
        street_number=address_dict.get("street_number"),
        route=address_dict.get("route"),
        neighborhood=address_dict.get("neighborhood"),
        sublocality_level1=address_dict.get("sublocality_level1"),
        administrative_area_level2=address_dict.get("administrative_area_level2"),
        administrative_area_level1=address_dict.get("administrative_area_level1"),
        country=address_dict.get("country"),
        postal_code=address_dict.get("postal_code"),
    )
    db.add(address)
    db.commit()

    return {"message": "Successfully added restaurant"}


@restaurant_router.get("/restaurant/get_restaurant/{owner_id}")
async def get_restaurant(
        owner_id: int,
        db: Session = Depends(get_db)
) -> List[RestaurantResponseBase] :
    restaurants = (
        db.query(Restaurant)
        .options(
            joinedload(Restaurant.coordinates),
            joinedload(Restaurant.address),
            joinedload(Restaurant.schedule)
        )
        .filter(Restaurant.owner_id == owner_id)
        .all()
    )
    db.close()

    if not restaurants:
        raise HTTPException(status_code=404, detail="Not Found")

    return restaurants

