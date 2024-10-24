from datetime import datetime, timedelta

from dns.dnssecalgs import algorithms
import jwt
from google.oauth2 import id_token
from sqlalchemy.orm import Session
from google.auth.transport import requests
from decouple import config
from fastapi import Depends, FastAPI, HTTPException
from src.models import user, refresh_token
from src.schemas.google_signin_base import GoogleUser, GoogleAuthResponse
from src.schemas.user_base import UserBase

google_client_id = config("GOOGLE_CLIENT_ID")

def create_user(db: Session, email: str, first_name, last_name, profile_image):
    user_data = user.User(email=email, first_name=first_name, last_name=last_name, profile_image=profile_image)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data

def get_user(db: Session, email: str):
    return db.query(user.User).filter(user.User.email == email).first()

def verify_google_id_token(google_id_token: str):
    try:
        id_info =id_token.verify_oauth2_token(google_id_token, requests.Request(), google_client_id)

        return id_info
    except ValueError:
        raise HTTPException(status_code=400, detail="Could not validate Google ID token.")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config("SECRET_KEY"))
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=10)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config("SECRET_KEY"))
    return encoded_jwt, expire

def store_refresh_token(refresh_token_str: str, db: Session, user_id: int, expire_date: datetime):
    token = refresh_token.RefreshToken(refresh_token=refresh_token_str, user_id=user_id, expires_in=expire_date)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, config("SECRET_KEY"))
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

def get_refresh_token(token: str, db: Session):
    return db.query(refresh_token.RefreshToken).filter(refresh_token.RefreshToken == token).first()

def delete_refresh_token(token: str, db: Session):
    try:
        print(f"Token type: {type(token)}")
        token = db.query(refresh_token.RefreshToken).filter(refresh_token.RefreshToken == token).first()
        if not token:
            raise HTTPException(status_code=401, detail="Token not found")

        db.delete(token)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete token")

