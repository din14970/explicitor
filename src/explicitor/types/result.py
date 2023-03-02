from __future__ import annotations
from typing import Generic, TypeVar, Any, Callable, Union
from explicitor.utils import _equal_errors


T = TypeVar("T")
U = TypeVar("U")
W = TypeVar("W")
E = TypeVar("E", bound=BaseException)


class Ok(Generic[T, E]):
    _value: T
    __match_args__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"Ok({repr(self._value)})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Ok):
            return self._value == other._value
        return False

    def unwrap(self) -> T:
        return self._value

    def expect(self, message: str) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return self._value

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap_err(self) -> E:
        raise Exception(f"Unexpected {repr(self)}")

    def expect_err(self, message: str) -> E:
        raise Exception(message)

    def map(self, op: Callable[[T], U]) -> Result[U, E]:
        return Ok(op(self._value))

    def raise_err(self) -> None:
        pass


class Err(Generic[T, E]):
    _err: E
    __match_args__ = ("_err",)

    def __init__(self, err: E) -> None:
        self._err = err

    def __repr__(self) -> str:
        return f"Err({repr(self._err)})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Err):
            return _equal_errors(self._err, other._err)
        return False

    def unwrap(self) -> T:
        raise self._err

    def expect(self, message: str) -> T:
        raise Exception(message)

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return op(self._err)

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap_err(self) -> E:
        return self._err

    def expect_err(self, message: str) -> E:
        return self._err

    def map(self, op: Callable[[T], U]) -> Result[U, E]:
        return Err(self._err)

    def raise_err(self) -> None:
        raise self._err


Result = Union[Ok[T, E], Err[T, E]]
