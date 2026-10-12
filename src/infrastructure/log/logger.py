import logging
import sys

from pythonjsonlogger.json import JsonFormatter


def setup_logging(level: int = logging.INFO) -> None:
    """Install a JSON handler on the root logger.

    Call this explicitly from the application entrypoint. Unlike
    ``logging.basicConfig`` this always takes effect, even when the root
    logger was already configured by pytest, uvicorn or gunicorn.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(filename)s %(lineno)d %(message)s",
            rename_fields={
                "asctime": "timestamp",
                "levelname": "level",
                "name": "logger",
                "filename": "file",
                "lineno": "line",
            },
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
    )

    root = logging.getLogger()
    for existing in root.handlers[:]:
        root.removeHandler(existing)
    root.addHandler(handler)
    root.setLevel(level)


logger = logging.getLogger(__name__)
