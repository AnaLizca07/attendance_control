from collections import defaultdict
from datetime import datetime, time
from typing import List, Dict, DefaultDict
from config.time_sync import TimeSync
from models.attendance.ProcessedAttendance import ProcessedAttendance
from models.attendance.AttendanceTimeCalculator import AttendanceTimeCalculator
from models.attendance.enums.AttendanceStatus import AttendanceStatus
from models.attendance.enums.AttendanceType import AttendanceType
from models.attendance.AttendanceRecord import AttendanceRecord

class AttendanceProcessor:
    def __init__(self, connector):
        self.connector = connector

    def get_daily_attendance(self) -> List:
        try:
            conn = self.connector.connect()
            if not conn:
                raise ConnectionError("Connection failed")
            
            attendance = conn.get_attendance()
            date_range = self._get_current_date_range()
            return self._filter_attendance(attendance, date_range)
            
        except Exception as e:
            print(f"Error getting attendance: {e}")
            return []
        finally:
            if self.connector:
                self.connector.disconnect()

    def process_user_attendance(self, users_info: Dict, attendance_list: List) -> Dict:
        try:
            attendance_by_user = self.organize_by_user(attendance_list)
            
            processed_data = {}
            for user_id, dates in attendance_by_user.items():
                if user_id in users_info:
                    user_records = self._process_single_user(
                        dates, 
                        str(user_id), 
                        users_info[user_id]
                    )
                    if user_records:
                        processed_data[user_id] = user_records
                        
            return processed_data
            
        except Exception as e:
            print(f"Error processing user attendance: {e}")
            return {}

    def _process_single_user(self, dates: Dict, user_id: str, 
                           user_info: Dict) -> List[Dict]:
        processed_records = []
        
        for date, times in sorted(dates.items()):
            times.sort()
            attendance_records = self._create_attendance_records(times)
            total_hours = AttendanceTimeCalculator.calculate_total_hours(times)
            status = AttendanceStatus.COMPLETE if len(times) >= 2 else AttendanceStatus.INCOMPLETE
            
            processed_record = ProcessedAttendance.create(
                user_info=user_info,
                user_id=user_id,
                attendance_date=date,
                records=attendance_records,
                total_hours=total_hours,
                status=status
            )
            
            processed_records.append(processed_record.__dict__)
            
        return processed_records

    def organize_by_user(self, attendance_list: List) -> DefaultDict:
        attendance_by_user = defaultdict(lambda: defaultdict(list))
        
        for attendance in attendance_list:
            self._add_attendance_record(attendance_by_user, attendance)
            
        return attendance_by_user

    def _get_current_date_range(self) -> tuple:
        time_sync = TimeSync()
        ntp_date, _ = time_sync.get_date_time()
        current_date = datetime.strptime(ntp_date, "%Y-%m-%d")
        return (
            datetime.combine(current_date, time.min),
            datetime.combine(current_date, time.max)
        )

    @staticmethod
    def _filter_attendance(attendance: List, date_range: tuple) -> List:
        start_datetime, end_datetime = date_range
        return [
            att for att in attendance 
            if start_datetime <= att.timestamp <= end_datetime
        ]

    @staticmethod
    def _add_attendance_record(attendance_dict: DefaultDict, 
                             attendance_record) -> None:
        user_id = attendance_record.user_id
        date = attendance_record.timestamp.date()
        attendance_dict[user_id][date].append(attendance_record.timestamp)

    @staticmethod
    def _create_attendance_records(times: List[datetime]) -> List[Dict]:
        records = []
        for i, timestamp in enumerate(times):
            attendance_type = AttendanceProcessor._determine_attendance_type(i, len(times))
            record = AttendanceRecord(
                hour=timestamp.strftime("%H:%M:%S"),
                type=attendance_type
            )
            records.append(record.__dict__)
        return records

    @staticmethod
    def _determine_attendance_type(index: int, total_records: int) -> AttendanceType:
        if index == 0:
            return AttendanceType.CHECKIN
        if index == total_records - 1:
            return AttendanceType.CHECKOUT
        return AttendanceType.INTERMEDIATE