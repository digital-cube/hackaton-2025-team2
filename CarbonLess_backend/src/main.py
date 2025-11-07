from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.utils.config import init_db, get_tortoise_orm_config
from src.utils.fastapi_utils import load_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_services(app)
    await init_db(app)
    yield
app = FastAPI(lifespan=lifespan)

TORTOISE_ORM = get_tortoise_orm_config()

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)