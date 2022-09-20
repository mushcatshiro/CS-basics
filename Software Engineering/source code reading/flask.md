[TOC]

# Flask source code reading

## python related

1. functools [official doc link](https://docs.python.org/3/library/functools.html)

```python
from functools import partial

callable_object = partial(fn, 5, multiplier=10)
callable_object(2)
# >>> 25
def fn(x, y, multiplier=2):
    return x * multiplier / y
```

partial objects are callable objects created by `partial()` with three **read only attributes**, func, args and keywords. note, args will be the **leftmost** positional argument.

2. python debugger

```python
import pdb

pdb.set_trace()
```

## reference material

- [cizixs](https://cizixs.com/2017/01/10/flask-insight-introduction/)
- [segmentfault](https://segmentfault.com/a/1190000022139239)
- [jiajunhuang](https://jiajunhuang.com/articles/2016_09_15-flask_source_code.rst.html)