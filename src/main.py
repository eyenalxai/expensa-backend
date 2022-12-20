"""Main entry point for the application."""

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings.settings_reader import base_settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=base_settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=base_settings.port)
