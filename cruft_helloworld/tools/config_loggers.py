import collections
from logging.config import dictConfig
from typing import Iterable


def nested_update(d, u):
    """
    >>> {**{"toto": {"tata": 42, "titi": 7}}, **{"toto": {"titi": 42}, "abc": 11}}
    {'toto': {'titi': 42}, 'abc': 11}
    >>> nested_update({"toto": {"tata": 42, "titi": 7}}, {"toto": {"titi": 42}, "abc": 11})
    {'toto': {'tata': 42, 'titi': 42}, 'abc': 11}
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = nested_update(d.get(k, type(v)()), v)
        else:
            d[k] = v
    return d


def config_loggers(default_logger_level: str = "INFO"):
    """"""
    default_logging_handler = "human_readable-colored-stdout"
    logging_config = None

    default_loggers_libs_config = {
        "handlers": [default_logging_handler],
        "propagate": True,
        "level": default_logger_level,
    }
    libs_names: Iterable[str] = ()

    default_logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "human_readable": {
                "format": "%(asctime)s "
                "[%(name)s:%(threadName)s] "
                "%(levelname)s "
                "%(message)s "
                "(%(filename)s:%(funcName)s:%(lineno)d)",
            },
            "human_readable-colored": {
                "format": "%(asctime)s "
                "[%(bold)s%(name)s%(reset)s:%(threadName)s] "
                "%(log_color)s%(levelname)-8s%(reset)s "
                "%(message)s "
                "(%(bold)s%(filename)s%(reset)s:%(funcName)s:%(lineno)d)",
                "()": "colorlog.ColoredFormatter",
            },
        },
        "handlers": {
            "human_readable-stdout": {
                "level": default_logger_level,
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "human_readable",
                "filters": [],
            },
            "human_readable-colored-stdout": {
                "level": default_logger_level,
                "class": "colorlog.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "human_readable-colored",
                "filters": [],
            },
        },
        "loggers": {
            "root": {"handlers": [], "level": "NOTSET"},
            "cruft_helloworld": {
                "handlers": [default_logging_handler],
                "propagate": True,
                "level": default_logger_level,
            },
            **{lib_name: default_loggers_libs_config for lib_name in libs_names},
        },
    }

    dictConfig(nested_update(default_logging_config, logging_config or {}))
