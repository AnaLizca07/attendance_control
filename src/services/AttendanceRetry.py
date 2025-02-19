import sqlite3
from datetime import datetime
from pathlib import Path

class AttendanceRetry:
    def __init__(self, db_folder="database", db_name="attendance_retry.db"):
        # Define la ruta de la base de datos en la carpeta 'database'
        self.db_folder = Path(__file__).parent / db_folder
        self.db_folder.mkdir(parents=True, exist_ok=True)  # Asegura que la carpeta exista
        self.db_path = self.db_folder / db_name

        self._initialize_db()

    def _initialize_db(self):
        """Crea la base de datos si no existe."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pending_attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_pending_record(self, timestamp):
        """Guarda una fecha de asistencia fallida."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pending_attendance (timestamp) VALUES (?)", (timestamp,))
            conn.commit()

    def get_pending_dates(self):
        """Obtiene todas las fechas de asistencias pendientes."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp FROM pending_attendance")
            return cursor.fetchall()  # Retorna [(id, timestamp), ...]

    def delete_record(self, record_id):
        """Elimina un registro de asistencia pendiente una vez procesado."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pending_attendance WHERE id = ?", (record_id,))
            conn.commit()
