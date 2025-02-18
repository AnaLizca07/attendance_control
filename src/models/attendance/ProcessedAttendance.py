from dataclasses import dataclass
from datetime import date as date_type
from typing import List, Dict
from models.attendance.enums.AttendanceStatus import AttendanceStatus
from models.device.DeviceInfo import DeviceInfo

@dataclass
class ProcessedAttendance:
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
        return {
            "user_id": str(user_id),
            "user_name": str(name),
            "records": records,
            "total_hours": f"{total_hours:.2f}",
            "status": status.value
        }