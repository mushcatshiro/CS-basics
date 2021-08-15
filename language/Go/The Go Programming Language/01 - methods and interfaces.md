[TOC]

# methods and interfaces

object is just a value or variable with methods (function associated with particular type). OO program uses methods to express the properties and operation of each data structure.

## methods

### declaration

```go
type Point struct {X, Y float64}
// function
func distance(p, q Point) float64 {
    return math.Hypot(q.X-p.X, q.Y-p.Y)
}
// methods
func (p Point) distanceOO(q Point) float64 {
    return math.Hypot(q.X-p.X, q.Y-p.Y)
}
p := Point{1, 2}
q := Point{2, 3}
fmt.Printf(p.distanceOO(q))
```

`p` is the method's receiver (of distanceOO)