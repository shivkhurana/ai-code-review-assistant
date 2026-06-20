import logging
from typing import Dict, Any


def configure_logger() -> logging.Logger:
    logger = logging.getLogger("conversational_ai_pipeline")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def log_event(message: str, extra: Dict[str, Any] = None) -> None:
    logger = configure_logger()
    if extra:
        logger.info(f"{message} | {extra}")
    else:
        logger.info(message)
