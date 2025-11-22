import logging

def get_logger(name: str):
    """
    Creates a formatted logger instance for consistent debug/info output.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Formatter for readable log output
    formatter = logging.Formatter(
        "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger
