# pype

pype is a super simple, asynchronous, generator based library that makes it easy
for you to create pipelines of data.

This is still very much an experimental work, and has been made out of curiosity.
I would like any and all feedback!

## Installation

All you will need to do is pip install this is:

```
pip install -e git+git@github.com:CaptainCuddleCube/pype.git#egg=pype
```

## About pype's Async Pipelines

pype is broken down into three components:

- Sources
- Processors
- Destinations

Each of these perform slightly, but importantly, different tasks.

### Sources

Sources can be seen where data arrives from. These could be stdin, or responses
from an API. The main point with a source, is that it creates an async generator,
that can be iterated over.

### Processors

These accept a generator (or a collection of generators), perform a process on
the data from that generator, and then return that data in a new generator.
Effectively, processors are where you would focus your data transformation.

There are special processors which maintain the flow of data. Some will _merge_
the results of two or more other data streams, others convert the data stream from
asynchronous to synchronous (useful if you want this running in production code).

### Destinations

These can be seen as where data streams are being funneled too. Destinations will
automatically try and deplete / iterate over a given async generator, and funnel
this data out somewhere else.

### Putting it all together

pype has some friendly syntax to make building pipelines easier, and more expressive.

#### The pipe operator (`|`)

The first trick, is the pipe ( `|` ) operator. This operator allows you to take an
existing pype generator, and add another generator to the tail. When you use the
pipe syntax, the pype generator to the left of the `|` must be a class, since we
are essentially instantiating a new class!

**example 1:**

```python
from pype import sources, destinations
pipeline = sources.Constant('foo') | destinations.StdOut
await pipeline.run()
```

In example 1, we create a constant source, and we sending all the data in it to
std-out! We are leaving the `|` operator to handle the instantiation for us. In
order to actually run the pipeline, we need to invoke it with `.run()`, and we
need to await the coroutine.

**example 2:**

```python
from pype import sources, destinations, processors
pipeline = sources.Constant('foo') | processors.Delay.apply(timeout=0.5) | destinations.StdOut
await pipeline.run()
```

In example 1, we created a pipeline the spewed a `foo` to std-out as fast as we
could generate it. What if we wanted to slow things down a bit? We can use the
processor `Delay`, which just pauses the stream for a defined amount of time
before passes the streamed data on. Since we need to define the `timeout`, we have
to use a special class method call `apply`, which sets the `args` and `kwargs`
when the class is instantiated.

It's also possible to use Python's `functool.partial` function to wrap the pype
generator class!

## Motivation

I was rather curious about creating simple Python code flows using Python async-
generators. Ideally, if you have a lot of simple and expressive generators, you
can craft easy to test pipelines. I noticed that I started following a similar
pattern when working with a FastAPI and other Python asynchronous code - you want
to form lazy coroutines, and push any and all compute out to some other process.
This project is taking that to the extreme.
