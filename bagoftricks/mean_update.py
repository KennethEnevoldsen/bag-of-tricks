from typing import Iterable


def mean_update(x: Iterable[float], start_mean: float = 0, n: int = 0):
    """
    A mean update which takes in an iterable and returns mean, but never expands the
    whole document.

    following the formula
    mu_n = mu_{n-1} + frac{1}{k}(mu_{n-1} - x_i)
    """

    def __mean_update(x, mu, n):
        return mu + 1 / n * (mu - x)

    iter_x = iter(x)
    if n == 0:
        mu = next(iter_x)
        n = 1
    for v in iter_x:
        mu = __mean_update(x, mu, n)
        n += 1
    return mu
