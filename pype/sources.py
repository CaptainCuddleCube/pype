import asyncio
import sys
from typing import Any

import asyncpg
import httpx

from .base import Base


class Http(Base):
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


class Constant(Base):
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


class PostgresQuery(Base):
    """
    Creates a stream of data from a PostgreSQL database. While records are
    returned one by one, there is a prefetch argument which allows for the
    number of rows fetched from the database to be fetched first.
    """

    def __init__(
        self,
        query,
        user,
        password,
        database,
        host,
        port=5432,
        prefetch_size=None,
        data_type=dict,
    ):
        self._query = query
        self._prefetch_size = prefetch_size
        self._conn_details = dict(
            user=user, password=password, database=database, host=host, port=port
        )
        self._data_gen = None
        if data_type != dict or data_type != tuple:
            raise ValueError("The only data types allowed are dictionaries and tuples.")
        self._data_type = data_type

    async def _query_gen(self):
        conn = await asyncpg.connect(**self._conn_details)
        async with conn.transaction():
            async for record in conn.cursor(self._query, prefetch=self._prefetch_size):
                yield self._data_type(record)
        await conn.close()

    def reset_stream(self):
        self._data_gen = None

    async def get_data(self):
        if self._data_gen is None:
            self._data_gen = self._query_gen()
        return await self._data_gen.__anext__()


class PostgresBatchQuery(PostgresQuery):
    def __init__(
        self,
        query,
        user,
        password,
        database,
        host,
        port=5432,
        data_type=dict,
        batch_size=None,
    ):
        super().__init__(
            query, user, password, database, host, port, data_type=data_type
        )
        self._batch_size = batch_size

    async def _query_gen(self):
        conn = await asyncpg.connect(**self._conn_details)
        async with conn.transaction():
            cur = await conn.cursor(self._query)
            while not cur._exhausted:
                tmp_data = await cur.fetch(self._batch_size)
                yield [self._data_type(i) for i in tmp_data]
        await conn.close()
