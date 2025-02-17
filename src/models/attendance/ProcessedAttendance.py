from dataclasses import dataclass
from datetime import date as date_type
from typing import List, Dict
from models.attendance.enums.AttendanceStatus import AttendanceStatus
from models.device.DeviceInfo import DeviceInfo

@dataclass
class ProcessedAttendance:
    device_id: str
    user_id: str
    date: str
    records: List[Dict]
    total_hours: str
    status: AttendanceStatus

    @classmethod
    def create(cls, user_id: str, 
               attendance_date: date_type, 
               records: List[Dict], 
               total_hours: float, 
               status: AttendanceStatus,
               device_info: DeviceInfo) -> 'ProcessedAttendance':
        
        if not device_info:
            raise ValueError("device_info cannot be None")
            
        return cls(
            device_id=device_info.device_id,
            user_id=str(user_id),
            date=attendance_date.strftime("%Y-%m-%d"),
            records=records,
            total_hours=f"{total_hours:.2f}",
            status=status
        )