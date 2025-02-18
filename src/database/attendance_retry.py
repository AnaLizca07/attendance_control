import sqlite3

class SQLiteDB:
    def __init__(self, db_name="attendance.db"):
        self.db_name = db_name
        self._initialize_db()

    def _initialize_db(self):
        """Crea la tabla de asistencia si no existe"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    status TEXT DEFAULT 'pending'
                )
            ''')
            conn.commit()

    def get_connection(self):
        """Devuelve una conexión activa a la base de datos"""
        return sqlite3.connect(self.db_name)
