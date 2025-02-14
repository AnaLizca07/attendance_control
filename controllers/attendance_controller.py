import json
from models.user import User
from models.attendance import Attendance
from config.settings import get_json_filename
from controllers.device_controller import DeviceController
from views.to_JSON import ToJSON
from datetime import datetime

class AttendanceController:
    
    def __init__(self, connector):
        self.connector = connector
        self.device_controller = DeviceController(connector)
        self.view = ToJSON()
        self.device_info_saved = False

    def process_attendance(self):

        if not self.device_info_saved:
            self.device_controller.get_device_info()
            self.device_info_saved = True
            
        try:
            conn = self.connector.connect()
            if not conn:
                return
            
            print(f'--- Attendances per day ---')
            
            users_info = User.get_users_info(conn)
            
            filtered_attendance = Attendance.get_filtered_attendance(conn)
            attendance_by_user = Attendance.organize_attendance_by_user(filtered_attendance)
            
            json_filename = get_json_filename(datetime.now().date())

            try:
                with open(json_filename, "r") as file:
                    json_output = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                json_output = {}
            
            for user_id, dates in attendance_by_user.items():
                user_info = users_info.get(user_id, {})
                str_user_id = str(user_id)

                processed_records = Attendance.process_attendance_records(dates, user_id, user_info)

                if str_user_id in json_output:
                    existing_records = json_output[str_user_id]

                    existing_set = {json.dumps(record, sort_keys=True) for record in existing_records}

                    unique_records = [record for record in processed_records if json.dumps(record, sort_keys=True) not in existing_set]

                    if unique_records:
                        json_output[str_user_id].extend(unique_records)
                else: 
                    json_output[str_user_id] = processed_records
            
            with open(json_filename, "w") as file:
                json.dump(json_output, file, indent=4)
            
            self.view.save_json_output(json_output, json_filename)
            print(f"\nTotal records: {len(filtered_attendance)}")
            
            return filtered_attendance
            
        except Exception as e:
            print("Error processing: {}".format(e))
            return []
        finally:
            self.connector.disconnect()