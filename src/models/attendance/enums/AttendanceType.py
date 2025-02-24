from enum import IntEnum

class AttendanceType(IntEnum):
    """
    Enumeration representing the type of an attendance record.
    
    This enum defines the possible types of attendance events that can be
    recorded in the system, using integer values for compatibility with
    external systems or databases.
    
    Attributes:
        CHECKOUT (0): Represents a checkout/exit event.
        CHECKIN (1): Represents a checkin/entry event.
        INTERMEDIATE (2): Represents an intermediate record between
                         checkin and checkout (e.g., break start/end).
    """
    CHECKOUT = 0
    CHECKIN = 1
    INTERMEDIATE = 2
