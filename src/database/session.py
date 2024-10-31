from src.database.database_config import engine, SessionLocal
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi import FastAPI, HTTPException, Depends

from src.models import user, refresh_token, restaurant

# we will create the dependency for our db

user.Base.metadata.create_all(bind=engine)
refresh_token.Base.metadata.create_all(bind=engine)
restaurant.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# we will create an annotation for our db

db_dependency = Annotated[Session, Depends(get_db)]