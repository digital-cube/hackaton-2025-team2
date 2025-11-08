from typing import Literal
import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport
from tortoise import Tortoise

from utils.config import init_db
from utils.fastapi_utils import load_services


@pytest.mark.asyncio
class TestBase:
    app: FastAPI = None

    async def setup(self):
        load_services(self.app)
        await init_db(self.app)
    async def teardown(self): ...

    @pytest_asyncio.fixture(autouse=True, scope="function")
    async def setup_fixture(self) -> None:
        from src.main import app
        from src.utils.config import init_db

        self.app = app

        # Initialize database
        await init_db(self.app)

        await self.setup()
        yield
        await self.teardown()

        # Close database connections
        await Tortoise.close_connections()

    async def request(
        self,
        method: Literal['get', 'post', 'put', 'patch', 'delete'],
        path: str,
        json_data: dict = None,
        query_params: dict = None,
        headers: dict = None,
        files: dict = None,
        data: dict = None,
    ):
        async with httpx.AsyncClient(transport=ASGITransport(app=self.app), base_url="http://test") as client:
            func = getattr(client, method, None)

            if not func:
                raise Exception(f'Invalid method: {method}')

            if method in ('get', 'delete'):
                response = await func(url=path, params=query_params, headers=headers)
            else:

                kwargs = {'url': path, 'params': query_params, 'headers': headers}
                if files is not None:
                    kwargs['files'] = files
                if json_data is not None:
                    kwargs['json'] = json_data
                if data is not None:
                    kwargs['data'] = data

                response = await func(**kwargs)

            return response