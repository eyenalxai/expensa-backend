import uvicorn

from app.config.config_reader import app_config
from app.initialize import initialize_app

if __name__ == "__main__":
    app = initialize_app()
    uvicorn.run(app, host=app_config.host, port=app_config.port)
