import traceback
from pathlib import Path
from utils.to_JSON import ToJSON
import json
from typing import Dict
from datetime import datetime
from models.device.DeviceInfo import DeviceInfo
from utils.FileNameSanitizer import FileNameSanitizer
from config.Logging import Logger
    
class DeviceFileManager:
    def __init__(self):
        self.log = Logger.get_logger()
        self.base_dir = Path(__file__).parent.parent / 'data'
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
            self.log.debug(f"Device info saved to: {filepath}")
            
        except Exception as e:
            self.log.error(f"Error saving device info: {e}")
            raise

class AttendanceFileHandler:
    """
    Class that manages the storage and retrieval of attendance records.
    
    Attributes:
        log: Logger instance for event logging.
        base_dir (Path): Base directory for attendance data storage.
        filename (Path): Complete path of the attendance records file.
    """
    def __init__(self, filename: str):
        """
        Initializes the attendance file handler.
            
        Args:
            filename (str): Name of the file where the records will be saved.
            
        Note:
            The directory 'attandance_output' contains a typo,
            it should be 'attendance_output'.
        """
        self.log = Logger.get_logger()
        self.base_dir = Path(__file__).parent.parent / 'data'
        self.base_dir = self.base_dir / 'attandance_output'
        self.ensure_directory()
        self.filename = self.base_dir / filename

    def ensure_directory(self) -> None:
        """
        Ensures that the base directory exists, creating it if it doesn't.
        """
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def read_existing_records(self) -> Dict:
        """
        Reads existing records from the file.
        
        Returns:
            Dict: Dictionary with attendance records. If the file doesn't exist
                 or contains invalid JSON, returns an empty dictionary.
        """
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_records(self, records: Dict) -> None:
        """
        Saves attendance records to the file.
        
        Args:
            records (Dict): Dictionary with attendance records to save.
        
        Raises:
            Exception: If an error occurs during the saving of the records.
                      The error is logged before raising the exception.
        """
        try:
            self.ensure_directory()
            
            self.log.debug(f"Preparing to save records...")
            self.log.debug(f"Records structure: {type(records)}")
            self.log.debug(f"Number of users in records: {len(records)}")
            if records:
                sample_user = next(iter(records))
                self.log.debug(f"Sample user records: {len(records[sample_user])}")
            
            with open(self.filename, "w") as file:
                json.dump(records, file, indent=4)
            self.log.debug(f"Records saved successfully to: {self.filename}")
            
        except Exception as e:
            self.log.error(f"Error saving records: {e}")
            self.log.error(traceback.format_exc())
            raise