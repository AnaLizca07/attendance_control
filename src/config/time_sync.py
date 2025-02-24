import ntplib
from datetime import datetime
import pytz
from typing import Tuple, Optional
import os
from config.Logging import Logger

class TimeSync:
    """
    Class that provides synchronized time using NTP servers with fallback options.
    
    This utility handles time synchronization with an NTP server and provides
    formatted date and time strings in the configured timezone. If NTP synchronization
    fails, it falls back to the local system time.
    
    Attributes:
        logger: Logger instance for event logging.
        ntp_server (str): NTP server address from environment variables.
        timezone (str): Timezone name from environment variables.
        ntp_version (int): NTP protocol version from environment variables.
        timeout (int): NTP request timeout in seconds from environment variables.
    """
    def __init__(self):
        """
        Initializes the TimeSync utility with configuration from environment variables.
        
        Loads synchronization parameters from environment variables:
        - NTP_SERVER: Address of the NTP server
        - TIMEZONE: Timezone to use for localization
        - NTP_VERSION: NTP protocol version
        - NTP_TIMEOUT: Timeout for NTP requests in seconds
        """
        self.logger = Logger().get_logger()
        self.ntp_server = os.getenv('NTP_SERVER')
        self.timezone = os.getenv('TIMEZONE')
        self.ntp_version = int(os.getenv('NTP_VERSION'))
        self.timeout = int(os.getenv('NTP_TIMEOUT'))


    def get_date_time(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Gets the current date and time with NTP synchronization when possible.
        
        This method attempts to get time from an NTP server first. If that fails,
        it falls back to using the local system time.
        
        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing (date_string, time_string),
                                               where date is in "YYYY-MM-DD" format and
                                               time is in "HH:MM" format.
        """
        try:
            local_time = self._get_localized_time()
        except Exception as e:
            self.logger.error(f"Error getting date/time: {str(e)}")
            local_time = self._get_local_time()
            
        return self._format_date_time(local_time)

    def _get_localized_time(self) -> datetime:
        """
        Retrieves time from an NTP server and converts it to the configured timezone.
        
        Returns:
            datetime: NTP synchronized time in the configured timezone.
            
        Raises:
            Exception: If NTP synchronization fails.
        """
        client = ntplib.NTPClient()
        response = client.request(
            self.ntp_server, 
            version=self.ntp_version, 
            timeout=self.timeout
        )
        
        utc_time = datetime.utcfromtimestamp(response.tx_time)
        local_tz = pytz.timezone(self.timezone)
        
        return pytz.utc.localize(utc_time).astimezone(local_tz)
    
    def _get_local_time(self) -> datetime:
        """
        Gets the current local system time as a fallback.
        
        Returns:
            datetime: Current local system time in the configured timezone.
        """
        local_tz = pytz.timezone(self.timezone)
        return datetime.now(local_tz)

    def _format_date_time(self, local_time: datetime) -> Tuple[str, str]:
        """
        Formats a datetime object into standardized date and time strings.
        
        Args:
            local_time (datetime): The datetime object to format.
            
        Returns:
            Tuple[str, str]: A tuple containing (date_string, time_string),
                           where date is in "YYYY-MM-DD" format and
                           time is in "HH:MM" format.
        """
        return (
            local_time.strftime("%Y-%m-%d"),
            local_time.strftime("%H:%M")
        )