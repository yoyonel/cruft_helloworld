from inspect import signature
from typing import Any


def get_default_parameter(obj, parameter_name: str) -> Any:
    """
    >>> get_default_parameter(signature, "follow_wrapped")
    True
    """
    return signature(obj).parameters[parameter_name].default
