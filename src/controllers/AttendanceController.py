
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

    def _get_attendance_data(self, conn) -> tuple:
        user_repo = UserRepository(self.connector)
        users_info = user_repo.get_users_info()
        
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

            if not self.device_info:
                print("\nFetching device information...")
                self.device_info = self.device_controller.fetch_device_info()
                if not self.device_info:
                    raise ValueError("Could not get device info")
                print("Device information saved successfully")
            
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

            processor = AttendanceProcessor(conn,
                    device=Device(),
                    device_info=self.device_info)
            attendance_records = processor.process_user_attendance(users_info, filtered_attendance)

            attendance_records["id"] = str(int(datetime.now().timestamp()))

            print("Saving records...")
            existing_records = file_handler.read_existing_records()
            merged_records = self._merge_records(existing_records, attendance_records)
            file_handler.save_records(merged_records)
            
            print(f"\nTotal records: {len(filtered_attendance)}")
            return attendance_records

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

        if not existing:
            return new

        if not new:
            return existing
        
        print(f"Existing records: {len(existing.get('users', {}))} users")
        print(f"New records: {len(new.get('users', {}))} users")

        merged = {
            "id": new["id"],
            "serial_number": new["serial_number"],
            "date": new["date"],
            "users": existing.get("users", {}).copy()
        }
        
        for user_id, user_data in new.get("users", {}).items():
            if user_id not in merged["users"]:
                merged["users"][user_id] = user_data
                print(f"Added new user {user_id}")
            else:
                existing_records = set(
                    json.dumps(record, sort_keys=True) 
                    for record in merged["users"][user_id].get("records", [])
                )
                        
                new_records = [
                    record for record in user_data.get("records", [])
                    if json.dumps(record, sort_keys=True) not in existing_records
                ]
                        
                if new_records:
                    merged["users"][user_id]["records"].extend(new_records)
                    merged["users"][user_id]["total_hours"] = str(
                        float(merged["users"][user_id]["total_hours"]) + 
                        float(user_data["total_hours"])
                    )
                
        print(f"Final merged records: {len(merged['users'])} users")
        return merged