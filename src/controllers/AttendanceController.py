
import json
import time
import traceback
from typing import Dict, List, Optional
from datetime import datetime
from models.user.UserRepository import UserRepository
from models.attendance.AttendanceProcessor import AttendanceProcessor
from config.FilePathManager import FilePathManager
from controllers.DeviceController import DeviceController
from controllers.FileHandler import AttendanceFileHandler
from utils.to_JSON import ToJSON 
from models.device.Device import Device
from models.attendance.AttendanceProcessor import AttendanceProcessor
from config.Logging import Logger

class AttendanceController:
    def __init__(self, connector, device_controller: Optional[DeviceController] = None):

        self.connector = connector
        self.device_controller = device_controller or DeviceController(connector)
        self.view = ToJSON()
        self.device_info = None
        self.log = Logger().get_logger()

    def _ensure_device_info(self) -> None:
        if not self.device_info:
            self.log.debug("Fetching device information...")
            self.device_info = self.device_controller.fetch_device_info()  # Use fetch_device_info directly
            if self.device_info:
                self.log.debug("Device information saved successfully")
            else:
                self.log.error("Failed to save device information")
                raise ValueError("Could not get device info")

    def _get_attendance_data(self, conn) -> tuple:
        user_repo = UserRepository(self.connector)
        users_info = user_repo.get_users_info()
        
        # Asegurarnos de que tengamos la info del dispositivo
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

        try:
            self.connector.disconnect()
        except Exception as e:
            self.log.error(f"Error closing connection: {e}")

    def process_attendance(self) -> List:
        retry_interval = 60  # Intervalo entre intentos (en segundos)

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
                    continue  # Volver a intentar

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
                
                self.log.info(f"Total records: {len(filtered_attendance)}")
                return filtered_attendance  # Si todo va bien, finaliza la función

            except ConnectionError as e:
                self.log.error(f"Connection error: {e}")
                self.log.error(traceback.format_exc())
            except Exception as e:
                self.log.error(f"Error processing attendance: {str(e)}")

            self.log.warning(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)  # Espera antes de volver a intentar

    @staticmethod
    def _merge_records(existing: Dict, new: Dict) -> Dict:
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