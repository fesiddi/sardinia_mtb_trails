import logging


class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """

    def filter(self, record):
        record.function_name = record.funcName
        return True


class Logger:
    logger = None

    @staticmethod
    def setup(name):
        if Logger.logger is None:
            Logger.logger = logging.getLogger(name)
            Logger.logger.addFilter(ContextFilter())
            Logger.logger.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

            # StreamHandler logs to console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            Logger.logger.addHandler(console_handler)

            # FileHandler logs to a file
            file_handler = logging.FileHandler('logfile.log')
            file_handler.setFormatter(formatter)
            Logger.logger.addHandler(file_handler)

    @staticmethod
    def info(message):
        Logger.logger.info(message)

    @staticmethod
    def debug(message):
        Logger.logger.debug(message)

    @staticmethod
    def warning(message):
        Logger.logger.warning(message)

    @staticmethod
    def error(message):
        Logger.logger.error(message)


# Set up the logger
Logger.setup(__name__)
