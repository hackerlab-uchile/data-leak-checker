from fastapi import APIRouter

# from apis import (
#     route_auth,
#     route_users,
#     route_categories,
#     route_challenges,
#     route_licenses,
#     route_projects,
#     route_properties,
# )

api_router = APIRouter()


@api_router.get("/")
def index():
    return {"message:", "Hello World!"}


# api_router.include_router(route_auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(route_auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(route_users.router, prefix="/users", tags=["users"])
