import time
import os
from typing import Optional
from dotenv import load_dotenv
from config.zk_connector import ZKConnector
from config.time_sync import TimeSync
from controllers.AttendanceController import AttendanceController

class AttendanceService:
    def __init__(self):
        load_dotenv()
        self.execution_time = os.getenv('EXECUTION_TIME')
        self.time_sync = TimeSync()
        self.connector = ZKConnector()
        self.controller = AttendanceController(self.connector)
        
        if not self.execution_time:
            raise ValueError("EXECUTION_TIME not set in environment variables")

    def process_attendance_data(self) -> None:
        try:
            print("Initiating data collection...")
            self.controller.process_attendance()
        except Exception as e:
            self._handle_error(f"Error processing attendance: {str(e)}")

    def should_execute(self, current_time: Optional[str]) -> bool:
        return current_time == self.execution_time

    def run(self) -> None:
        print(f"Service started. Scheduled execution time: {self.execution_time}")
        
        while True:
            try:
                ntp_date, ntp_time = self.time_sync.get_date_time()
                
                if not ntp_time:
                    self._handle_error("Failed to get current time")
                    time.sleep(30)
                    continue

                if self.should_execute(ntp_time):
                    self.process_attendance_data()

                time.sleep(30)  

            except Exception as e:
                self._handle_error(f"Unexpected error in main loop: {str(e)}")
                time.sleep(60)  # Esperar más tiempo en caso de error
    
    def _handle_error(self, error_message: str) -> None:
        print(f"Error: {error_message}")