import importlib

from fastapi import FastAPI
from tortoise import Tortoise

from src.utils.env import DB
from src.utils.path import get_services


async def init_db(app: FastAPI):
    await Tortoise.init(config = get_tortoise_orm_config())
    await Tortoise.generate_schemas()
def get_tortoise_orm_config():
    services_path = get_services()
    models_list = ['aerich.models']

    for service in services_path.iterdir():
        if service.is_dir() and service.name != "__pycache__":
            handlers_file = service / "models" / "models.py"
            if handlers_file.exists():
                try:
                    module_name = f"src.services.{service.name}.models.models"
                    module = importlib.import_module(module_name)
                    if module:
                        models_list.append(module_name)
                        print(f'Added models for {service.name.upper()}')
                except Exception as e:
                    print(f'{service.name.upper()} has no models.')
            else:
                print(f'{service.name.upper()} has no models.')

    # "engine": "tortoise.backends.sqlite",
    # "credentials": {
    #     "file_path": "db.sqlite3"
    # }

    TORTOISE_ORM = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "host": DB.HOST,
                    "port": DB.PORT,
                    "user": DB.USERNAME,
                    "password": DB.PASSWORD,
                    "database": DB.NAME,
                }
            }
        },
        "apps": {
            "models": {
                "models": models_list,
                "default_connection": "default",
            }
        }
    }

    return TORTOISE_ORM

async def close_db():
    await Tortoise.close_connections()