import logging
from config.database_config import DatabaseLogs

class InfoErrorFilter(logging.Filter):
    """
    Filter class for Python's logging system that only allows INFO and ERROR level messages.
    
    This filter is used to restrict log handlers to only process messages with
    specific logging levels, in this case INFO and ERROR.
    
    Attributes:
        Inherits from logging.Filter with no additional attributes.
    """
    def filter(self, record):
        """
        Determines if a log record should be processed based on its level.
        
        Args:
            record: The log record to be checked.
            
        Returns:
            bool: True if the record's level is either INFO or ERROR, otherwise False.
        """
        return record.levelno in (logging.INFO, logging.ERROR)

class Logger:
    """
    Singleton logger manager that provides a centralized logging configuration.
    
    This class implements a singleton pattern to ensure that only one logger instance
    is created across the application. It configures multiple handlers for different
    logging destinations (console and database) with appropriate formatters.
    
    Attributes:
        _logger: Class-level variable that stores the singleton logger instance.
    """
    _logger = None 
    @staticmethod
    def get_logger():
        """
        Returns the singleton logger instance, creating it if it doesn't exist.
        
        This method ensures that the logger is only created once and configures:
        1. A console handler with a simple formatter showing log level, filename,
           line number, and message.
        2. A database handler for persistent storage of INFO and ERROR level messages
           with a detailed formatter including timestamp, log level, and message.
        
        Returns:
            logging.Logger: Configured logger instance.
        """
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
