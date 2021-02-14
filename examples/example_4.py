from pype import sources, destinations, processors

c1 = sources.Constant("const a") | processors.Delay.with_args(timeout=0.3)
c2 = sources.Constant("const b") | processors.Delay.with_args(timeout=0.6)
sync = (
    processors.MergeStreams(c1, c2)
    | processors.Batch.with_args(batch_size=3)
    | processors.Limit.with_args(limit=3)
    | processors.AsyncToSync
)

for data in sync:
    print(data)
