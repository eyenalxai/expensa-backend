import logging

logger = logging

logger.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",  # noqa: WPS323 %-style
    datefmt="%Y-%m-%d %H:%M:%S",  # noqa: WPS323 %-style
)
