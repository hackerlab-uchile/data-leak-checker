from api import route_breach, route_verify
from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/")
def index():
    """Hello World!"""
    return {"message:", "Hello World!"}


api_router.include_router(route_breach.router, prefix="/breach", tags=["breach"])
api_router.include_router(route_verify.router, prefix="/verify", tags=["verify"])
