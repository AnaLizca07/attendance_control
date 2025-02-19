from services.AttendanceService import AttendanceService
import signal
import sys

def signal_handler(signum, frame):
    print("\nReceived signal to terminate. Cleaning up...")
    sys.exit(0)


def main():
    try:
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        print("Starting Attendance Service...")

        service = AttendanceService()
        service.run()

    except KeyboardInterrupt:
        print("\nService stopped by user")
        return 0
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())