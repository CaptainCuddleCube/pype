import asyncio
from typing import AsyncGenerator

from .base import Base, SyncBase


class Delay(Base):
    def __init__(self, source: AsyncGenerator, *, timeout: int):
        self._timeout = timeout
        self._source = source

    async def get_data(self):
        await asyncio.sleep(self._timeout)
        return await self._source.__anext__()


class AddPrefix(Base):
    def __init__(self, source: AsyncGenerator, *, prefix: str):
        self._source = source
        self._prefix = prefix

    async def get_data(self):
        data = await self._source.__anext__()
        return f"{self._prefix}{data}"


class MergeStreams(Base):
    def __init__(self, *generators: AsyncGenerator):
        self._gens = generators
        self._index = 0

    async def get_data(self):
        data = await self._gens[self._index].__anext__()
        self._index = (self._index + 1) % len(self._gens)
        return data


class RaceToMergeStreams(Base):
    def __init__(self, *generators: AsyncGenerator):
        self._gens = generators
        self._data = {}
        self._pending = {}

    async def get_data(self):
        if len(self._data) == 0:
            if len(self._pending) == 0:
                self._pending = {i.__anext__() for i in self._gens}
            self._data, self._pending = await asyncio.wait(
                self._pending, return_when=asyncio.FIRST_COMPLETED
            )
        return self._data.pop().result()


class GatherAll(Base):
    def __init__(self, *generators: AsyncGenerator):
        self._gens = generators

    async def get_data(self):
        return asyncio.gather([i for i in self._gens])


class Race(Base):
    """
    Allows you to return data from one of the generators.
    """

    def __init__(self, *generators: AsyncGenerator):
        self._gens = generators

    async def get_data(self):
        done, pending = await asyncio.wait(
            {i.__anext__() for i in self._gens}, return_when=asyncio.FIRST_COMPLETED
        )
        for i in pending:
            i.cancel()
        return [i.result() for i in done]


class Batch(Base):
    def __init__(self, source: AsyncGenerator, *, batch_size: int):
        self._source = source
        self._batch_size = batch_size

    async def get_data(self):
        return [await self._source.__anext__() for i in range(self._batch_size)]


class Limit(Base):
    def __init__(self, source: AsyncGenerator, *, limit: int):
        self._source = source
        self._limit = limit
        self._count = 0

    async def get_data(self):
        if self._count == self._limit:
            raise StopAsyncIteration(f"Reached set limit of {self._limit} iterations")
        self._count += 1
        return await self._source.__anext__()


class AsyncToSync(SyncBase):
    def __init__(self, source: AsyncGenerator):
        self._source = source
        self._loop = asyncio.new_event_loop()

    def get_data(self):
        try:
            return self._loop.run_until_complete(self._source.__anext__())
        except StopAsyncIteration as async_iteration_stopped:
            raise StopIteration from async_iteration_stopped
