from fastapi import FastAPI

from router import api_router
from src import api


# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello Ana"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

def create_app() -> FastAPI:
    app = FastAPI(title="KataifBusinessCloud")
    app.include_router(api_router)

    return app

app = create_app()