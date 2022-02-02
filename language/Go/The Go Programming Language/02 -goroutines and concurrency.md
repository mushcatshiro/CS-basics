[TOC]

# goroutines and concurrency

## goroutines and channels

### goroutines

> Don't communicate by sharing memory; share memory by communicating.

Go enables two styles of concurrent programming, where goroutines and channels supports CSP, a model of concurrency in which values are passed between independent goroutines but variables are for the most part confined to a single activity. another approach which is the traditional model of shared memory multithreading.

in a program that have two function and neither of them calls the other, a sequential approach may call one after another, but a concurrent program with two or more goroutines call both at the same time. when a go program starts, a single goroutine is called on the `main` function and new goroutines are called by the `go` statement.

```go
f()  // call f; wait for return
go f()  // create a new goroutine that calls f; not waiting
```

one can now safely assume goroutine as thread, and the main differences will be discussed later. in the fib spinner example, the spinner spins (in a goroutine) while recursive fib is being processed. other than returning from `main` or exiting the program, there is no way for one goroutine to stop another.

```go
for {
  conn, err := listener.Accept()
  if err != nil {
    log.Print(err) // e.g., connection aborted
    continue
  }
  go handleConn(conn) // with the addition of go, now it handles connections concurrently, else sequentially
}
```

### channels

channel connects goroutines and allows one goroutine to send values to another. channel can only sends a specific type (declared). a channel is a reference to the data structure created by `make`. this allows the caller and callee refer to the same data structure. the zero value of a channle is `nil`. channels are comparable, and is true when both reference refers to the same data structure.

```go
ch := make(chan int) // int channel
```

channels can send and receive using the `<-` operator

```go
ch <- x // send
x = <- ch // receive and assign
<- ch // receive and drop
```

after a channel is closed with `close(ch)`, any further send attempts will cause panic, and any receive attempts will yield values that have been sent until no more values left and receive the zero value of the channel's type.

#### unbufferend channels

```go
ch = make(chan int)
// or
ch = make(chan int, 0)
```

communicating over an unbuffered channel causes the sending and receiving goroutines to synchronize. this means that either operation (send or receive) will be blocked until the corresponding operation is being perform by another goroutine before both of them may continue.
