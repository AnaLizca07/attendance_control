import time
import os
from typing import Optional
from dotenv import load_dotenv # type: ignore
from config.zk_connector import ZKConnector
from config.time_sync import TimeSync
from controllers.AttendanceController import AttendanceController
from config.Logging import Logger


class AttendanceService:
    """
    Service that schedules and executes attendance data processing at specific times.
    
    This service runs as a continuous process, checking the current time against
    a configured execution time. When the times match, it triggers the attendance
    data processing through the attendance controller.
    
    Attributes:
        execution_time (str): Time when the service should execute (format: "HH:MM").
        time_sync (TimeSync): Utility for getting synchronized time.
        connector (ZKConnector): Connector for communicating with ZK devices.
        controller (AttendanceController): Controller for attendance data processing.
        logger: Logger instance for event logging.
    """
    def __init__(self):
        """
        Initializes the attendance service with components and configuration.
        
        Loads execution time from environment variables and initializes required
        components for time synchronization, device connection, and data processing.
        
        Raises:
            ValueError: If EXECUTION_TIME is not set in environment variables.
        """
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
        """
        Processes attendance data through the attendance controller.
        
        This method is called when the execution time is reached. It logs the
        start of data collection and delegates the actual processing to the
        attendance controller.
        """
        try:
            self.logger.debug(f"\n{'='*50}")
            self.logger.debug("Initiating data collection...")
            self.logger.debug(f"\n{'='*50}")
            self.controller.process_attendance()
        except Exception as e:
            self._handle_error(f"Error processing attendance: {str(e)}")

    def should_execute(self, current_time: Optional[str]) -> bool:
        """
        Determines if processing should occur based on the current time.
        
        Args:
            current_time (Optional[str]): Current time in "HH:MM" format.
            
        Returns:
            bool: True if the current time matches the execution time, False otherwise.
        """
        should_run = current_time == self.execution_time
        if should_run:
            self.logger.debug(f"Time match! Current: {current_time}, Scheduled: {self.execution_time}")
        return should_run

    def run(self) -> None:
        """
        Main service loop that runs continuously.
        
        This method implements the service's main loop, which:
        1. Gets the current synchronized time
        2. Checks if execution should occur
        3. Processes attendance data when the execution time is reached
        4. Handles errors with appropriate logging and recovery
        
        The loop runs indefinitely with short sleep intervals between iterations.
        """
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
        """
        Centralizes error handling for the service.
        
        Args:
            error_message (str): Error message to log.
        """
        self.logger.error(f"Error: {error_message}")