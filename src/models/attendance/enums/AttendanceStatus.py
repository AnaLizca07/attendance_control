from enum import IntEnum

class AttendanceStatus(IntEnum):
    """
    Enumeration representing the status of a user's attendance for a day.
    
    This enum defines the possible statuses that can be assigned to a user's
    daily attendance record, using integer values for compatibility with
    external systems or databases.
    
    Attributes:
        INCOMPLETE (0): Represents an incomplete attendance record, typically
                        when only check-in or check-out is recorded but not both.
        COMPLETE (1): Represents a complete attendance record with both check-in
                     and check-out records present.
    """
    INCOMPLETE = 0
    COMPLETE = 1