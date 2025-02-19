import time
import os
from typing import Optional
from dotenv import load_dotenv
from config.zk_connector import ZKConnector
from config.time_sync import TimeSync
from controllers.AttendanceController import AttendanceController
from services.APIClient import APIClient


class AttendanceService:
    def __init__(self):
        load_dotenv()
        self.execution_time = os.getenv('EXECUTION_TIME')
        print(f"Loaded EXECUTION_TIME: {self.execution_time}")

        #Sistem components
        self.time_sync = TimeSync()
        self.connector = ZKConnector()
        self.controller = AttendanceController(self.connector)
        self.api_client = APIClient()
        
        #Config validation
        if not self.execution_time:
            raise ValueError("EXECUTION_TIME not set in environment variables")


    def process_attendance_data(self) -> None:
        try:
            print(f"\n{'='*50}")
            print("Initiating data collection...")
            print(f"\n{'='*50}")

            attendance_data = self.controller.process_attendance()
            if attendance_data:
                print("\nSending attendance data to API...")
                if self.api_client.send_attendance_data(attendance_data):
                    print("Attendance data sent successfully")
                else:
                    print("Failed to send attendance data to API")

                device_info = self.controller.device_info
                if device_info:
                    print("\nSending device data to API...")
                    if self.api_client.send_device_data(device_info.__dict__):
                        print("Device data sent successfully")
                    else:
                        print("Failed to send device data to API")
        except Exception as e:
            self._handle_error(f"Error processing attendance: {str(e)}")


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
                
                if not ntp_time:
                    self._handle_error("Failed to get current time")
                    time.sleep(10)
                    continue

                if ntp_time != last_execution_time:
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

    def _send_data_to_api(self, data: dict, is_device_data: bool = False) -> bool:
        try:
            if is_device_data:
                return self.api_client.send_device_data(data)
            return self.api_client.send_attendance_data(data)
        except Exception as e:
            self._handle_error(f"Error sending data to API: {str(e)}")
            return False