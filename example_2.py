import asyncio
from pype import sources, destinations, processors
from functools import partial


async def main():
    c1 = sources.ConstantSource("const a") | partial(processors.Delay, timeout=0.3)
    c2 = sources.ConstantSource("const b") | partial(processors.Delay, timeout=0.6)
    merged = (
        processors.MergeStreams(c1, c2)
        | partial(processors.Batch, batch_size=3)
        | partial(processors.Limit, limit=3)
    )
    async for data in merged:
        print(data)


asyncio.run(main())
