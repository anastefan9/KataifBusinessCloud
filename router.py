from fastapi import APIRouter

from src.api.v1.base import base_router
from src.api.v1.google_signin import google_signin_router

api_router = APIRouter()

api_router.include_router(base_router)
api_router.include_router(google_signin_router)