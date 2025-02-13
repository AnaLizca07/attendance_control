import os
import json
from models.user import User
from models.attendance import Attendance
from views.console_views import ConsoleView
from config.settings import get_json_filename
from controllers.device_controller import DeviceController

class AttendanceController:
    
    def __init__(self, connector):
        self.connector = connector
        self.view = ConsoleView()
        self.device_controller = DeviceController(connector)
        self.device_info_displayed = False

    def process_attendance(self, specific_date):

        if not self.device_info_displayed:
            self.device_controller.get_device_info()
            self.device_info_displayed = True
            
        try:
            conn = self.connector.connect()
            if not conn:
                return
            
            print(f'--- Asistencias por Usuario para el día {specific_date.date()} ---')
            
            # Obtener información de usuarios
            users_info = User.get_users_info(conn)
            
            # Obtener y filtrar asistencias
            filtered_attendance = Attendance.get_filtered_attendance(conn, specific_date)
            attendance_by_user = Attendance.organize_attendance_by_user(filtered_attendance)
            
            # Procesar y mostrar resultados
            json_filename = get_json_filename(specific_date)

            try:
                with open(json_filename, "r") as file:
                    json_output = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                json_output = {}
            
            for user_id, dates in attendance_by_user.items():
                user_info = users_info.get(user_id, {})
                str_user_id = str(user_id)

                # Procesar registros incluyendo información del usuario
                processed_records = Attendance.process_attendance_records(dates, user_id, user_info)

                if str_user_id in json_output:
                    existing_records = json_output[str_user_id]

                    existing_set = {json.dumps(record, sort_keys=True) for record in existing_records}

                    unique_records = [record for record in processed_records if json.dumps(record, sort_keys=True) not in existing_set]

                    if unique_records:
                        json_output[str_user_id].extend(unique_records)
                else: 
                    json_output[str_user_id] = processed_records
                
                # Mostrar en consola
                self.view.display_user_info(user_id, user_info)
                for date, times in sorted(dates.items()):
                    self.view.display_attendance(date, times)
            
            with open(json_filename, "w") as file:
                json.dump(json_output, file, indent=4)
            
            print(f"\nTotal registros encontrados: {len(filtered_attendance)}")
            
            return filtered_attendance
            
        except Exception as e:
            print("Error procesando asistencias: {}".format(e))
            return []
        finally:
            self.connector.disconnect()