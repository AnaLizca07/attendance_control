from dataclasses import dataclass
from models.attendance.enums.AttendanceType import AttendanceType

@dataclass
class AttendanceRecord:
    """
    Data class representing a single attendance record entry.
    
    This class stores information about a particular attendance event,
    including the time it occurred and its type (e.g., check-in or check-out).
    
    Attributes:
        hour (str): The time of the attendance event, stored as a string.
        type (AttendanceType): The type of the attendance event (e.g., IN, OUT).
    """
    hour: str
    type: AttendanceType