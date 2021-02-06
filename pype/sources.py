import httpx
import sys
from typing import Any
from .base import Base


class HttpSource(Base):
    def __init__(self, url: str, headers: dict = None, parameters: dict = None):
        self._url = url
        self._headers = headers
        self._parameters = parameters

    async def get_data(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=self._url, params=self._parameters, headers=self._headers
            )
        return str(resp.content)


class ConstantSource(Base):
    def __init__(self, constant: Any):
        self._constant = constant

    async def get_data(self):
        return self._constant


class StdIn(Base):
    async def get_data(self):
        if sys.stdin.closed:
            raise StopAsyncIteration()
        data = "".join([line for line in sys.stdin])
        if data == "":
            raise StopAsyncIteration()
        return data
