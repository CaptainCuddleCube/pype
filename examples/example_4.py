from pype import sources, destinations, processors

c1 = sources.Constant("const a") | processors.Delay.apply(timeout=0.3)
c2 = sources.Constant("const b") | processors.Delay.apply(timeout=0.6)
sync = (
    processors.MergeStreams(c1, c2)
    | processors.Batch.apply(batch_size=3)
    | processors.Limit.apply(limit=3)
    | processors.AsyncToSync
)

for data in sync:
    print(data)
