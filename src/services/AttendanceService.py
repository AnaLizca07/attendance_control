import time
import os
from typing import Optional
from dotenv import load_dotenv
from config.zk_connector import ZKConnector
from config.time_sync import TimeSync
from controllers.AttendanceController import AttendanceController
from services.NetworkRetryService import NetworkRetry
from services.AttendanceRecoveryService import AttendanceRecovery

class AttendanceService:
    def __init__(self):
        load_dotenv()
        self.execution_time = os.getenv('EXECUTION_TIME')
        print(f"Loaded EXECUTION_TIME: {self.execution_time}")
        
        self.time_sync = TimeSync()
        self.connector = ZKConnector()
        self.controller = AttendanceController(self.connector)
        self.retry_manager = NetworkRetry()
        self.attendance_task = AttendanceRecovery()

        if not self.execution_time:
            raise ValueError("EXECUTION_TIME not set in environment variables")

    def process_attendance_data(self) -> None:
        """
        Intenta procesar la asistencia, maneja errores de conexión
        y delega a AttendanceRecovery si falla.
        """
        try:
            print(f"\n{'='*50}")
            print("Initiating data collection...")
            print(f"\n{'='*50}")
            
            # Primero, procesar cualquier asistencia pendiente
            self.attendance_task.process_attendance(self.controller.process_attendance)

            # Luego, procesar la asistencia actual
            self.controller.process_attendance()

        except Exception as e:
            print(f"Error processing attendance: {str(e)}")
            self.retry_manager.save_pending_execution(self.execution_time)  # Guardar como pendiente

    def should_execute(self, current_time: Optional[str]) -> bool:
        should_run = current_time == self.execution_time
        if should_run:
            print(f"Time match! Current: {current_time}, Scheduled: {self.execution_time}")
        return should_run

    def run(self) -> None:
        print(f"Service started. Scheduled execution time: {self.execution_time}")
        last_execution_time = None

        while True:
            try:
                ntp_date, ntp_time = self.time_sync.get_date_time()
                print(f"Current time: {ntp_time}")
                
                if not ntp_time:
                    self._handle_error("Failed to get current time")
                    time.sleep(10)
                    continue

                if ntp_time != last_execution_time:
                    print(f"Current time: {ntp_time}")
                    last_execution_time = ntp_time

                if self.should_execute(ntp_time):
                    print(f"Executing at scheduled time: {ntp_time}")
                    self.process_attendance_data()
                    time.sleep(60)
                    print("Completed scheduled execution")

                time.sleep(10)  

            except Exception as e:
                self._handle_error(f"Unexpected error in main loop: {str(e)}")
                time.sleep(30)  
                
    def _handle_error(self, error_message: str) -> None:
        print(f"Error: {error_message}")
