
import json
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

class AttendanceController:
    def __init__(self, connector, device_controller: Optional[DeviceController] = None):

        self.connector = connector
        self.device_controller = device_controller or DeviceController(connector)
        self.view = ToJSON()
        self.device_info = None

    def _ensure_device_info(self) -> None:
        if not self.device_info:
            print("\nFetching device information...")
            self.device_info = self.device_controller.fetch_device_info()  # Use fetch_device_info directly
            if self.device_info:
                print("Device information saved successfully")
            else:
                print("Failed to save device information")
                raise ValueError("Could not get device info")

    def _get_attendance_data(self, conn) -> tuple:
        user_repo = UserRepository(self.connector)
        users_info = user_repo.get_users_info()
        
        # Asegurarnos de que tengamos la info del dispositivo
        if not self.device_info:
            print("Getting device info in controller...")
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
            print(f"Error closing connection: {e}")

    def process_attendance(self) -> List:

        try:
            print("Starting attendance processing...")
            self._ensure_device_info()
            
            print("Connecting to device...")
            conn = self.connector.connect()
            if not conn:
                raise ConnectionError("Connection failed")

            print("Getting attendance data...")
            users_info, filtered_attendance = self._get_attendance_data(conn)
            
            if not filtered_attendance:
                print("Record dont found")
                return []

            print("Processing records...") 
            file_handler = AttendanceFileHandler(
                FilePathManager().get_json_filename(datetime.now().date())
            )

            processor = AttendanceProcessor(conn, device=Device(),
                device_info=self.device_info)
            attendance_records = processor.process_user_attendance(users_info, filtered_attendance)
            
            print(f"Found {len(attendance_records)} records")
            existing_records = file_handler.read_existing_records()
            merged_records = self._merge_records(existing_records, attendance_records)
            
            print("Saving records...")
            file_handler.save_records(merged_records)
            
            print(f"\nTotal records: {len(filtered_attendance)}")
            return filtered_attendance

        except ConnectionError as e:
            print(f"Connection error: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            print(traceback.format_exc())
            return []
        except Exception as e:
            print(f"Error processing attendance: {str(e)}")
            return []
        finally:
            print("Closing connection...")
            self._close_connection()

    @staticmethod
    def _merge_records(existing: Dict, new: Dict) -> Dict:
        print(f"\nMerging records...")
        print(f"Existing records: {len(existing)} users")
        print(f"New records: {len(new)} users")
        merged = existing.copy()
        
        for user_id, new_records in new.items():
            if user_id not in merged:
                merged[user_id] = new_records
                print(f"Added new user {user_id} with {len(new_records)} records")
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

        print(f"Final merged records: {len(merged)} users")
        return merged