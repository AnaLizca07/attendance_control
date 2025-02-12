# models/attendance.py
from collections import defaultdict
from datetime import datetime, time

class Attendance:
    @staticmethod
    def get_filtered_attendance(conn, specific_date):
        attendance = conn.get_attendance()
        # Crear datetime para inicio y fin del día específico
        start_datetime = datetime.combine(specific_date.date(), time.min)
        end_datetime = datetime.combine(specific_date.date(), time.max)
        
        return [
            att for att in attendance 
            if start_datetime <= att.timestamp <= end_datetime
        ]

    @staticmethod
    def organize_attendance_by_user(filtered_attendance):
        attendance_by_user = defaultdict(lambda: defaultdict(list))
        
        for att in filtered_attendance:
            user_id = att.user_id
            date = att.timestamp.date()
            attendance_by_user[user_id][date].append(att.timestamp)
            
        return attendance_by_user

    @staticmethod
    def process_attendance_records(dates, user_id, user_info):
        processed_records = []
        
        for date, times in sorted(dates.items()):
            times.sort()
            
            # Crear lista de todos los registros del día
            registros = []
            for i, timestamp in enumerate(times):
                tipo = "Entrada" if i == 0 else "Salida" if i == len(times)-1 else f"Receso {i+1}"
                registros.append({
                    "hora": timestamp.strftime("%H:%M:%S"),
                    "tipo": tipo
                })
            
            # Calcular total de horas si hay al menos entrada y salida
            total_horas = "0.00"
            estado = "Incompleto"
            if len(times) >= 2:
                total_seconds = (times[-1] - times[0]).total_seconds()
                total_horas = f"{total_seconds / 3600:.2f}"
                estado = "Completo"
            
            processed_records.append({
                "Usuario": user_info.get('name', 'No registrado'),
                "Id usuario": str(user_id),
                "Fecha": date.strftime("%Y-%m-%d"),
                "Registros": registros,
                "Total horas": total_horas,
                "Estado": estado
            })
            
        return processed_records