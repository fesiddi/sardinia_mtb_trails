import logging


class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """

    def filter(self, record):
        record.function_name = record.funcName
        return True


def setup_logger(name):
    """
    Set up a logger with the given name.
    """
    logger = logging.getLogger(name)
    f = ContextFilter()
    logger.addFilter(f)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s in function %(function_name)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


# Set up the logger
logger = setup_logger(__name__)
