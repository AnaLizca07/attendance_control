import time
import os
from typing import Optional
from dotenv import load_dotenv # type: ignore
from config.zk_connector import ZKConnector
from config.time_sync import TimeSync
from controllers.AttendanceController import AttendanceController
from config.Logging import Logger


class AttendanceService:
    def __init__(self):
        load_dotenv()
        self.execution_time = os.getenv('EXECUTION_TIME')
        self.time_sync = TimeSync()
        self.connector = ZKConnector()
        self.controller = AttendanceController(self.connector)
        self.logger = Logger().get_logger()
        
        self.logger.debug(f"Loaded EXECUTION_TIME: {self.execution_time}")
        if not self.execution_time:
            raise ValueError("EXECUTION_TIME not set in environment variables")

    def process_attendance_data(self) -> None:
        try:
            self.logger.debug(f"\n{'='*50}")
            self.logger.debug("Initiating data collection...")
            self.logger.debug(f"\n{'='*50}")
            self.controller.process_attendance()
        except Exception as e:
            self._handle_error(f"Error processing attendance: {str(e)}")

    def should_execute(self, current_time: Optional[str]) -> bool:
        should_run = current_time == self.execution_time
        if should_run:
            self.logger.debug(f"Time match! Current: {current_time}, Scheduled: {self.execution_time}")
        return should_run

    def run(self) -> None:
        self.logger.debug(f"Service started. Scheduled execution time: {self.execution_time}")
        last_execution_time = None

        while True:
            try:
                ntp_date, ntp_time = self.time_sync.get_date_time()
                self.logger.debug(f"Current time: {ntp_time}")
                
                if not ntp_time:
                    self._handle_error("Failed to get current time")
                    time.sleep(10)
                    continue

                if ntp_time != last_execution_time:
                    self.logger.debug(f"Current time: {ntp_time}")
                    last_execution_time = ntp_time

                if self.should_execute(ntp_time):
                    self.logger.debug(f"Executing at scheduled time: {ntp_time}")
                    self.process_attendance_data()
                    time.sleep(60)
                    self.logger.debug("Completed scheduled execution")

                time.sleep(10)  

            except Exception as e:
                self._handle_error(f"Unexpected error in main loop: {str(e)}")
                time.sleep(30)  
    
    def _handle_error(self, error_message: str) -> None:
        self.logger.error(f"Error: {error_message}")