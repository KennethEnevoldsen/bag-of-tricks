from typing import Callable


def multigen(gen_func: Callable, *args, **kwargs) -> Callable:
    """From a generator create a reapeatable generator

    Args:
        gen_func (Callable): Generator function

    Returns:
        Callable: The reapeatable generator

    Examples:
        >>> def gen_fun():
        >>>   for i in range(4):
        >>>     yield i
        >>> mgen = multigen(gen_fun)
        >>> list(mgen)
        [1,2, 3, 4]
        >>> list(mgen)
        [1,2, 3, 4]
    """

    class _multigen:
        def __init__(self, *args, **kwargs):
            # save argument to pass forward
            self.__args = args
            self.__kwargs = kwargs

        def __iter__(self):
            # create generator with args
            return gen_func(*self.__args, **self.__kwargs)

    return _multigen()
