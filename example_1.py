import asyncio
from pype import sources, destinations, processors
from functools import partial


async def main():
    pl = sources.StdIn() | partial(processors.Delay, timeout=0.8) | destinations.StdErr
    async for _ in pl:
        pass


asyncio.run(main())
