from fastapi import APIRouter

from api import route_breach

api_router = APIRouter()


@api_router.get("/")
def index():
    """Hello World!"""
    return {"message:", "Hello World!"}


api_router.include_router(route_breach.router, prefix="/breach", tags=["breach"])
