import sys


class StdOut:
    def __init__(self, source):
        self._source = source
        self._file = sys.stdout

    async def run(self):
        async for data in self._source:
            print(data, file=self._file)


class StdErr(StdOut):
    def __init__(self, source):
        super().__init__(source)
        self._file = sys.stderr
