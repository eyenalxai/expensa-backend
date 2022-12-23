import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes.auth import auth_router
from routes.user import user_router
from settings.settings_reader import base_settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=base_settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=base_settings.port)
