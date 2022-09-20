[TOC]

# methods and interfaces

object is just a value or variable with methods (function associated with particular type). OO program uses methods to express the properties and operation of each data structure.

## methods

### declaration

```go
package geometry

type Point struct {X, Y float64}
// function
func distance(p, q Point) float64 {
    return math.Hypot(q.X-p.X, q.Y-p.Y)
}
// methods
func (p Point) distance(q Point) float64 {
    return math.Hypot(q.X-p.X, q.Y-p.Y)
}
p := Point{1, 2}
q := Point{2, 3}
fmt.Printf(p.distance(q))
```

`p` is the method's receiver (of distanceOO). also the function name can be the same as the first function is called `geometry.distance` and the second is called `Point.distance`. `p.distance` is called selector because it selects the appropriate method for the receiver for p. because of the name space difference we could technically have multiple distance methods for different struct/types without conflict. however its not acceptable to call `p.X` where X is an ambiguous method.

```go
type Path []Point
func (path Path) distance() float64 {
    sum := 0.0
    for i := range path {
        if i > 0 {
            sum += path[i-1].distance(path[i])
		}
    }
    return sum
}
```

`Path` is a named slice type instead of struct, but its still possible to define method for it. go is different from other OO languages, where it is possible to define behaviors for simple types eg. numbers, strings, slices, maps and even functions. methods can be declared on any named type defined in the same package as long as its underlying type is not pointer or an interface.

```go
perim := Path{
    {1, 1},
    {5, 1},
    {5, 4},
    {1, 1}
}
fmt.Pringln(perim.distance()) // 12
```

> note both distance methods is called to calculate the perimeter

### methods with a pointer receiver

if the argument is too large and we wish to avoid copying the value we can pass the address of the variable using pointer and the same goes to receiver variable

```go
func (p *Point) ScaleBy(factor float64) {
    p.X *= factor
    p.Y *= factor
}
```

by convention if any method has a pointer receiver, then all methods of of that named type should have a pointer receiver. note method declarations are not permitted on named type that are already pointer. go compiler can implicitly perform an `&p` on the variable, however it only works on variable.

```go
p.ScaleBy(2)
// the following is not possible
Point{1, 2}.ScaleBy(2) // not variable, non-addressable
// but its possible for
pointPtr.Distance(q) // Distance take in *Point receiver
(*pointPtr).Distance(q) // equivalent to
```

in short,

1. if the receiver argument has same type as receiver parameter, it works
2. if the receiver argument is a variable of type T and receiver parameter has type *T, it works
3. if receiver argument has type *T and receiver parameter has type T, it works

also if receiver type of T instead of *T, it is safe to copy instances of that type but if any method has pointer receiver, copying instances of T should be avoided.

### Nil as receiver value

```go
// linkedlist
type IntList struct{
    Value int
    Tail *IntList
}

func (list *IntList) Sum() int{
    if list == nil {
		return 0
    }
    return list.Value + list.Tail.Sum()
}
```

note the following differences between methods that allow nil as receiver value and methods that do not.

```go
m = nil
fmt.Println(m.Get("item"))  // get allows nil as receiver value, ""
m.Add("item", "2")  // panic: assignment to entry in nil map
```

`Add` will not compile because the type of `nil` has not been determined.

### Composing types by struct embedding

```go
type Point struct{X, Y float64}
type ColoredPoint struct {
    Point
    Color color.RGBA
}
// we can do the following
var p, q ColoredPoint
// ... declaration
q.ScaleBy(2)
q.Distance(q.Point)
q.Distance(p) // compile error
```

`ColorPoint` is not a `Point` but has one. there is no way for the method to access a `Point` within a `ColorPoint` from a `ColorPoint`.
