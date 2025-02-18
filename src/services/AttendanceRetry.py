import sqlite3
import logging
import os
import time
import threading

class AttendanceRetry:
    def __init__(self, attendance_service):
        self.db_path = "attendance_retry.db"
        self.attendance_service = attendance_service  # Servicio de asistencia
        self._initialize_db()
        os.makedirs("logs", exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            filename="logs/attendance_service.log",
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        # Iniciar el hilo para procesar asistencia en segundo plano
        self.start_retry_loop()

    def _initialize_db(self):
        """Crea la tabla si no existe."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pending_attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    attempts INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'pending',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_pending_record(self, attendance_data):
        """Guarda la asistencia pendiente en la base de datos."""
        print("⚠️ Guardando asistencia como pendiente debido a error de conexión.")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pending_attendance (data, attempts, status) 
                VALUES (?, 0, 'pending')
            """, (str(attendance_data),))
            conn.commit()
        logging.warning("⚠️ Asistencia guardada como pendiente.")

    def process_pending_records(self):
        """Procesa los registros pendientes de manera indefinida hasta que haya conexión."""
        while True:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, data, attempts FROM pending_attendance WHERE status = 'pending'")
                pending_records = cursor.fetchall()

            if pending_records:
                for record in pending_records:
                    record_id, data, attempts = record
                    try:
                        logging.info(f"🔄 Reintentando asistencia ID {record_id}, intento {attempts + 1}...")

                        if self.attendance_service.is_connected():
                            success = self.attendance_service.controller.process_attendance()
                            if success:
                                self.delete_record(record_id)
                                logging.info(f"✅ Asistencia ID {record_id} procesada correctamente.")
                            else:
                                self.increment_attempt(record_id)
                        else:
                            logging.warning("❌ Sin conexión. Reintentando en 30 segundos...")
                    except Exception as e:
                        logging.error(f"❌ Error al procesar asistencia ID {record_id}: {str(e)}")
                        self.increment_attempt(record_id)

            time.sleep(30)  # Esperar 30 segundos antes de volver a intentar

    def increment_attempt(self, record_id):
        """Aumenta el contador de intentos fallidos."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE pending_attendance SET attempts = attempts + 1 WHERE id = ?", (record_id,))
            conn.commit()

    def delete_record(self, record_id):
        """Elimina el registro después de procesarlo correctamente."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pending_attendance WHERE id = ?", (record_id,))
            conn.commit()

    def start_retry_loop(self):
        """Ejecuta la reintento en un hilo separado."""
        retry_thread = threading.Thread(target=self.process_pending_records, daemon=True)
        retry_thread.start()
