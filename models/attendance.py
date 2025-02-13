from collections import defaultdict
from datetime import datetime, time

class Attendance:

    @staticmethod
    def get_filtered_attendance(conn):
        attendance = conn.get_attendance()
        current_date = datetime.now().date()
        start_datetime = datetime.combine(current_date, time.min)
        end_datetime = datetime.combine(current_date, time.max)
        
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
            
            records = []
            for i, timestamp in enumerate(times):
                type = 1 if i == 0 else 0 if i == len(times)-1 else 2
                records.append({
                    "hour": timestamp.strftime("%H:%M:%S"),
                    "type": type
                })
            
            total_hours = "0.00"
            status = 0
            if len(times) >= 2:
                total_seconds = (times[-1] - times[0]).total_seconds()
                total_hours = f"{total_seconds / 3600:.2f}"
                status = 1
            
            processed_records.append({
                "User": user_info.get('name', 'Unknown'),
                "User ID": str(user_id),
                "Date": date.strftime("%Y-%m-%d"),
                "Records": records,
                "Total hours": total_hours,
                "Status": status
            })
            
        return processed_records