import pytest
from explicitor import Ok, Err, unraise, Result
from explicitor.utils import _equal_errors


class TestOk:
    ok: Ok = Ok(1)

    def test_repr(self) -> None:
        assert repr(self.ok) == "Ok(1)"

    def test_eq(self) -> None:
        assert self.ok == Ok(1)
        assert self.ok != Ok(2)

    def test_unwrap(self) -> None:
        assert self.ok.unwrap() == 1

    def test_expect(self) -> None:
        assert self.ok.expect("something something") == 1

    def test_unwrap_or(self) -> None:
        assert self.ok.unwrap_or(2) == 1

    def test_unwrap_or_else(self) -> None:
        assert self.ok.unwrap_or_else(lambda x: x) == 1

    def test_is_ok(self) -> None:
        assert self.ok.is_ok()

    def test_is_err(self) -> None:
        assert not self.ok.is_err()

    def test_unwrap_err(self) -> None:
        with pytest.raises(Exception) as e:
            self.ok.unwrap_err()
        assert str(e.value) == "Unexpected Ok(1)"

    def test_expect_err(self) -> None:
        with pytest.raises(Exception) as e:
            self.ok.expect_err("something")
        assert str(e.value) == "something"

    def test_map(self) -> None:
        assert self.ok.map(lambda x: x + 1) == Ok(2)

    def test_raise_err(self) -> None:
        self.ok.raise_err()


class TestErr:
    err: Err = Err(ValueError("test"))

    def test_repr(self) -> None:
        assert repr(self.err) == "Err(ValueError('test'))"

    def test_eq(self) -> None:
        assert self.err == Err(ValueError("test"))
        assert self.err != Err(ValueError("test2"))

    def test_unwrap(self) -> None:
        with pytest.raises(ValueError) as e:
            self.err.unwrap()
        assert str(e.value) == "test"

    def test_expect(self) -> None:
        with pytest.raises(Exception) as e:
            self.err.expect("something something")
        assert str(e.value) == "something something"

    def test_unwrap_or(self) -> None:
        assert self.err.unwrap_or(2) == 2

    def test_unwrap_or_else(self) -> None:
        assert self.err.unwrap_or_else(lambda x: str(x) + "123") == "test123"

    def test_is_ok(self) -> None:
        assert not self.err.is_ok()

    def test_is_err(self) -> None:
        assert self.err.is_err()

    def test_unwrap_err(self) -> None:
        assert _equal_errors(self.err.unwrap_err(), ValueError("test"))

    def test_expect_err(self) -> None:
        assert _equal_errors(self.err.expect_err("bla"), ValueError("test"))

    def test_map(self) -> None:
        assert self.err.map(lambda x: x + 1) == self.err

    def test_raise_err(self) -> None:
        with pytest.raises(ValueError) as e:
            self.err.raise_err()
        assert str(e.value) == "test"


def test_unraise() -> None:

    def raises_exception(x: int) -> int:
        if x < 10:
            raise ValueError("too small")
        return x + 1

    result_ok: Result[int, ValueError] = unraise(raises_exception)(20)
    result_err: Result[int, ValueError] = unraise(raises_exception)(5)

    assert result_ok.unwrap() == 21
    assert result_err == Err(ValueError("too small"))


def test_unraise_method() -> None:

    class Dummy:
        @unraise
        def raises_exception(self, x: int) -> int:
            if x < 10:
                raise ValueError("too small")
            return x + 1

    result_ok: Result[int, ValueError] = Dummy().raises_exception(20)
    result_err: Result[int, ValueError] = Dummy().raises_exception(5)

    assert result_ok.unwrap() == 21
    assert result_err == Err(ValueError("too small"))


def test_match() -> None:
    def test_function(x: int) -> Result[int, ValueError]:
        if x < 10:
            return Err(ValueError("too small"))
        return Ok(x + 1)

    match test_function(20):
        case Ok(v): assert v == 21
        case Err(e): raise Exception

    match test_function(5):
        case Ok(v): raise Exception
        case Err(e): assert _equal_errors(e, ValueError("too small"))
