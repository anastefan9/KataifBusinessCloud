import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from router import api_router
from src import api


def create_app() -> FastAPI:
    app = FastAPI(title="KataifBusinessCloud")
    app.include_router(api_router)

    UPLOAD_DIRECTORY = "images"
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.mkdir(UPLOAD_DIRECTORY)
    app.mount("/images", StaticFiles(directory=UPLOAD_DIRECTORY), name="images")

    return app

app = create_app()