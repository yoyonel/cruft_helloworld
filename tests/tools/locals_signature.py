import inspect
from typing import Callable, Dict


def locals_func_to_dict_signature_params(dict_locals: Dict, func: Callable) -> Dict:
    return {
        p.name: dict_locals[p.name]
        # https://www.programcreek.com/python/example/81294/inspect.signature
        for p in inspect.signature(func).parameters.values()
        if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    }
