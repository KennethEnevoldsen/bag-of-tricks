from typing import Iterable
import random


def shuffle_buffer(x: Iterable, buffer_size: int) -> Iterable:
    """Creates shuffle buffer from iterable.

    Args:
        x (Iterable): An iterable you want shuffled
        buffer_size (int): The buffer shuffle

    Returns:
        Iterable: An iterable which is shuffled using a shuffle buffer

    Example:
        >>> shuffled = shuffle_buffer(x =[1,2, 3, 4, 5], buffer_size=2)
        >>> print(list(shuffled))
        [2, 1, 4, 3, 5]
    """
    iter_x = iter(x)

    shufbuf = []
    try:
        for i in range(buffer_size):
            shufbuf.append(next(iter_x))
    except StopIteration:
        buffer_size = len(shufbuf)

    while True:
        try:
            item = next(iter_x)
            i = random.randint(0, buffer_size - 1)
            yield shufbuf[i]
            shufbuf[i] = item
        except StopIteration:
            break
    while shufbuf:
        yield shufbuf.pop()
