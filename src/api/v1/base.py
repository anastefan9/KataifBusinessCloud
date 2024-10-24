from fastapi import APIRouter

base_router = APIRouter()

@base_router.get("/")
async def root():
    return {"message": "Hello, Ana!"}


@base_router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}