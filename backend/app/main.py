import os

print(f"\nDIRECTORY: {os.getcwd()}\n")
print(f"\nELEMENTS: {os.listdir()}\n")

from platform import python_version

from api.route_base import api_router

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


def init_app():
    app = FastAPI()
    app.include_router(api_router)

    allowed_origins = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:8000"
    ).split(",")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


print("Python Version:", python_version())
app = init_app()
