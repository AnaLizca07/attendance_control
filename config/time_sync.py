import ntplib
from datetime import datetime
import pytz

def getting_date_time():
    client = ntplib.NTPClient()
    try:
        response = client.request('time.google.com', version=3, timeout=10)
        utc_time = datetime.utcfromtimestamp(response.tx_time)  

        colombia_tz = pytz.timezone('America/Bogota')
        colombia_time = pytz.utc.localize(utc_time).astimezone(colombia_tz)

        ntp_date = colombia_time.strftime("%Y-%m-%d")
        ntp_time = colombia_time.strftime("%H:%M")

        return ntp_date, ntp_time
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None

# Ejemplo de uso
date, time = getting_date_time()
print(f"Date: {date}, Time: {time} ")
