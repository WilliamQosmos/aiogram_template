import logging.config
from pathlib import Path

import yaml


logger = logging.getLogger(__name__)


def setup_logging():
    try:
        with open(Path("app/config/logging.yaml"), "r") as f:
            logging_config = yaml.safe_load(f)
        logging.config.dictConfig(logging_config)
        logger.info("Logging configured successfully")
    except IOError:
        logging.basicConfig(level=logging.DEBUG)
        logger.warning("logging config file not found, use basic config")
