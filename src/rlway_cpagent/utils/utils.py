"""
Utilities
"""


def greet(person: str) -> str:
    r"""returns a string saying hello to a person

    Note
    ----
    Does not print.

    Warning
    -------
    Use it wisely!

    Tip
    ---
    The ancestor of the C language was called ... B ;)

    Parameters
    ----------
    person: str, mandatory
        the name of the person to greet

    Raises
    ------
    TypeError
        when input argument is not a string

    Examples
    --------

    >>> greet("ED")
        Hello ED!
    """
    if not isinstance(person, str):
        raise TypeError(f"Input must be integer : Invalid type {type(person)} ({person}). ")

    msg = f"Hello {person}!"
    return msg
