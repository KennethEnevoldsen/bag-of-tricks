from typing import Optional


def create_run_name(
    custom_name: str = None,
    date: bool = True,
    date_format: Optional[str] = "%Y-%m-%d-%H.%M",
    n_slugs: int = 2,
    suffix: str = "",
) -> str:
    """A function for generating run names.

    Args:
        custom_name (str, optional): custom name of the run, with the added date. If None it will use a generated slug.
            Defaults to None.
        date_format (Optional[str], optional): The desired date format. If None the date is not added.
            Defaults to '%Y-%m-%d-%H.%M'.
        n_slugs (int, optional): Number of slugs. Defaults to 2.
        suffix (str, optional): Add a suffix to the name. Defaults to "".

    Returns:
        str: The run name
    """
    from coolname import generate_slug

    if custom_name is None:
        name = generate_slug(n_slugs)
    else:
        name = custom_name

    if date_format:
        from datetime import datetime

        name = datetime.today().strftime("%Y-%m-%d-%H.%M") + "_" + name

    name += suffix
    return name
