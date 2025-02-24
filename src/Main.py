from services.AttendanceService import AttendanceService
from config.Logging import Logger
import signal
import sys

log = Logger.get_logger()
def signal_handler(signum, frame):
    """
    Handles termination signals to ensure clean shutdown.
    
    This function is registered as a handler for SIGINT and SIGTERM signals,
    allowing the application to perform cleanup operations before exiting.
    
    Args:
        signum: Signal number received.
        frame: Current stack frame.
    """
    log.error("Received signal to terminate. Cleaning up...")
    sys.exit(0)


def main():
    """
    Main function that initializes and runs the attendance service.
    
    This function:
    1. Sets up signal handlers for graceful termination
    2. Initializes the attendance service
    3. Runs the service's main loop
    4. Handles exceptions and provides appropriate exit codes
    
    Returns:
        int: Exit code (0 for normal exit, 1 for error).
    """
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
    main()