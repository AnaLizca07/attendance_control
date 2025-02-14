from datetime import datetime
from typing import List

class AttendanceTimeCalculator:
    @staticmethod
    def calculate_total_hours(times: List[datetime]) -> float:
        if len(times) < 2:
            return 0.0
        total_seconds = (times[-1] - times[0]).total_seconds()
        return total_seconds / 3600