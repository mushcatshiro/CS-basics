[TOC]

# goroutines and concurrency

## goroutines and channels

> Don't communicate by sharing memory; share memory by communicating.

Go enables two styles of concurrent programming, where goroutines and channels supports CSP, a model of concurrency in which values are passed between independent goroutines but variables are for the most part confined to a single activity. another approach which is the traditional model of shared memory multithreading.

in a program that have two function and neither of them calls the other, a sequential approach may call one after another, but a concurrent program with two or more goroutines call both at the same time. when a go program starts, a single goroutine is called on the `main` function and new goroutines are called by the `go` statement.

```go
f()  // call f; wait for return
go f()  // create a new goroutine that calls f; not waiting
```

