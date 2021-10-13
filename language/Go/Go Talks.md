[TOC]

# Go Talks

## common mistakes in Go to avoid

[talk by steve francia](https://www.youtube.com/watch?v=29LLRKIL_TI&ab_channel=DataCouncil)

1. not accepting interfaces
2. not using `Io.Reader` and `Io.Writer`
3. requiring broad interfaces
4. methods vs functions (functions can accept interface as input?)
5. pointers vs values (share access not because to optimize performance, also pointers are not safe for concurrent access)
6. thinking of errors as strings (it is an interface)
7. building package and not considering concurrency (data structures are not concurrency safe, use sync package to ensure value is safe though atomic operation and mutex and channels to coordinate value across go routines by permitting one go routine to access at at time; though there is also reason to be unsafe which is being flexible for users)

```go
var ErrNoName = errors.New("zero length page name") // custom error type for context

// such that later on we can do 

if err == ErrNoName {
    // some code here
} else {
    log.FatalF(err)
}

// custom error example

if serr != nil {
    if serr, ok := serr.(*PathError); ok && serr.Err == syscall.ENOTDIR {
		return nil
    }
    return serr
}
```

reference: [afero](https://github.com/spf13/afero), [container from scratch](https://github.com/lizrice/containers-from-scratch), [golang perf](https://github.com/golang/perf)

## Simulating A Real-World System In Go

[coffee shop](https://www.youtube.com/watch?v=jJS6G7irZSc&ab_channel=CodingTech)

reference: [github](https://github.com/Sajmani/dotgo/tree/master/coffee)

## The Why of Go

[carmen andoh qconsf](https://www.youtube.com/watch?v=bmZNaUcwBt4&ab_channel=InfoQ)

a search of answers in [this article](https://talks.golang.org/2012/splash.article)

green threads decision: user level process, allocated from heap instead of stack created by os - go routines. events, threads and Go routines where Nginx is an event loop plus state machine model (also nodejs, syscall hurts) tailing latency and go's GC. memory locality.

### readability

> you are not paid to program, you are not even paid to maintain someone else's program, you are paid to deliver solution to the business - Dave Cheney

also

> if you can't be replaced, you cannot be promoted.

on engineering

> engineering is what happens when things need to live longer and influence of time starts creeping in. - Titus Winters