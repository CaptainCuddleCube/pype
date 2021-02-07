import asyncio
from pype import sources, destinations, processors

"""
using the pype syntax
"""

c1 = sources.ConstantSource("const a").pype(processors.Delay, timeout=0.3)
c2 = sources.ConstantSource("const b").pype(processors.Delay, timeout=0.6)
sync = (
    processors.MergeStreams(c1, c2)
    .pype(processors.Batch, batch_size=3)
    .pype(processors.Limit, limit=3)
    | processors.AsyncToSync
)

for data in sync:
    print(data)
