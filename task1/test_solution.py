import pytest

from solution import strict


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def to_string(a: int, b: bool, c: float, d: str):
    return str(a) + str(b) + str(c) + d

@strict
def no_args():
    return 1


@strict
def no_annotations(a):
    return a


def test_args():
    assert sum_two(1, 2) == 3
    assert no_args() == 1
    with pytest.raises(AssertionError):
        assert no_annotations(1) == 1
    with pytest.raises(TypeError):
        sum_two(1, 2.4)
    with pytest.raises(TypeError):
        sum_two('a', 2)
    with pytest.raises(AssertionError):
        sum_two(1, 2, 3)


def test_kwargs():
    assert sum_two(1, b=2) == 3
    assert sum_two(a=4, b=2) == 6
    with pytest.raises(TypeError):
        sum_two(1, b=True)
    with pytest.raises(AssertionError):
        sum_two(1, 2, c=3)


def test_to_string():
    assert to_string(1, False, 3.0, 'a') == '1False3.0a'
    with pytest.raises(AssertionError):
        to_string(1, False, 3.0)
    with pytest.raises(TypeError):
        to_string(1, 3, 3.0, 'b')
    with pytest.raises(TypeError):
        to_string(1, True, 3, 'b')
    with pytest.raises(TypeError):
        to_string(1, True, 3.4, 1)