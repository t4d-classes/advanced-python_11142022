""" list transform module """

from typing import Any, Callable
from collections.abc import Generator

nums = [1,2,3,4,5]

# double_nums = []

# for num in nums:
#     double_nums.append(num * 2)

def double(pnum: int) -> int:
    """ double pnum """
    print(f"called double {pnum}")
    return pnum * 2

# double_nums1 = [ double(num) for num in nums ]
double_nums2 = map(double, nums)

print(nums)


# for num in double_nums1:
#     print(num)

# for num in double_nums2:
#     print(num)


def mymap(
    transform_fn: Callable[[Any], Any],
    items: list[Any]) -> Generator[Any, None, None]:
    """ mymap """
    for item in items:
        yield transform_fn(item)


double_nums3 = mymap(double, nums)

for num in double_nums3:
    print(num)
