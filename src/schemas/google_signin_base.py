from datetime import datetime

from pydantic import BaseModel

from src.schemas.user_base import UserBase


class GoogleAuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires_in: int

class RefreshAccessToken(BaseModel):
    access_token: str

class GoogleUser(BaseModel):
    idToken: str
    id: str
    familyName: str
    givenName: str
    profilePictureUri: str