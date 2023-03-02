from typing import Any, Callable, cast
from explicitor.types import Ok, Err, Result, T, E
import functools


def unraise(func: Callable[..., T]) -> Callable[..., Result[T, E]]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Result[T, E]:
        result: Result[T, E]
        try:
            output = func(*args, **kwargs)
            if isinstance(output, Ok):
                result = output
            else:
                result = Ok(output)
        except Exception as e:
            result = Err(cast(E, e))
        return result

    return wrapper
