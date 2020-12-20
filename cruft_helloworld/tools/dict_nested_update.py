import collections


def nested_update(d, u):
    """
    >>> d1 = {"toto": {"tata": 42, "titi": 7}}
    >>> d2 = {"toto": {"titi": 42}, "abc": 11}
    >>> {**d1, **d2}
    {'toto': {'titi': 42}, 'abc': 11}
    >>> nested_update(d1, d2)
    {'toto': {'tata': 42, 'titi': 42}, 'abc': 11}
    """
    # https://www.python.org/dev/peps/pep-0448/
    return {
        **d,
        **{
            k: nested_update(d.get(k, type(v)()), v)
            if isinstance(v, collections.abc.Mapping)
            else v
            for k, v in u.items()
        },
    }
