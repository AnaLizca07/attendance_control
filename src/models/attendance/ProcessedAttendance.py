from dataclasses import dataclass
from datetime import date as date_type
from typing import List, Dict
from models.attendance.enums.AttendanceStatus import AttendanceStatus
from models.device.DeviceInfo import DeviceInfo

@dataclass
class ProcessedAttendance:
    """
    Data class representing processed attendance information for a user.
    
    This class stores the final calculated attendance data including user details,
    attendance records, total hours worked, and overall attendance status.
    
    Attributes:
        user_id (str): The user's identifier.
        name (str): The user's name.
        records (List[Dict]): List of attendance record dictionaries.
        total_hours (str): Total hours worked, formatted as a string with two decimal places.
        status (AttendanceStatus): The overall attendance status (e.g., PRESENT, ABSENT, etc.).
    """
    user_id: str
    name: str
    records: List[Dict]
    total_hours: str
    status: AttendanceStatus

    @classmethod
    def create(cls, user_id: str, 
               name: str,
               records: List[Dict], 
               total_hours: float, 
               status: AttendanceStatus) -> Dict:
        """
        Creates a dictionary representation of processed attendance data.
        
        Note: This method doesn't return a ProcessedAttendance instance,
        but rather a dictionary representation directly.
        
        Args:
            user_id (str): The user's identifier.
            name (str): The user's name.
            records (List[Dict]): List of attendance record dictionaries.
            total_hours (float): Total hours worked as a float value.
            status (AttendanceStatus): The overall attendance status.
            
        Returns:
            Dict: Dictionary containing attendance information with keys:
                - user_id: String representation of the user ID
                - user_name: String representation of the user name
                - records: List of attendance record dictionaries
                - total_hours: Formatted string of hours worked with 2 decimal places
                - status: String value of the AttendanceStatus enum
        """
        return {
            "user_id": str(user_id),
            "user_name": str(name),
            "records": records,
            "total_hours": f"{total_hours:.2f}",
            "status": status.value
        }