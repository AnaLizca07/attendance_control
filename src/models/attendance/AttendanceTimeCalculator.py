from datetime import datetime
from typing import List

class AttendanceTimeCalculator:
    """
    Utility class that provides methods for calculating attendance times.
    
    This class contains static methods to perform time-based calculations
    on attendance data, such as determining total hours worked.
    """
    
    @staticmethod
    def calculate_total_hours(times: List[datetime]) -> float:
        """
        Calculates the total hours between the first and last datetime in a list.
        
        This method computes the time duration from the first recorded time
        to the last recorded time in the provided list, converting the result
        to hours.
        
        Args:
            times (List[datetime]): A list of datetime objects representing
                                   clock-in and clock-out times.
            
        Returns:
            float: Total hours between first and last time. Returns 0.0 if
                  the list contains fewer than 2 datetime objects.
        """
        if len(times) < 2:
            return 0.0
        total_seconds = (times[-1] - times[0]).total_seconds()
        return total_seconds / 3600