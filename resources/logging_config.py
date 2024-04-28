#!/usr/bin/env python3

from functools import cache
import logging
import jsonformatter
import os

TIME_FORMAT = "[%Y-%m-%d %H:%M:%S.%f]"
LOG_FORMAT = "[%(name)s] %(message)s"

from rich.logging import RichHandler

logging.basicConfig(
    level=os.environ.get("LRH_LOGLEVEL", "INFO"),
    format=f"{LOG_FORMAT}",
    datefmt=f"{TIME_FORMAT}",
    handlers=[RichHandler()],
)


@cache
def get_logger(name, json=True) -> logging.Logger:
    if json:
        return get_json_logger(name)
    else:
        return get_normal_logger(name)


@cache
def get_normal_logger(name) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(name)

    logging.basicConfig(
        level=os.environ.get("LRH_LOGLEVEL", "INFO"),
        format=f"{LOG_FORMAT}",
        datefmt=f"{TIME_FORMAT}",
        handlers=[RichHandler()],
    )

    return logger


@cache
def get_json_logger(name) -> logging.Logger:
    STRING_FORMAT = """{
    "Name":            "name",
    "Level":       "levelname",
    "LogTime":         "asctime",
    "Message":         "message"}"""

    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    jformatter = jsonformatter.JsonFormatter(STRING_FORMAT, datefmt="%Y-%m-%dT%H:%M:%S")
    sh = logging.StreamHandler()
    sh.setFormatter(jformatter)
    logger.addHandler(sh)

    return logger
