from logging.config import dictConfig
from typing import Dict, Iterable, Optional

from cruft_helloworld import __project_name__ as application_name
from cruft_helloworld.tools.dict_nested_update import nested_update


def config_loggers(
    default_logger_level: str = "INFO",
    default_logging_handler: str = "human_readable-colored-stdout",
    logging_config: Optional[Dict] = None,
    libs_names: Iterable[str] = (),
) -> None:
    default_loggers_libs_config = {
        "handlers": [default_logging_handler],
        "propagate": True,
        "level": default_logger_level,
    }

    default_logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "human_readable-colored": {
                "format": "%(asctime)s "
                "[%(bold)s%(name)s%(reset)s:%(threadName)s] "
                "%(log_color)s%(levelname)-8s%(reset)s "
                "%(message)s "
                "(%(bold)s%(filename)s%(reset)s:%(funcName)s:%(lineno)d)",
                "()": "colorlog.ColoredFormatter",
                "log_colors": {
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                },
                "datefmt": None,
                "reset": True,
            },
        },
        "handlers": {
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
            application_name: {
                "handlers": [default_logging_handler],
                "propagate": True,
                "level": default_logger_level,
            },
            **{lib_name: default_loggers_libs_config for lib_name in libs_names},
        },
    }

    dictConfig(nested_update(default_logging_config, logging_config or {}))
