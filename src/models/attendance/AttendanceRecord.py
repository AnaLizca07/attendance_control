from dataclasses import dataclass
from models.attendance.enums.AttendanceType import AttendanceType

@dataclass
class AttendanceRecord:
    hour: str
    type: AttendanceType