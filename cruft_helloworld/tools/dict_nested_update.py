import collections
from typing import Dict, Mapping, Union


def nested_update(dict_1: Dict, dict_2: Union[Dict, Mapping]):
    """
    >>> d1 = {"toto": {"tata": 42, "titi": 7}}
    >>> d2 = {"toto": {"titi": 42}, "abc": 11}
    >>> {**d1, **d2}    # classic dicts merge
    {'toto': {'titi': 42}, 'abc': 11}
    >>> nested_update(d1, d2)   # extended/nested dicts merge ("tata" is preserved)
    {'toto': {'tata': 42, 'titi': 42}, 'abc': 11}
    """
    # https://www.python.org/dev/peps/pep-0448/
    return {
        **dict_1,
        **{
            k: nested_update(dict_1.get(k, type(v)()), v)
            if isinstance(v, collections.abc.Mapping)
            else v
            for k, v in dict_2.items()
        },
    }
