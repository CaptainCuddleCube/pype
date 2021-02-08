import asyncio
from pype import sources, destinations, processors
from functools import partial

"""
An example of having a the pipeline appear to be synchronous, by using an
adapter!
"""

c1 = sources.Constant("const a") | partial(processors.Delay, timeout=0.3)
c2 = sources.Constant("const b") | partial(processors.Delay, timeout=0.6)
sync = (
    processors.MergeStreams(c1, c2)
    | partial(processors.Batch, batch_size=3)
    | partial(processors.Limit, limit=3)
    | processors.AsyncToSync
)

for data in sync:
    print(data)
