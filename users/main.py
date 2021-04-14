import asyncio
import json
# import requests
import typer

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.base import init_models
from src import products


origins = [
        "http://localhost:3000"
        ]


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(products.router,
                               prefix="/api/products", tags=["products"])
    application.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    return application


app = create_application()
cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


if __name__ == "__main__":
    cli()
