import json
import os
import sys

from fastapi import FastAPI
from fastapi.logger import logger
from pydantic_settings import BaseSettings

from cointracker.lib.services.user_service import UserService

app = FastAPI()


class Settings(BaseSettings):
    BASE_URL: str = "http://localhost:8000"
    USE_NGROK: bool = os.environ.get("USE_NGROK", "False") == "True"


settings = Settings()


def init_webhooks(base_url: str):
    pass


if settings.USE_NGROK:
    from pyngrok import ngrok

    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8000"

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    print('ngrok tunnel "{}" -> "http://127.0.0.1:{}"'.format(public_url, port))

    settings.BASE_URL = public_url
    init_webhooks(public_url)


@app.get("/users/wallet_address")
async def create_user_wallet_address_mapping(user_id: int):
    data = UserService.get_wallet_metadata(
        user_id=user_id,
    )
    result = {}
    for key in data:
        result[key] = data[key].__dict__
    return json.dumps(result, default=str)


@app.post("/users/wallet_address/")
async def create_user_wallet_address_mapping(user_id: int, wallet_address: str):
    UserService.add_wallet_address(
        user_id=user_id,
        wallet_address=wallet_address,
    )


@app.delete("/users/wallet_address/")
async def remove_user_wallet_address_mapping(user_id: int, wallet_address: str):
    UserService.remove_wallet_address(
        user_id=user_id,
        wallet_address=wallet_address,
    )


@app.get("/users/transactions")
async def get_user_transactions(user_id: int, limit: int = 50, offset: int = 0):
    data = UserService.get_transactions(
        user_id=user_id,
        limit=limit,
        offset=offset,
    )
    result = {}
    for key in data:
        result[key] = [e.__dict__ for e in data[key]]
    return json.dumps(result, default=str)


@app.post("/users/transactions")
async def sync_user_transactions(user_id: int, limit: int = 100):
    UserService.synchronize_transactions(
        user_id=user_id,
        limit=limit,
    )
