# Explicitor

Rust-like explicit errors for typed Python.

## Why this exists

Exceptions suck in many statically typed programming languages.
From a function signature it is usually impossible to know whether the function can throw an error.
The Rust programming language solves this problem quite elegantly with the [Result enum](https://doc.rust-lang.org/std/result/enum.Result.html), which allows you to use the type checker to reason about correct error handling.
An additional benefit is that error handling is much more elegant than `try ... except` clauses.

The goal of this package is to emulate in Python the Rust way of dealing with errors.
The implementation is *heavily* inspired by the contents of [this blogpost](https://jellis18.github.io/post/2021-12-13-python-exceptions-rust-go/) by [Justin Ellis](https://github.com/jellis18).
The philosophy is that instead of raising exceptions, exceptions are returned wrapped in an `Err` class, which is a variant of the `Result` type.
Hence, a function that can get into an error state returns a `Result` which can be clearly indicated in a function signature.
This can be valuable when one uses static type analysis tools like [mypy](https://www.mypy-lang.org/).

## Installation

```bash 
pip install explicitor
```


## How to use it

There are 3 types defined: `Ok`, `Err` which are the two variants of `Result`.

Instead of defining a function that can raise an exception, for example:

```python 
def function(x: int) -> int:
    if x < 10:
        raise ValueError("too small")
    return x + 1
```

you would define your function as

```python 
from explicitor import Ok, Err, Result


def function(x: int) -> Result[int, ValueError]:
    if x < 10:
        return Err(ValueError("too small"))
    return Ok(x + 1)
```

To deal with the error, there's a number of methods implemented on `Err` and `Ok`:

```python 
result_1 = function(20)  # should be an Ok
result_2 = function(5)  # should be an Err


# unwrap: returns the wrapped value of an Ok or raises the error contained by an Err
assert result_1.unwrap() == 21
try:
    result_2.unwrap()
except ValueError as e:
    assert str(e) == "too small"


# expect: same as unwrap, but raises a custom exception with custom message
assert result_1.expect("bla") == 21
try:
    result_2.expect("bla")
except Exception as e:
    assert str(e) == "bla"


# is_ok and is_err: checks what variant it is and returns a boolean
assert result_1.is_ok()
assert result_2.is_err()


# unwrap_or: if Ok, unwrap, if Err, return the value supplied
assert result_1.unwrap_or(2) == 21
assert result_2.unwrap_or(2) == 2


# unwrap_or_else: if Ok, unwrap, if Err, apply a function to the wrapped error and return it
assert result_1.unwrap_or_else(lambda x: str(x)) == 21
assert result_2.unwrap_or_else(lambda x: str(x)) == "too small"


# unwrap_err: the opposite of unwrap, raise an exception if Ok, return the wrapped Exception if Err
try:
    result_1.unwrap_err()
except Exception as e:
    assert str(e) == "Unexpected Ok(21)"
assert str(result_2.unwrap_err()) == "too small"


# expect_err: the opposite of expect, raise an exception with custom message if Ok, return the wrapped Exception if Err
try:
    result_1.expect_err("custom message")
except Exception as e:
    assert str(e) == "custom message"
assert str(result_2.expect_err("custom message")) == "too small"


# map: apply a function to the wrapped value in Ok, do nothing if Err
assert result_1.map(lambda x: x + 1) == Ok(22)
assert result_2.map(lambda x: x + 1) == Err(ValueError("too small"))
```

Finally, in Python 3.10+, it's possible to use Rust-like `match` statements for dealing with the errors:

```python 
match function(20):
    case Ok(v): print("The value is", v)
    case Err(e): print("The error is", str(e))
```

Suppose a function does raise exceptions, it is possible to use the `unraise` decorator to catch these exceptions and return them wrapped in an `Err` instead.
If no exception is raised, the decorator wraps the output of the function in an `Ok`.

```python 
from typing import Callable
from explicitor import unraise


def function(x: int) -> int:
    if x < 10:
        raise ValueError("too small")
    return x + 1


safe_func: Callable[[int], Result[int, ValueError]] = unraise(function)
```

## What does not work
In Rust, there is the handy `?` operator, which allows you to quickly return an `Err` from a function or continue if the result is an `Ok`.
In Python, the equivalent might be:

```python
result: Result = function()

if result.is_err():
    return result

...
```

There are also a lot of additional methods available on Rust's `Ok` and `Err` which are thus far not implemented, particularly their translations to `Option`.

Personal experimentation has shown that mypy may not always deal with these types or the `match` expression as expected, certainly I would not consider them as safe as the Rust equivalents.
If you know how to improve the implementation so that it works better with mypy, and/or makes the behavior more Rust-like, feel free to make a PR.


## Contributing
1. Fork and clone the repo
2. Create a virtual environment
3. `poetry install`
