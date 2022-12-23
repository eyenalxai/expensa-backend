from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.config_reader import app_config
from app.routes.auth_route import auth_router
from app.routes.user_route import user_router


def initialize_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(user_router)

    return app
