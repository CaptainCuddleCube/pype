class Base:
    async def get_data(self):
        raise NotImplementedError("Please fill this out")

    async def __anext__(self):
        return await self.get_data()

    def __aiter__(self):
        return self

    def __or__(self, other):
        return other(self)
