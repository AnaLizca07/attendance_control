import ntplib
from datetime import datetime
import pytz
from typing import Tuple, Optional
import os

class TimeSync:
    def __init__(self):
        DEFAULT_NTP_SERVER = "pool.ntp.org"
        DEFAULT_TIMEZONE = "America/Bogota"
        DEFAULT_NTP_VERSION = 3
        DEFAULT_TIMEOUT = 5

        self.ntp_server = os.getenv('NTP_SERVER', DEFAULT_NTP_SERVER)
        self.timezone = os.getenv('TIMEZONE', DEFAULT_TIMEZONE)
        
        try:
            self.ntp_version = int(os.getenv('NTP_VERSION', DEFAULT_NTP_VERSION))
        except (TypeError, ValueError):
            self.ntp_version = DEFAULT_NTP_VERSION
            
        try:
            self.timeout = int(os.getenv('NTP_TIMEOUT', DEFAULT_TIMEOUT))
        except (TypeError, ValueError):
            self.timeout = DEFAULT_TIMEOUT

    def get_date_time(self) -> Tuple[Optional[str], Optional[str]]:

        try:
            local_time = self._get_localized_time()
        except Exception as e:
            print(f"Error getting date/time: {str(e)}")
            local_time = self._get_local_time()
            
        return self._format_date_time(local_time)

    def _get_localized_time(self) -> datetime:
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
        local_tz = pytz.timezone(self.timezone)
        return datetime.now(local_tz)

    def _format_date_time(self, local_time: datetime) -> Tuple[str, str]:
        return (
            local_time.strftime("%Y-%m-%d"),
            local_time.strftime("%H:%M")
        )
    
# Example usage
time_sync = TimeSync()
date, time = time_sync.get_date_time()
print(f"Date: {date}, Time: {time}")