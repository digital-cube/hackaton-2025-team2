from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.config import init_db, get_tortoise_orm_config, close_db
from src.utils.fastapi_utils import load_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_services(app)
    await init_db(app)
    yield
    await close_db()
app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)
origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TORTOISE_ORM = get_tortoise_orm_config()

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8069, reload=True)