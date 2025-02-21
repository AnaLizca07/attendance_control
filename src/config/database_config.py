import logging
import sqlite3
from pathlib import Path

class DatabaseLogs(logging.Handler):
    def __init__(self, db_folder="data", db_name="attendance_logs.db"):
        super().__init__()

        self.db_folder = Path(__file__).parent.parent / db_folder
        self.db_folder.mkdir(parents=True, exist_ok=True)
        self.db_path = self.db_folder / db_name

        self._initialize_db()

    def _initialize_db(self):
        """Create the table in the database if it does not exist."""
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
        """Saves the log in the database."""
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
        """Correctly closes the handler."""
        super().close()
