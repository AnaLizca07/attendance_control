from services.AttendanceService import AttendanceService
from config.Logging import Logger
import signal
import sys

log = Logger.get_logger()
def signal_handler(signum, frame):
    log.error("Received signal to terminate. Cleaning up...")
    sys.exit(0)


def main():
    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        log.info("Starting Attendance Service...")

        service = AttendanceService()
        service.run()

    except KeyboardInterrupt:
        log.warning("\nService stopped by user")
        return 0
    except Exception as e:
        log.error(f"Fatal error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())