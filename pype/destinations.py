import sys

from .base import Base


class StdOut(Base):
    def __init__(self, source):
        self._source = source

    async def get_data(self):
        data = await self._source.__anext__()
        print(data, file=sys.stdout)


class StdErr(StdOut):
    async def get_data(self):
        data = await self._source.__anext__()
        print(data, file=sys.stderr)
