[TOC]

# The Basics

Go

- is compiled
- handles Unicode natively
- comes with toolbox (git, compiler and etc.)
- tabs instead of spaces
- variable implicitly declared are set to zero value of its type
- `:=` is a short variable declaration
- does not permit unused local variable, thus use `_` as an blank identifier
- uses camel case

```go
package main // package declaration
```

package `main` is special because it defines a standalone executable program instead of a library, and function `main` is where the program starts. whatever `main` does is what the program does.

go `imports` of redundant or missing package will cause compilation failure.

## declarations

### var, const, type and func

```go
s := "" // only in functions, not for package level var
var s string
var s = "" // rarely used
var s string = "" // redundant if we assign to zero value of type
```

var declaration are always implicitly assign to zero value. package-level variable are initialized before `main` begins.

### short variable declarations

```go
err := os.Open()
i, j := 1, 0
```

to declare and initialize **local** variables. its often used to declare and initialize the majority of the local variables while `var` tends to be reserved for local variables that need an explicit type.

> note := is declaration while = is assignment

```go
// tuple assignment - similar to python
a, b = b, a
```

short variable declaration does not necessarily declare everything. if some of them are declared in the same lexical block then the short variable declaration acts like an assignment

```go
in , err := os.Open()
// ...
out, err := os.Create() // compiles
// ---
f, err := os.Open()
// ...
f, err := os.Create() // compile error: no new variables
f, err = os.Create() // fix
```

### type declarations

defines the characteristics of the values it may take on.

```go
type Celsius float64
type Fahrenheit float64

const AbsoluteZeroCelsius Celsius = -273.15

func CToF (c Celsius) Fahrenheit { return Fahrenheit(c * 9/5 + 32)}
```

`celsius` and `fahrenheit` although shares same underlying type but they are not the same type, thus can't be compared or combined in arithmetic expressions. distinguishing them allow to prevent mixed type calculation. for every type `T` there is a conversion operation that converts value `x` to type `T` and it permitted as long as the underlying type are the same.

## pointers

similar to C

```go
x := 1
p := &x
fmt.Println(*p) // 1
*p = 2
fmt.Println(*p) // 2
```

`&` can only be applied on variables. pointers are comparable with `==`. its possible to retain local variable after the call of function has returned. we can pass a pointer to a function to allow update on the variable directly. by passing variable `p` shown above is essentially using the variable `x`'s  alias.

### the new function

creates an unnamed variable of the declared type and subsequently accessed through dereferencing. the merit of using new to create variables is such that it does not requires to declare dummy name (x in the example above). note its a syntactical convenience.

```go
func newInt() *int {
    return new(int)
}
// work same as
p := new(int)
// and
func newInt() *int {
    var dummy int
    return &int
}
```

there might be a caveat depending on the implementation that variables that carries no information may have the same address. `new` is rarely used as the most common unnamed variables are `struct`.

## variable lifetime

lifetime of a package-level variables is the entire execution of the program. local variable in contrast have a dynamic lifetime, after creation, it lives until its unreachable and then proceed to be GC. similar to java, an object or variable is GCed when no more reference (or path in go) lead to it. local variables can be allocated to heap or stack depending on the program implementation eg. if access is still needed post local function call. its okay to leave this consideration out until performance optimization.

```go
var global *int
func f() {
    x := 1
    global = &x // heap
}
func g() {
    y := new(int)
    *y = 1 // stack
}
```

## file structure

1. file whose names end with `.go`
2. file begins with a `package` declaration that indicates what package the file is part of
3. `import` declaration
4. package-level declaration

## packages and files

upper casing of first letter of a name determines that its exported, and its visible and accessible outside of its own package and may be referred to by other parts of the program. package similar to other languages serves as an approach to modularize, encapsulate and more. each package have a separate name space for its declaration. 

### some standard packages

#### os

dealing with operating system and `os.Args` can retrieve CLI args. the variables from `os.Args` are slice of strings.

#### bufio

buffered io that warps around `io.Reader` or `io.Writer`, creating another object that implements the interface but provides buffering.

#### flag

take in cli flags and register to **pointer**, thus subsequent usage will be using `*` to dereference.

### package initialization

package initialization begin by initializing package-level variables by - dependencies and order of declaration. in some cases its better to use declare an `init` function

```go
func init() {}
```

these `init` function cant be called or referred, and will be executed first. packages are initialized one at a time, in the order of imports, dependencies, and bottom up - thus `main` is the last to be initialized such that all packages are fully initialized before `main` function begin.

## scope

scope is a compile-time property; lifetime is a run-time property. a syntactic block is a sequence of statements enclosed in braces. a name declared in a syntactic block is not visible outside. `import` in one file is local to that file (or `imports` is at file level), another file need to use the package requires another `import`. similar to python, the go compiler will look for declaration starting with the inner most enclosing lexical block (eg a simple `for` or `if` block), and work up to the universal block. if no declaration is found then `undeclared name` error is throwed.

```go
// example 1
if f, err := os.Open(); err != nil { return err } // a lexical block
f.ReadByte() // compile error: undefined f
f.Close() // compile error: undefined f
// example 2 - preferred
f, err := os.Open()
if err != nil { return err }
f.ReadByte() // ok
f.Close() // ok
// example 3
if f, err := os.Open(); err != nil {
    return err
} else {
    f.ReadByte() // ok
    f.Close() // ok
}
```

## imports

```go
import "net/http" // allows us to refer to http directly
```

go differs from python which the usual flow would be `pip install` packages then update `requirements.txt` then import. for go standard packages, a seamless way is to **not** import any package and allow `gofmt` to handles those. for external packages, not sure yet.

## data structures

go's types falls into four categories, basic, aggregate, reference and interface. aggregate is formed up by several simpler ones. reference type including pointers, slices, maps, functions and channels, refers to program variables or state **indirectly**, such that the effect of an operation applied is observed by all copies of that reference.

### basic data types

#### numbers

`int` and `uint`. `NaN` always yield false in any comparison.

#### strings

immutable sequence of bytes. `len` returns number of bytes in a string and `s[i]` retrieves the i-th byte of string s where 0 <= i < `len(s)` (note we could be working on 16 byte characters more on this later). substring yields **new** string consist of bytes of the original string.

```go
// immutability
s := "string"
t := s
s += " another"
// fmt.Println(t) prints "string"
// fmt.Println(s) prints "string another"
```

due to its immutability, its cheap to substring, and copy string of any length (by pointing to same object). raw string literals are wrapped with back quotes `.

important packages for manipulating strings `bytes`, `strings`, `strconv` and `unicode`. `strings` provide searching, replacing, comparing, trimming, splitting and joining. `bytes` manipulates bytes or `[]byte` which shares some property as strings, and due to string's immutability it would be better to build up string incrementally using `bytes.Buffer`. `strconv` converts bool, int and float to their string representations. `unicode` allows `IsDigit` and similar functions for classifying runes.

`bytes` package provides `Buffer` type to manipulate byte slices efficiently by starts out empty and grow as the data types are written to it.

```go
s := "abc"
b := []byte(s)
s2 := string(b)
```

the approach above involved two coping operation, to avoid conversions and unnecessary memory allocation utility function in `byte` package mirrors those in `strings` package.

#### unicode and utf-8

utf-8 is a variable length encoding of unicode code points as bytes. it uses between 1 to 4 byte to represent each rune, but only 1 byte for ASCII characters, and 2 or 3 for most runes in common uses. go source files are always encoded in utf-8 and its the preferred encoding for text string manipulated by go programs. `unicode` package provides function for working with individual runes, and `unicode/utf8` provides functions for encoding and decoding runes as bytes using utf-8.

#### string and number conversions

through `strconv` package.

```go
// from int to str
x := 123
fmt.Println(strconv.Iota(x))
// from str to int
x := "123"
y, err := strconv.Aoti(x)
// or with the following to prevent overflow / underflow
y, err = strconv.ParseInt(x, 10, 64) // base 10, max 64 bits
```

#### booleans

`&&` and `||`. short circuit behavior if the answer is already determined by the values of the left operand, the right operand will not be evaluated.

#### constants

expression whose value is know to compiler and whose evaluation is guaranteed to occur at compile time instead of runtime. constants is still the usual number, strings and booleans however its value cannot be change during runtime.

```go
// multi-declaration
const (
	e = 2.718
    pi = 3.142
)
// constant generator iota
type Weekday int
const (
	Sunday Weekday = iota // 0
    Monday // 1
    // ...
)
```

#### untyped constants

its possible to have uncommitted type constants, and with this compiler will assume higher accuracy (at least 256 bits). the deferment also allows constants to participate more expressions without conversions. note only constants can be untyped.

```go
// example of controllable precision
const Pi64 float64 = math.Pi
var x float32 = float32(Pi64)
var y float64 = Pi64
var z complex128 = complex128(Pi64)
```

> //take the following point with a grain of salt

```go
var f float64 = 212
fmt.Println((f - 32) * 5 / 9) // 100
fmt.Println(5 / 9 * (f - 32)) // 0
fmt.Println(5.0 / 9.0 * (f - 32)) // 100
```

the print result is without decimal points because the number used for calculation are uncommitted. also the numbers here are actually constants (if my interpretation is correct).

### composite types

array and structs are aggregate types where they concatenate other values in memory, with one homogeneous and one heterogeneous. both are fixed size and contrast to map and slice are dynamic data structures.

#### arrays

**FIXED** length sequence of elements. slice (variate length) is more prominent however slice is based off array's idea. a new array will be initialized to zero value of the declared type.

````go
var q [3]int = [3]int{1, 2, 3}
// array literal can be replace by ... thus
q := [...]int{1, 2, 3}
````

> note [3]int and [4]int are different type, given the size is a constant it can be computed in runtime

```go
type Currency int

const (
	USD Currency = iota
    EUR
    GBP
    RMB
)

symbol := [...]string{USD: "$", EUR: "euro", GBP: "pound", RMB: "yuan"} // not to confuse with python dict
fmt.Println(RMB, symbol[RMB]) // 3 yuan
fmt.Println(symbol) // [dollar euro pound yuan]
```

comparing between arrays is possible if the type are the same. checking `==` is checking if all corresponding elements are equal. in go functions **passes a COPY** of each argument as contrast to python's **pass by REFERENCE**, thus to optimize performance we can do the following.

```go
// instead of passing a copy of a large array
func zero(ptr *[32]byte) {
    for i: range ptr {
        ptr[i] = 0
    }
   	// or 
    *ptr = [32]byte{}
}
```

array indexing is a bit different from python where negative indexes are not supported, thus to access the last element we should do the following

```go
var arr = [3]int{1, 2, 3}
fmt.Printf(arr[len(arr)-1])
```

#### slices

variable length sequences whose element of the same type. slice declaration is just array without the size `[]T`. initializing this way will first creates an array and returns the slice of it. a slice consist of three components, pointer, length and capacity. we can re-slice beyond the original slice length as long as it does not exceeds the underlying array length else it panics.

```go
// reversing an array
func reverse(s []int) {
    for i, j := 0, len(s)-1; i < j; i, j = i+1, j-1 {
        s[i], s[j] = s[j], s[i]
    }
}

func main() {
    a := [...]{0, 1, 3, 4, 5}
    reverse(a[:])
}
```

unlike arrays, slices are not comparable, go  check equality with shallow equality test (reference identity). the only legal slice comparison is to check against `nil` (if a slice is zero value) and to check if a slice is empty use `len(s) == 0`.

```go
// creates an unnammed array and return slice and the array is accessed though the slice
make([]T, len)
make([]T, len, cap) // cap > len, thus can only access the first len of elements
```

slice's build-in function `append` appends item to slice.

```go
// appends allows adding multiple items 
slice = append(slice, 2, 3, 4)
// its achieved by having ellipsis which makes a function variadic
func appendInt(x []int, y ...int) []int {
    // ...
}
```

> if there are multiple outputs and we only care about the first we can omit the second output

> takes note functions that modify data structure in place, their behavior might be unexpected

```go
func nonempty(strings []string) []string {
    i := 0
    for _, s := range strings {
        if s != "" {
            strings[i] = s
            i++
        }
    }
    return strings[:i]
}
data := []string{"one", "", "three"}
fmt.Printf("%q\n", nonempty(data)) // ["one", "three"]
fmt.Printf("%q\n", data) // ["one", "three", "three"]
// to avoid confussion its best to do the following
data = nonempty(data)
```

using slice as stack

```go
var stack []int
stack = append(stack, value)
top := stack[len(stack)-1]
stack = stack[:len(stack)-1]
```

#### maps

hash table, an **unordered** collection of key/value pair where all keys are distinct and we can apply crud to the values using constant number key comparison regardless of the size of the hash table.

```go
counts := make(map[string]int)
// map literals
age := map[string]int{"Alice": 25}
// adding, delete, update
age["Bob"] = 24
delete(age, "alice")
age["Bob"]++ // if not specified will still initiated as 0
// map element is not a variable
_ = &age["Bob"] // compile error: cannot take address of map element
// enumerating
for name, age := range age {
    // pass
}
```

note, order of printing from `range` is random and it is intentionally designed as such. to enumerate in order, maps must be sorted explicitly.

```go
import "sort"

var names[]string
for name := range ages{
    names = append(names, name)
}
sort.Strings(names)
for _, name := range names{
    fmt.Printf("%s\t%d\n", name ages[namettt])
}
// since we know the length of age, it is more efficient to allocate an array of the required size.
names := make([]string, 0, len(ages))
// validate key existence
age, ok := ages["bob"]
if !ok {
    // bob dne
}
// a more concise way
if age, ok := ages["bob"]; !ok {
    // do stuffs
}
```

similar to slice, map can't be compared to each other, the only legal test is against `nil` thus to check equality or key existence, loop is required.

```go
func equal_map(x, y map[string]int) bool {
    if len(x) != len(y) {
        return false
    }
    for k, vx := range x {
        if vy, ok := y[k]; !ok || vy != vx {
            return false
        }
    }
    return true
}
```

there is no build-in set types, but it is made possible with map's key.

> to come back p97 - 99

#### structs

an aggregate data type that groups together zero or more named values of arbitrary types as single entity. each value is called a field. fields are accessed with dot notation and struct fields order in the declaration matters. Caps struct name indicates its exported. struct cant declare a field of the same type, it should be a pointer instead when building data structure eg. linked list.

```go
type Employee struct {
    ID int
    Name string
    DOB time.Time
}

type tree struct {
    value int
    left, right *tree
}
// struct literal
var t = tree{value:1} // explicit
```

modifying structs efficiently. go always pass a copy thus in-place modification need to be done though pointers.

```go
func Bonus(e *Employee, factor int) {
    e.salary = e.salary * factor
}
```

comparing structs is possible with `==` and `!=`, and because its a comparable type, it is eligible to be set as key of a map type. anonymous fields and struct embeddings

```go
// explicit
type Point struct {
    x, y int
}
type Circle struct {
    Center Point
    Radius int
}
type Wheel struct {
    Circle Circle
    Spokes int
}
var w Wheel
w.Circle.Center.x = 8 // might be too verbose
// anonymous fields
type Circle struct {
    Point
    Radius int
}
type Wheel struct {
    Circle
    Spokes int
}
w.x = 8 // we still can access through the verbose way, but its now optional at the cost of lack of struct literal support
w = Wheel{x: 8, y:8, Radius: 8, Spokes: 8} // compile error: unknown fields
w = Wheel{Circle{Point{8, 8}, 8}, 8} // no error
// or
w = Wheel{
    Circle: Circle{
        Point: Point{x: 8, y: 8},
        Radius: 8, // note trailing comma
    }
    Spokes: 8, // note trailing comma
}
```

its not possible to have two anonymous fields of the same type as there exists implicit name. also the field visibility tied to the type (name), in the example above both `Point` and `Circle` are exported, had they been not exported eg. `point`, it will not be possible to access through explicit form `w.circle.point.x` although still be able to access through `w.x`.

```go
// printing structs
fmt.Printf("%#v\n", w) // # will print out field names
```

#### json

go has support to structured information including json, xml and more under `encoding` and `decoding` package. json types including numbers, booleans, strings are essentially sequence of unicode code points enclosed in double qoutes with backslash escapes.

> note field tag alternative name is also for json name with underscore

```go
// marshaling, converting go objects to json
type Movie struct {
    Title string
    Year int `json:"released,omitempty"`
    Actors []string
}
var movies = []Movie{
    // ...
}
data, err := json.Marshal(movies) // or MarshalIndent for readability
```

marshaling uses go struct field names as field names for JSON objects through reflection and only exported fields are marshaled thus caps is required for all fields. the backtick indicates field tags, the first released is the alternative JSON field name, `omitempty` indicates no output to produce when field has zero value or empty.

```go
// unmarshaling
var titles []struct{ Title string}
if err := json.Unmarshal(data, &titles); err != nil {
    log.Fatalf("JSON unmarshaling failed: %s", err)
}
```

its possible to partially unmarshal json by defining the struct accordingly.

#### text and HTML templates

similar to jinja2 from python, with `text/template` and `html/template`.

```go
const templ = `{{.TotalCount}} issues:
{{range .Items}}Number:
{{.Number}}
User: {{.User.Login}}
Title: {{.Title | printf "%.64s"}}
Age: {{.CreatedAt | daysAgo}} days
{{end}}`
```

`range` and `end` creates a loop.

## Functions

- go have no default parameters concept
- return may be named or just state the type
- go do not have way to specify arguments by name

### returning multiple values

````go
func findLinks(url string) ([]string, error) {
	resp, err := http.Get(url)
	if err != nil {
        return nil, err
	}
	if resp.StatusCode != http.StatusOK {
		resp.Body.Close()
		return nil, fmt.Errorf("getting %s: %s", url, resp.Status)
	}
	doc, err := html.Parse(resp.Body)
	resp.Body.Close()
	if err != nil {
		return nil, fmt.Errorf("parsing %s as HTML: %v", url, err)
	}
	return visit(nil, doc), nil
}
````

the result of a multi-value call may be itself return from a multi-valued calling function

```go
func findLinksLog(url string) ([]string, error) {
    log.Printf("find links %s", url)
    return findLinks(url)
}
```

for named returns, its possible do a bare return

```go
func findWordCount(input string) (word string, count int, err error) {
    return
}
```

### errors

a function for which failure is expected returns an additional result. if there is only a possible cause, return a boolean instead. go uses ordinary value to report failure which differentiates from other language's exception although go have a similar mechanism panic. the reason for such design is to allow control flow to respond to errors, instead of reporting routine error with incomprehensible stack trace.

#### error handling strategies

first, propagating error such that a subroutine failure becomes a failure of the calling routine. error messages are frequently chained together thus messages should not be caps and avoid newlines to benefit tools eg `grep`. the caller will have the most information with regards to the error thus it should be responsible for the reporting.

secondly, transient or unpredictable problems might be sensible to retry with a delay between tries and limited attempts before giving up entirely.

```go
func WaitForServer(url string) error {
	const timeout = 1 * time.Minute
	deadline := time.Now().Add(timeout)
	for tries := 0; time.Now().Before(deadline); tries++ {
		_, err := http.Head(url)
		if err == nil {
			return nil // success
		}
		log.Printf("server not responding (%s); retrying...", err)
		time.Sleep(time.Second << uint(tries)) // exponential backoff
	}
	return fmt.Errorf("server %s failed to respond after %s", url, timeout)
}
```

thirdly, if progress is impossible the caller can print the error and stop the program gracefully however this should be reserved for the main function by using `log.Fatalf`. the default format is for long running server, for interactive tool we can use the prefix used by `log` package.

```go
log.SetPrefix("wait: ")
log.SetFlags(0)
```

fourthly, log and continue with reduced functionality. and finally in rare cases we can ignore error entirely, by discarding error out completely.

#### end of file

```go
in := bufio.NewReader(os.Stdin)
for {
	r, _, err := in.ReadRune()
	if err == io.EOF {
		break // finished reading
	}
	if err != nil {
		return fmt.Errorf("read failed: %v", err)
	}
	// ...use r...
}
```

### function values

functions are first class values in go. a function zero value is `nil` and can be compared with `nil` but not each other.

```go
func add1(r rune) rune { return r+1 }
fmt.Println(strings.map(add1, "VMS")) // WNT
```

### anonymous functions

similar concept as an object? an anonymous function will have access to the enclosed function lexical scope. this is also why functions are not comparable. function values are implemented with closures.

```go
func squares() func() int {
	var x int
	return func() int {
		x++
		return x * x
	}
}
func main() {
	f := squares()
	fmt.Println(f()) // "1"
	fmt.Println(f()) // "4"
	fmt.Println(f()) // "9"
	fmt.Println(f()) // "16"
}
```

#### caveat with iterables

````go
var rmdirs []func()
for _, d := range tempDirs(){
    dir := d // note!
    os.MkdirAll(dir, 0755)
    rmdirs = append(rmdirs, func(){
        os.RemoveAll(dir)
    })
}
````

the `for` loop introduce a new lexical scope where `dir` is declared, `d` will refer to the same address but not the value at the moment. this caveat is not unique for `range` based loops but all iterables and together with the use of `go` and `defer` statement as execution of a function value is delayed until loop is finished.

### variadic functions

function with varying numbers of arguments, ie a fixed arguments plus any number of subsequent arguments for `fmt.Printf`.

```go
func sum(vals ...int) int {
    total := 0
    for _, val := vals {
        total += val
    }
    return total
}
```

implicitly it allocates an array and copies the arguments into it then passes a slice of the entire array to the function.

```go
// slice arguments
values := []int{1, 2, 3, 4}
fmt.Printf(sum(values...))
```

although `...int` behaves like a slice however, its different type.

```go
func sum1(...int) {}
func sum2([]int) {}
fmt.Printf("%T\n", sum1) // func(...int)
fmt.Printf("%T\n", sum2) // func([]int)
```

### deferred function calls

when we need to `close` IOs multiple times for different situations, go has `defer` syntactic sugar for it. `defer` is an ordinary function or method call prefixed such that function and argument expressions are evaluated when the statement is executed but actual call is deferred until the function that contains the defer statement has finished. any number of calls can be deferred, and they are executed in reversed order (stack). in short defer is a mechanism to release resource eg lock, connection/IO and etc. the right place for a defer statement is immediately after the resource has been successfully acquired.

```go
func getTitle(url string) error {
    resp, err := http.Get(url)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    content := resp.Header.Get("Content-Type")
    if content != "text/html" && !strings.HasPrefixx(content, "text/html;") {
        return fmt.Errorf("%s has type %s not text/html", url, content)
    }
    doc, error := html.Parse(resp.Body)
    if err != nil {
        return fmt.Errorf("parsing %s as Html: %v", url, err)
    }
    return nil
}
// or a simple file IO
func readFile(fname string) ([]byte, error) {
    f, err := os.Open(fname)
    if err != nil {
        return nil, err
    }
    defer f.Close()
    return ReadAll(f)
}
```

`defer` can also be used pair on entry and on exit actions. it executes most of the statements on entry, and returns a function value that called on exit.

```go
func trace(msg string) func() {
    start := time.Now()
    log.Printf("on entry time: %s", start) // 2. execute up to here on entry
    return func() { log.Printf("on exit msg: %s; on exit time: %s", msg, time.Since(start)) } // 4. executes this on exit
}

func retrieveInformation () {
    defer trace("retrieveInformation") () // 1. note this execute
    time.Sleep(10 * time.Second)
    // 3. on exit
}
```

also deferred functions/calls runs after the return statement, it will have access to results within the same lexical scope.

```go
func double(x int) (result int) {
    defer func() { fmt.Printf("result: %d", result) }() // note, again
    return x * 2
}
// or changing the final output
func triple(x int) (result int) {
    defer func() { result += x }() // note, again
    return x * 2
}
```

handling `defer` with loops required extra caution, a common pattern is to move the loop body including the `defer` statement into another function that is called on each iteration. if its not separated, the release of resource will only be released after the loop has complete execution.

```go
for _, fname := range fnames {
    if err := doSomething(fname); err != nil {
        return err
    }
}
func doSomething(fname string) error{
    f, err := os.Open(fname)
    if err != nil {
        return err
    }
    defer f.Close()
    // work with f
}
// bad example
for _, fname := range fnames {
    f, err := os.Open(fname)
    if err != nil {
        return err
    }
    defer f.Close()
    // work with f
}
```

note to also not abuse `defer`. when we are working with file IO, its recommended to leave out defer.

### panic

essentially go's runtime error. during panic,

- normal execution stops
- deferred function calls in goroutine are executed
- program crashes with log message

the log message contains

- panic value
- for each goroutine a stack trace

its usually self sufficient to debug with the log message without executing the program thus its suggested to include the log message in the bug report of the panic program. also its possible to call `panic` manually, and it best for scenario when impossible situation happens.

```go
switch s := suit(drawCard()); s {
case "spades":
case "hearts":
case "diamonds":
case "clubs":
default:
    panic("joker")
}
```

panic is explicitly needed when additional information can be provided else go handles panic well enough. functions with Must as a prefix is the convention that handles panic. panic is not the exact exceptions we see in other languages. in go, there exists `error` and `panic` the former for most of the errors that can still be gracefully handled and the latter is for showstopper. go provides `printStack` for debugging purposes, and its usually run as `defer printStack()`.

### recover

not everything is disastrous or maybe cleanup is required before exiting process therefore recover. if `recover` is called within a deferred function during panic, it resolve as follows.

```go
func Parse(input string) (s *Syntax, err error) {
    defer func() {
        if p := recover(); p != nil {
            err = fmt.Errorf("internal error: %v", p)
        }
    }()
    return nil, nil // 2nd nil will be override by err
}
```

recover is another mechanism not to abuse because variables after panic is rarely well defined and documented. it recommended to recover within the same package for simplicity reason. panic is best to be called out.

