"""Main entrypoint for the API."""
import logging

import uvicorn
from api.bootstrap import bootstrap_di
from api.sensors.routes import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def main():
    logging.basicConfig(level=logging.INFO)
    app = FastAPI()
    origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:4200",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        router, tags=["sensors", "temperature", "humidity"], prefix="/sensors")
    uvicorn.run(app, host="0.0.0.0", port=8000,
                log_level="info", proxy_headers=True)


if __name__ == "__main__":
    bootstrap_di()
    main()
