import json 
import os
import time
from datetime import datetime
from config.FilePathManager import FilePathManager
from services.NetworkRetryService import NetworkRetry
from utils.to_JSON import ToJSON

class AttendanceRecovery:
    """
    Maneja la lógica de asistencia, permitiendo registrar, guardar y reintentar envíos fallidos.
    """
    def __init__(self):
        self.file_manager = FilePathManager()
        self.retry_manager = NetworkRetry()
        self.attendance_file = self.file_manager.get_json_filename(datetime.today(), 'attendance')

    def save_attendance(self, attendance_data):
        """Guarda la asistencia en un archivo JSON."""
        try:
            if os.path.exists(self.attendance_file):
                with open(self.attendance_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []
            
            data.append(attendance_data)
            ToJSON.save_json_output(data, self.attendance_file)
        except Exception as e:
            print(f"Error saving attendance: {e}")

    def process_attendance(self, send_function):
        """Intenta enviar la asistencia, guardando en reintentos si falla."""
        try:
            with open(self.attendance_file, 'r', encoding='utf-8') as f:
                attendances = json.load(f)
        except FileNotFoundError:
            print("No attendance records found.")
            return
        
        success = []
        for record in attendances:
            try:
                if send_function(record):
                    success.append(record)
                else:
                    self.retry_manager.save_retry(record)
            except Exception as e:
                print(f"Failed to send attendance: {e}")
                self.retry_manager.save_retry(record)
        
        # Guardamos solo los registros no enviados
        failed_attendances = [a for a in attendances if a not in success]
        ToJSON.save_json_output(failed_attendances, self.attendance_file)
