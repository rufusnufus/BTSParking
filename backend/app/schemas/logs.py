# Reference: https://stackoverflow.com/a/67937084

import os
import logging

from pydantic import BaseModel

info_target = os.path.join("/home/app/logs", "backend_info_logs.log")


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "backend"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "info": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": info_target,
            "level": "INFO",
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 500000,
            "backupCount": 4,
        },
    }
    loggers = {
        "backend": {"handlers": ["console"], "level": LOG_LEVEL},
    }
