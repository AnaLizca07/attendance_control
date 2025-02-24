import traceback
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
from config.Logging import Logger


class AttendanceProcessor:
    """
    Class responsible for processing attendance data from a device.
    
    This class handles fetching, organizing, and processing attendance records
    from connected devices, calculating work hours, and determining attendance status.
    """
    
    def __init__(self, connector, device: Device, device_info: Optional[DeviceInfo]=None):
        """
        Initialize an AttendanceProcessor with connector, device, and optional device info.
        
        Args:
            connector: The connector object used to communicate with the data source.
            device (Device): Device object used to retrieve device information.
            device_info (Optional[DeviceInfo]): Optional pre-loaded device information.
        """
        self.connector = connector
        self.device = device
        self.device_info = device_info
        self.log = Logger.get_logger()

    def get_daily_attendance(self) -> List:
        """
        Retrieves attendance records for the current day from the connected device.
        
        Returns:
            List: List of attendance records for the current day.
            Returns an empty list if an error occurs.
            
        Raises:
            ConnectionError: If connection to the device fails.
            ValueError: If device_info cannot be retrieved.
        """
        try:
            conn = self.connector.connect()
            if not conn:
                raise ConnectionError("Connection failed")
            
            if not self.device_info:
                self.logger.debug("Getting device info...")
                self.device_info = self.device.get_device_info(conn)
                if not self.device_info:
                    raise ValueError("Could not get device info")
            
            attendance = conn.get_attendance()
            date_range = self._get_current_date_range()
            return self._filter_attendance(attendance, date_range)
            
        except Exception as e:
            self.log.error(f"Error getting attendance: {e}")
            return []
        finally:
            if self.connector:
                self.connector.disconnect()

    def process_user_attendance(self, users_info: Dict, attendance_list: List) -> Dict:
        """
        Processes attendance data for all users and organizes it into a structured format.
        
        Args:
            users_info (Dict): Dictionary mapping user IDs to user information.
            attendance_list (List): List of attendance records to process.
            
        Returns:
            Dict: A dictionary containing processed attendance data with the structure:
                {
                    "id": "timestamp",
                    "serial_number": "device_serial_number",
                    "date": "YYYY-MM-DD",
                    "users": {
                        "user_id": {
                            "user_id": "user_id",
                            "user_name": "name",
                            "records": [list of attendance records],
                            "total_hours": "hours in decimal format",
                            "status": "attendance status"
                        },
                        ...
                    }
                }
            Returns an empty dictionary if an error occurs.
            
        Raises:
            ValueError: If device_info is not available.
        """
        try:
            self.log.debug(f"\nProcessing attendance for {len(attendance_list)} records")
            attendance_by_user = self.organize_by_user(attendance_list)
            self.log.debug(f"Organized into {len(attendance_by_user)} users")

            if not self.device_info:
                raise ValueError("device_info is not available")
            
            processed_data = {
                "id": str(int(datetime.now().timestamp())),
                "serial_number": self.device_info.description.serial_number,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "users": {}
            }
            
            for user_id, dates in attendance_by_user.items():
                self.log.debug(f"\nProcessing user_id: {user_id}")
                if user_id in users_info:
                    self.log.debug(f"User found in users_info")
                    user_records = self._process_single_user(
                        dates=dates,
                        user_id=str(user_id),
                        user_info=users_info[user_id]
                    )
                    if user_records and isinstance(user_records, dict) and user_records.get('records'):
                        processed_data["users"][user_id] = user_records
                        self.log.debug(f"Added records for user {user_id}")
                    else:
                        self.log.error(f"No valid records found for user {user_id}")
                else:
                    self.log.error(f"User {user_id} not found in users_info")
            
            self.log.debug(f"Final processed data contains {len(processed_data['users'])} users")
            return processed_data
            
        except Exception as e:
            self.log.debug(f"Error processing user attendance: {e}")
            self.log.debug(traceback.format_exc())
            return {}
        
    def _process_single_user(self, dates: Dict, user_id: str, user_info: Dict) -> Dict:
        """
        Processes attendance data for a single user.
        
        Args:
            dates (Dict): Dictionary mapping dates to lists of attendance timestamps.
            user_id (str): ID of the user being processed.
            user_info (Dict): Dictionary containing user information.
            
        Returns:
            Dict: A dictionary containing processed attendance data for the user.
            Returns an empty dictionary if an error occurs.
        """
        try:
            self.log.debug(f"\nProcessing user {user_id} with {len(dates)} dates")
            name = user_info.get('name', '') 

            if not dates:
                return {}

            try:
                # Process only the first day (since it's daily attendance)
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
                self.log.debug(f"Successfully processed record for date {date}")
                return processed_record
                
            except StopIteration:
                self.log.error(f"No dates found for user {user_id}")
                return {}
            
            except Exception as e:
                self.log.error(f"Error processing record: {e}")
                return {}
            
        except Exception as e:
            self.log.error(f"Error processing user {user_id}: {e}")
            return {}

    def organize_by_user(self, attendance_list: List) -> DefaultDict:
        """
        Organizes attendance records by user and date.
        
        Args:
            attendance_list (List): List of attendance records to organize.
            
        Returns:
            DefaultDict: A nested defaultdict where the first level keys are user IDs,
                        the second level keys are dates, and the values are lists of
                        attendance timestamps.
        """
        attendance_by_user = defaultdict(lambda: defaultdict(list))
        
        for attendance in attendance_list:
            self._add_attendance_record(attendance_by_user, attendance)
            
        return attendance_by_user

    def _get_current_date_range(self) -> tuple:
        """
        Gets the date range for the current day using NTP synchronized time.
        
        Returns:
            tuple: A tuple containing (start_datetime, end_datetime) for the current day.
        """
        time_sync = TimeSync()
        ntp_date, _ = time_sync.get_date_time()
        current_date = datetime.strptime(ntp_date, "%Y-%m-%d")
        return (
            datetime.combine(current_date, time.min),
            datetime.combine(current_date, time.max)
        )

    @staticmethod
    def _filter_attendance(attendance: List, date_range: tuple) -> List:
        """
        Filters attendance records to include only those within the specified date range.
        
        Args:
            attendance (List): List of attendance records to filter.
            date_range (tuple): Tuple containing (start_datetime, end_datetime).
            
        Returns:
            List: Filtered list of attendance records.
        """
        start_datetime, end_datetime = date_range
        return [
            att for att in attendance 
            if start_datetime <= att.timestamp <= end_datetime
        ]

    @staticmethod
    def _add_attendance_record(attendance_dict: DefaultDict, 
                             attendance_record) -> None:
        """
        Adds an attendance record to the organized attendance dictionary.
        
        Args:
            attendance_dict (DefaultDict): The organized attendance dictionary.
            attendance_record: The attendance record to add.
        """
        user_id = attendance_record.user_id
        date = attendance_record.timestamp.date()
        attendance_dict[user_id][date].append(attendance_record.timestamp)

    @staticmethod
    def _create_attendance_records(times: List[datetime]) -> List[Dict]:
        """
        Creates a list of attendance records from a list of timestamps.
        
        Args:
            times (List[datetime]): List of attendance timestamps.
            
        Returns:
            List[Dict]: List of attendance record dictionaries.
        """
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
        """
        Determines the attendance type based on the index and total number of records.
        
        Args:
            index (int): Index of the current record.
            total_records (int): Total number of records.
            
        Returns:
            AttendanceType: The determined attendance type.
                           CHECKIN for the first record,
                           CHECKOUT for the last record,
                           INTERMEDIATE for all records in between.
        """
        if index == 0:
            return AttendanceType.CHECKIN
        if index == total_records - 1:
            return AttendanceType.CHECKOUT
        return AttendanceType.INTERMEDIATE