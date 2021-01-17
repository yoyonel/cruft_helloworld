from inspect import getmembers
from typing import Callable


def build_target(target: Callable) -> str:
    """
    >>> build_target(getmembers)
    'inspect.getmembers'
    """
    return f"{dict(getmembers(target))['__module__']}.{target.__qualname__}"
