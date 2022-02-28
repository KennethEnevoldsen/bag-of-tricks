from typing import List
from collections import Counter


def sum_counters(counters: List[Counter]) -> Counter:
    """
    Recursive counter with a O(log(n)) Complexity
    """
    length = len(counters)
    if length > 10:
        c1 = sum_counters(counters[: int(length / 2)])
        c2 = sum_counters(counters[int(length / 2) :])
        return sum([c1, c2], Counter())
    else:
        return sum(counters, Counter())
