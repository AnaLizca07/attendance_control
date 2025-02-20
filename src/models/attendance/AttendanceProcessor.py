from collections import defaultdict
from datetime import datetime, time
from typing import List, Dict, DefaultDict
from config.time_sync import TimeSync
from models.attendance.ProcessedAttendance import ProcessedAttendance
from models.attendance.AttendanceTimeCalculator import AttendanceTimeCalculator
from models.attendance.enums.AttendanceStatus import AttendanceStatus
from models.attendance.enums.AttendanceType import AttendanceType
from models.attendance.AttendanceRecord import AttendanceRecord
from models.device.Device import Device
from typing import Optional
from models.device.DeviceInfo import DeviceInfo

class AttendanceProcessor:
    def __init__(self, connector, device: Device, device_info: Optional[DeviceInfo]=None):
        self.connector = connector
        self.device = device
        self.device_info = device_info

    def get_daily_attendance(self) -> List:
        try:
            conn = self.connector.connect()
            if not conn:
                raise ConnectionError("Connection failed")
            
            if not self.device_info:
                print("Getting device info...")
                self.device_info = self.device.get_device_info(conn)
                if not self.device_info:
                    raise ValueError("Could not get device info")
            
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
            print(f"\nProcessing attendance for {len(attendance_list)} records")
            attendance_by_user = self.organize_by_user(attendance_list)
            print(f"Organized into {len(attendance_by_user)} users")

            if not self.device_info:
                raise ValueError("device_info is not available")
            
            processed_data = {
                "id": str(int(datetime.now().timestamp())),
                "serial_number": self.device_info.description.serial_number,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "users": {}
            }
            
            for user_id, dates in attendance_by_user.items():
                print(f"\nProcessing user_id: {user_id}")
                if user_id in users_info:
                    print(f"User found in users_info")
                    user_records = self._process_single_user(
                        dates=dates,
                        user_id=str(user_id),
                        user_info=users_info[user_id]
                    )
                    if user_records and isinstance(user_records, dict) and user_records.get('records'):
                        processed_data["users"][user_id] = user_records
                        print(f"Added records for user {user_id}")
                    else:
                        print(f"No valid records found for user {user_id}")
                else:
                    print(f"User {user_id} not found in users_info")
            
            print(f"Final processed data contains {len(processed_data['users'])} users")
            return processed_data
            
        except Exception as e:
            print(f"Error processing user attendance: {e}")
            import traceback
            print(traceback.format_exc())
            return {}
        

    def _process_single_user(self, dates: Dict, user_id: str, user_info: Dict) -> List[Dict]:
        try:
            print(f"\nProcessing user {user_id} with {len(dates)} dates")
            name = user_info.get('name', '') 

            if not dates:
                return {}

            try:
                # Procesar solo el primer día (ya que es asistencia diaria)
                date, times = next(iter(sorted(dates.items())))
                times.sort()
                
                attendance_records = self._create_attendance_records(times)
                total_hours = AttendanceTimeCalculator.calculate_total_hours(times)
                status = AttendanceStatus.COMPLETE if len(times) >= 2 else AttendanceStatus.INCOMPLETE
                
                processed_record = {
                    "user_id": str(user_id),
                    "user_name": name,
                    "records": attendance_records,
                    "total_hours": f"{total_hours:.2f}",
                    "status": status.value
                }
                print(f"Successfully processed record for date {date}")
                return processed_record
                
            except StopIteration:
                print(f"No dates found for user {user_id}")
                return {}
            
            except Exception as e:
                print(f"Error processing record: {e}")
                return {}
            
        except Exception as e:
            print(f"Error processing user {user_id}: {e}")
            return {}

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