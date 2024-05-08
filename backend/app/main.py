import os

import init_db
from api.route_base import api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from populate_db import populate_dummy_data


def init_app():
    """Inits the application"""
    new_app = FastAPI(root_path="/api")
    new_app.include_router(api_router)

    allowed_origins = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:8000"
    ).split(",")

    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return new_app


app = init_app()

populate_dummy_data()
