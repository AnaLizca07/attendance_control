
import json
from typing import Dict, List, Optional
from datetime import datetime
from models.user.UserRepository import UserRepository
from models.attendance.AttendanceProcessor import AttendanceProcessor
from config.FilePathManager import FilePathManager
from controllers.DeviceController import DeviceController
from controllers.FileHandler import AttendanceFileHandler
from utils.to_JSON import ToJSON 

class AttendanceController:
    def __init__(self, connector, device_controller: Optional[DeviceController] = None):

        self.connector = connector
        self.device_controller = device_controller or DeviceController(connector)
        self.view = ToJSON()
        self.device_info_saved = False

    def _ensure_device_info(self) -> None:

        if not self.device_info_saved:
            print("\nFetching device information...")
        if self.device_controller.get_device_info():
            self.device_info_saved = True
            print("Device information saved successfully")
        else:
            print("Failed to save device information")

    def _get_attendance_data(self, conn) -> tuple:

        user_repo = UserRepository(self.connector)
        users_info = user_repo.get_users_info()
        
        processor = AttendanceProcessor(self.connector)
        filtered_attendance = processor.get_daily_attendance()
        
        return users_info, filtered_attendance

    def _close_connection(self) -> None:

        try:
            self.connector.disconnect()
        except Exception as e:
            print(f"Error closing connection: {e}")

    def process_attendance(self) -> List:

        try:
            self._ensure_device_info()
            
            conn = self.connector.connect()
            if not conn:
                raise ConnectionError("Connection failed")

            users_info, filtered_attendance = self._get_attendance_data(conn)
            
            if not filtered_attendance:
                print("Record dont found")
                return []

            file_handler = AttendanceFileHandler(
                FilePathManager().get_json_filename(datetime.now().date())
            )

            processor = AttendanceProcessor(conn)
            attendance_records = processor.process_user_attendance(users_info, filtered_attendance)
            
            existing_records = file_handler.read_existing_records()
            merged_records = self._merge_records(existing_records, attendance_records)
            
            file_handler.save_records(merged_records)
            
            print(f"\nTotal records: {len(filtered_attendance)}")
            return filtered_attendance

        except ConnectionError as e:
            print(f"Connection error: {e}")
            return []
        except Exception as e:
            print(f"Error processing attendance: {str(e)}")
            return []
        finally:
            self._close_connection()

    @staticmethod
    def _merge_records(existing: Dict, new: Dict) -> Dict:
        merged = existing.copy()
        
        for user_id, new_records in new.items():
            if user_id not in merged:
                merged[user_id] = new_records
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

        return merged