from services.AttendanceService import AttendanceService
from database.attendance_retry import SQLiteDB

def main():

    
    try:
        service = AttendanceService()
        service.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())