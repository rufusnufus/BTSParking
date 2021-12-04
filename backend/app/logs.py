import logging
from logging.config import dictConfig

from app.schemas.logs import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("backend")
