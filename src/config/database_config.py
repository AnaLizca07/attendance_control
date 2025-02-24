import logging
import sqlite3
from pathlib import Path

class DatabaseLogs(logging.Handler):
    """
    Custom logging handler that stores log entries in an SQLite database.
    
    This handler extends Python's logging.Handler to provide persistent storage
    of log messages in an SQLite database. It automatically creates the database
    and required table structure if they don't exist.
    
    Attributes:
        db_folder (Path): Directory path where the database file is stored.
        db_path (Path): Full path to the SQLite database file.
    """
    def __init__(self, db_folder="data", db_name="attendance_logs.db"):
        """
        Initializes the database logging handler.
        
        Args:
            db_folder (str): Folder name for the database location, relative to
                            the parent directory of this file. Defaults to "data".
            db_name (str): Name of the SQLite database file. Defaults to "attendance_logs.db".
        """
        super().__init__()

        self.db_folder = Path(__file__).parent.parent / db_folder
        self.db_folder.mkdir(parents=True, exist_ok=True)
        self.db_path = self.db_folder / db_name

        self._initialize_db()

    def _initialize_db(self):
        """
        Creates the log table in the database if it does not exist.
        
        The table structure includes:
        - id: Autoincremented primary key
        - timestamp: When the log entry occurred
        - status: Log level (INFO, ERROR, etc.)
        - message: The raw log message
        - logs: The formatted log message
        - created_at: When the log entry was created in the database
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT NOT NULL,
                    logs TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def emit(self, record):
        """
        Saves the log record in the database.
        
        This method is called by the logging system when a log message needs
        to be processed. It formats the log record (if a formatter is set)
        and stores it in the database.
        
        Args:
            record: The log record to be processed and stored.
        """
        if self.formatter:
            log_time = self.formatter.formatTime(record, self.formatter.datefmt)
            log_message = self.format(record)
        else:
            log_time = record.created
            log_message = record.msg

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attendance_logs (timestamp, status, message, logs, created_at) 
                VALUES (?, ?, ?, ?, ?)
            """, (log_time, record.levelname, record.msg, log_message, log_time))
            conn.commit()

    def close(self):
        """
        Correctly closes the handler.
        
        This method is called during shutdown of the logging system
        to ensure proper cleanup of resources.
        """
        super().close()
