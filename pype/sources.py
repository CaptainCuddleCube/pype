import asyncio
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
            raise StopAsyncIteration
        try:
            data = next(sys.stdin)
        except StopIteration as stdin_err:
            raise StopAsyncIteration from stdin_err
        return data


class SubProcess(Base):
    def __init__(self, *commands, stop_on_error=False):
        self._proc = asyncio.create_subprocess_exec(
            *commands, stdout=asyncio.subprocess.PIPE
        )
        self._stop_on_error = stop_on_error

    async def get_data(self):
        err = self._proc.stderr.readlin()
        if err != b"" and self._stop_on_error or self._proc.stdout.at_eof():
            raise StopAsyncIteration
        return await self._proc.stdout.readline()
