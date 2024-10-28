from datetime import datetime
from http.client import HTTPException

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from src.database.session import get_db
from src.schemas.google_signin_base import GoogleUser, GoogleAuthResponse, RefreshAccessToken
from src.schemas.user_base import UserBase
from src.services.google_signin_service import verify_google_id_token, get_user, create_user, create_access_token, \
    create_refresh_token, store_refresh_token, delete_refresh_token, verify_token, get_refresh_token

google_signin_router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 180

@google_signin_router.post("/auth/verify_google_token")
async def verify_google_token(
        user: GoogleUser,
        db: Session= Depends(get_db)
) -> GoogleAuthResponse:
    try:
        verify_google_id_token(user.idToken)

        user_email = user.id
        user_first_name = user.givenName
        user_last_name = user.familyName
        user_profile_image = user.profilePictureUri

        user = get_user(db, user_email)
        if not user:
            user = create_user(db, user_email, user_first_name, user_last_name, user_profile_image)

        access_token = create_access_token(data={"sub": user.email})
        refresh_token, expire_date = create_refresh_token(data={"sub": user.email})
        store_refresh_token(refresh_token, db=db, user_id=user.id, expire_date=expire_date)
        print(user_profile_image)
        print(user.profile_image)

        user_data = UserBase.model_validate(user)

        return GoogleAuthResponse(access_token=access_token, refresh_token=refresh_token, access_token_expires_in=ACCESS_TOKEN_EXPIRE_MINUTES*60, user=user_data)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid OAuth2 token.")


security = HTTPBearer()

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing token",
        )
    return token

@google_signin_router.get("/auth/logout")
async def logout(token: str = Depends(get_token), db: Session = Depends(get_db)):
    try:
        success = delete_refresh_token(token, db=db)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete refresh token")
        return {"message": "Logged out successfully"}
    except IndexError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed Authorization header.")
    except Exception as e:
        print(f"Error during logout: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Logout failed due to internal server error.")


@google_signin_router.post("/auth/refresh")
async def refresh(refresh_token: str, db: Session = Depends(get_db)) -> RefreshAccessToken:
    token = verify_token(refresh_token)

    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found.")

    user_id = token["sub"]

    stored_token = get_refresh_token(refresh_token, db=db)
    if stored_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token.")

    if stored_token.expire_date < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired.")

    access_token = create_access_token(data={"sub": user_id})

    return RefreshAccessToken(access_token=access_token)