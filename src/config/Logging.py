import logging
from config.database_config import DatabaseLogs

class InfoErrorFilter(logging.Filter):
    """Filter to record INFO and ERROR only."""
    def filter(self, record):
        return record.levelno in (logging.INFO, logging.ERROR)

class Logger:
    _logger = None  # Class variable to store the logger and avoid duplicates
    @staticmethod
    def get_logger():
        if Logger._logger is None:
            logger = logging.getLogger("AttendanceLogger")
            logger.setLevel(logging.DEBUG)

            if not logger.hasHandlers():
                full_formatter = logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                )

                console_formatter = logging.Formatter("%(levelname)s - Line %(filename)s:%(lineno)d: %(message)s")

                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.DEBUG)
                console_handler.setFormatter(console_formatter) 
                logger.addHandler(console_handler)

                sqlite_handler = DatabaseLogs()
                sqlite_handler.setLevel(logging.INFO)
                sqlite_handler.setFormatter(full_formatter)
                logger.addHandler(sqlite_handler)

            Logger._logger = logger  # Guardar instancia en la variable de clase

        return Logger._logger
