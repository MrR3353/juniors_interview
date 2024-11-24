from functools import wraps


def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__.copy()
        annotations.pop('return', None)
        assert len(annotations) == len(args) + len(kwargs), "Count of annotations must be equal to args + kwargs"

        annotations = list(annotations.items())
        i = 0
        for arg in args:
            if type(arg) != annotations[i][1]:
                raise TypeError
            i += 1
        for key, value in kwargs.items():
            if type(value) != annotations[i][1]:
                raise TypeError
            i += 1
        result = func(*args, **kwargs)
        return result
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b

# print(sum_two(1, 2))  # >>> 3
# print(sum_two(1, 2.4))  # >>> TypeError

