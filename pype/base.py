from functools import partial


class Base:
    async def get_data(self):
        raise NotImplementedError("Please fill this out")

    async def __anext__(self):
        return await self.get_data()

    def __aiter__(self):
        return self

    def __or__(self, other):
        return other(self)

    @classmethod
    def apply(cls, *args, **kwargs):
        return partial(cls, *args, **kwargs)


class SyncBase:
    def get_data(self):
        raise NotImplementedError("Please fill this out")

    def __next__(self):
        return self.get_data()

    def __iter__(self):
        return self

    def __or__(self, other):
        return other(self)

    @classmethod
    def apply(cls, *args, **kwargs):
        return partial(cls, *args, **kwargs)
