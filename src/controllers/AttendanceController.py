
import json
import time
import traceback
from typing import Dict, List, Optional
from datetime import datetime
from models.user.UserRepository import UserRepository
from models.attendance.AttendanceProcessor import AttendanceProcessor
from config.FilePathManager import FilePathManager
from controllers.DeviceController import DeviceController
from controllers.FileHandler import AttendanceFileHandler, DeviceFileManager
from utils.to_JSON import ToJSON 
from models.device.Device import Device
from models.attendance.AttendanceProcessor import AttendanceProcessor
from config.Logging import Logger
from services.APIClient import APIClient

class AttendanceController:
    """
        Class that manages attendance processing, device interactions, and data synchronization.
        
        This controller handles device connections, attendance data retrieval, processing,
        storage, and API communication for synchronizing data with remote systems.
        
        Attributes:
            connector: Connection handler for the device.
            device_controller (DeviceController): Controller for device interactions.
            view (ToJSON): Utility for JSON operations.
            device_info: Information about the connected device.
            log: Logger instance for event logging.
            device_file_manager (DeviceFileManager): Manager for device information files.
            api_client (APIClient): Client for API communications.
    """
    def __init__(self, connector, device_controller: Optional[DeviceController] = None):
        """
        Initializes the attendance controller.
        
        Args:
            connector: Connection handler for the device.
            device_controller (Optional[DeviceController]): Controller for device interactions.
                                                           If None, a new DeviceController is created.
        """
        self.connector = connector
        self.device_controller = device_controller or DeviceController(connector)
        self.view = ToJSON()
        self.device_info = None
        self.log = Logger().get_logger()
        self.device_file_manager = DeviceFileManager()
        self.api_client = APIClient()

    def _ensure_device_info(self) -> None:
        """
        Ensures device information is available, fetching it if necessary.
        
        This method checks if device information is already available, and if not,
        it fetches and sends it to the API.
        
        Raises:
            ValueError: If device information cannot be retrieved.
        """
        if not self.device_info:
            self.log.debug("Fetching device information...")
            self.device_info = self.device_controller.fetch_device_info()

            if self.device_info:
                self.log.debug("Device information saved successfully")
                self._send_device_info()
            else:
                self.log.error("Failed to save device information")
                raise ValueError("Could not get device info")

    def _send_device_info(self) -> None:
        """
        Sends device information to the API.
        
        This method reads the device information from the file and sends it to the API
        using the API client.
        """
        try:
            device_file = self.device_file_manager.get_device_filepath(self.device_info.device_name)
            with open(device_file, 'r') as f:
                device_data = json.load(f)

            if self.api_client.send_device_data(device_data):
                self.log.info("Device data sent successfully")
            else:
                self.log.error("Failed to send device data")

        except Exception as e:
            self.log.error(f"Error sending device data to API: {str(e)}")

    def _get_attendance_data(self, conn) -> tuple:
        """
        Retrieves user information and attendance data from the device.
        
        Args:
            conn: Connection to the device.
            
        Returns:
            tuple: A tuple containing (users_info, filtered_attendance).
            
        Raises:
            ValueError: If device information cannot be retrieved.
        """
        user_repo = UserRepository(self.connector)
        users_info = user_repo.get_users_info()
        
        if not self.device_info:
            self.log.debug("Getting device info in controller...")
            self.device_info = self.device_controller.get_device_info()
            if not self.device_info:
                raise ValueError("Could not get device info")
        
        processor = AttendanceProcessor(
            connector=self.connector,
            device=Device(),
            device_info=self.device_info 
        )
        filtered_attendance = processor.get_daily_attendance()
        
        return users_info, filtered_attendance

    def _close_connection(self) -> None:
        """
        Safely closes the connection to the device.
        """
        try:
            self.connector.disconnect()
        except Exception as e:
            self.log.error(f"Error closing connection: {e}")

    def process_attendance(self) -> List:
        """
        Main method to process attendance data with retry mechanism.
        
        This method implements a continuous retry loop to ensure attendance data
        is processed even when temporary issues occur. It:
        1. Ensures device information is available
        2. Connects to the device
        3. Retrieves attendance data
        4. Processes and merges the attendance records
        5. Saves the records to a file
        6. Sends the attendance data to the API
        
        Returns:
            List: Filtered attendance records.
            
        Raises:
            ConnectionError: If connection with the device cannot be established.
        """
        retry_interval = 60

        while True:
            try:
                self.log.debug("Starting attendance processing...")
                self._ensure_device_info()
                
                self.log.debug("Connecting to device...")
                conn = self.connector.connect()
                if not conn:
                    raise ConnectionError("Connection failed")

                self.log.debug("Getting attendance data...")
                users_info, filtered_attendance = self._get_attendance_data(conn)
                
                if not filtered_attendance:
                    self.log.warning("No attendance records found. Retrying in 60 seconds...")
                    time.sleep(retry_interval)
                    continue 

                self.log.debug("Processing records...") 
                file_handler = AttendanceFileHandler(
                    FilePathManager().get_json_filename(datetime.now().date())
                )

                processor = AttendanceProcessor(conn, device=Device(), device_info=self.device_info)
                attendance_records = processor.process_user_attendance(users_info, filtered_attendance)
                
                self.log.debug(f"Found {len(attendance_records)} records")
                existing_records = file_handler.read_existing_records()
                merged_records = self._merge_records(existing_records, attendance_records)
                
                self.log.info("Saving records...")
                file_handler.save_records(merged_records)

                self._send_attendance(file_handler.filename)
                
                self.log.info(f"Total records: {len(filtered_attendance)}")
                return filtered_attendance 

            except ConnectionError as e:
                self.log.error(f"Connection error: {e}")
                self.log.error(traceback.format_exc())
            except Exception as e:
                self.log.error(f"Error processing attendance: {str(e)}")

            self.log.warning(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval) 

    def _send_attendance(self, filename: str) -> None:
        """
        Sends attendance data to the API.
        
        Args:
            filename (str): Path to the file containing attendance data.
        """
        try:
                    with open(filename, 'r') as f:
                        attendance_data = json.load(f)

                    if self.api_client.send_attendance_data(attendance_data):
                        self.log.info("Attendance data sent successfully")
                    else:
                        self.log.error("Failed to send attendance data")

        except Exception as e:
            self.log.error(f"Error sending attendance data to API: {str(e)}")


    @staticmethod
    def _merge_records(existing: Dict, new: Dict) -> Dict:
        """
        Merges existing and new attendance records, avoiding duplicates.
        
        Args:
            existing (Dict): Existing attendance records.
            new (Dict): New attendance records to merge.
            
        Returns:
            Dict: Merged attendance records.
        """
        log_merge = Logger().get_logger()
        log_merge.debug(f"Merging records...")
        log_merge.debug(f"Existing records: {len(existing)} users")
        log_merge.debug(f"New records: {len(new)} users")
        merged = existing.copy()
        
        for user_id, new_records in new.items():
            if user_id not in merged:
                merged[user_id] = new_records
                log_merge.debug(f"Added new user {user_id} with {len(new_records)} records")
                continue

            existing_set = {
                json.dumps(record, sort_keys=True) 
                for record in merged[user_id]
            }
            
            unique_records = [
                record for record in new_records 
                if json.dumps(record, sort_keys=True) not in existing_set
            ]
            
            if unique_records:
                merged[user_id].extend(unique_records)

        log_merge.error(f"Final merged records: {len(merged)} users")
        return merged