import logging
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def setup_logging(level: LogLevel = "INFO") -> None:
    """
        Configures the root logger, if no log level is
        set it uses INFO.
    """

    root_logger = logging.getLogger()
    root_logger.setLevel(level)


    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s:%(lineno)d) - %(message)s"
    )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
