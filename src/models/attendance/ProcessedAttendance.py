from dataclasses import dataclass
from datetime import date as date_type
from typing import List, Dict
from models.attendance.enums.AttendanceStatus import AttendanceStatus

@dataclass
class ProcessedAttendance:
    user_name: str
    user_id: str
    date: str
    records: List[Dict]
    total_hours: str
    status: AttendanceStatus

    @classmethod
    def create(cls, user_info: Dict, user_id: str, 
               attendance_date: date_type, 
               records: List[Dict], 
               total_hours: float, 
               status: AttendanceStatus) -> 'ProcessedAttendance':
        return cls(
            user_name=user_info.get('name', 'Unknown'),
            user_id=str(user_id),
            date=attendance_date.strftime("%Y-%m-%d"),
            records=records,
            total_hours=f"{total_hours:.2f}",
            status=status
        )