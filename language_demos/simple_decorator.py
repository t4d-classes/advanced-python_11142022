""" simple decorator module """

from typing import Any, Callable

def wrapper(func: Callable[..., Any]) -> Callable[...,Any]:
    """ wrapper """

    def inner(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
        """ inner """
        print("start")
        return func(*args, **kwargs)

    return inner

@wrapper
def do_it(num_a: int, num_b: int) -> int:
    """ do it """
    return num_a +num_b

# func_a = wrapper(do_it)
# print(func_a(1,2))

print(do_it(1,2))
