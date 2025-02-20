import sqlite3
from pathlib import Path

class DatabaseLogs:
    def __init__(self, db_folder="data", db_name="attendance_logs.db"):
        # Define the path to the database in the 'data' folder
        self.db_folder = Path(__file__).parent.parent / db_folder
        self.db_folder.mkdir(parents=True, exist_ok=True)  # Ensures that the folder exists
        self.db_path = self.db_folder / db_name

        self._initialize_db()

    def _initialize_db(self):
        """Create the database if it does not exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    logs TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def emit(self, record):
        """Inserta un log en la base de datos."""
        log_message = self.format(record)
        self.cursor.execute("INSERT INTO logs (level, message) VALUES (%s, %s)", (record.levelname, log_message))
        self.connection.commit()
    
    def close(self):
        """Cierra la conexión con la base de datos."""
        self.cursor.close()
        self.connection.close()
        super().close()