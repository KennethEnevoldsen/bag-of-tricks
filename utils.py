"""
a script containing a bunch of utility functions
"""


def create_run_name(custom_name: str = None,
                    date: bool = True,
                    date_format: str = '%Y-%m-%d-%H.%M',
                    n_slugs: int = 2,
                    suffix: str = ""):
    """
    custom_name (str|None): custom name of the run, typically with a date
    added if it is none it will use the slug 

    Example:
    >>> run_name = create_run_name(date=True, date_format="%Y-%m-%d", \
                                   n_slugs=2)
    >>> len(run_name.split("_")) == 2
    True
    >>> run_name = create_run_name(date=False, n_slugs=2)
    >>> len(run_name.split("-")) >= 2
    True
    """
    from coolname import generate_slug

    if custom_name is None:
        name = generate_slug(n_slugs)
    else:
        name = custom_name

    if date:
        from datetime import datetime
        name = datetime.today().strftime('%Y-%m-%d-%H.%M') + "_" + name

    name += suffix
    return name


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
