import os

from app import create_app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        port=int(os.getenv("BACKEND_PORT", "5000")),
        debug=os.getenv("APP_DEBUG", "false").lower() == "true",
    )
