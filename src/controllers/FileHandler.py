from pathlib import Path
from utils.to_JSON import ToJSON
import json
from typing import Dict
from datetime import datetime
from models.device.DeviceInfo import DeviceInfo
from utils.FileNameSanitizer import FileNameSanitizer
    
class DeviceFileManager:
    def __init__(self):
        self.documents_dir = Path.home()/ 'Documents'
        self.base_dir = self.documents_dir / 'output'
        self.device_dir = self.base_dir / 'device_info'
        self.ensure_directory()
        
    def ensure_directory(self) -> None:

        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.device_dir.mkdir(exist_ok=True)
        
    def get_device_filepath(self, device_name: str) -> Path:
        sanitized_name = FileNameSanitizer.sanitize(device_name)
        current_date = datetime.now().strftime('%Y%m%d')
        filename = f"device_{sanitized_name}_{current_date}.json"
        return self.device_dir / filename 
        
    def save_device_info(self, device_info: 'DeviceInfo') -> None:
        try:
            self.ensure_directory()
            filepath = self.get_device_filepath(device_info.device_name)
            
            json_output = {
                'device_name': device_info.device_name,
                'device_id': device_info.device_id,
                'description': {
                    'serial_number': device_info.description.serial_number,
                    'mac_address': device_info.description.mac_address,
                    'network': {
                        'ip': device_info.description.network_config.ip,
                        'gateway': device_info.description.network_config.gateway
                    }
                }
            }
            
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            ToJSON().save_json_output(json_output, str(filepath))
            print(f"\nDevice info saved to: {filepath}")
            
        except Exception as e:
            print(f"Error saving device info: {e}")
            raise

class AttendanceFileHandler:
    def __init__(self, filename: str):
            self.documents_dir = Path.home()/ 'Documents'
            self.base_dir = self.documents_dir / 'output'
            self.attendance_dir = self.base_dir / 'attendance'
            self.ensure_directory()
            self.filename = self.base_dir / filename

    def ensure_directory(self) -> None:
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.attendance_dir.mkdir(exist_ok=True)

    def read_existing_records(self) -> Dict:
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_records(self, records: Dict) -> None:
        try:
            self.ensure_directory()
            
            print(f"\nPreparing to save records...")
            print(f"Records structure: {type(records)}")
            print(f"Number of users in records: {len(records)}")
            if records:
                sample_user = next(iter(records))
                print(f"Sample user records: {len(records[sample_user])}")
            
            with open(self.filename, "w") as file:
                json.dump(records, file, indent=4)
            print(f"Records saved successfully to: {self.filename}")
            
        except Exception as e:
            print(f"Error saving records: {e}")
            import traceback
            print(traceback.format_exc())
            raise