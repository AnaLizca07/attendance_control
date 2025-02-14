# main.py
import time
import threading
from datetime import datetime
from utils.zk_connector import ZKConnector
from config.time_sync import getting_date_time
from controllers.attendance_controller import AttendanceController
from dotenv import load_dotenv
import os

load_dotenv()
#EXECUTION_TIME = os.getenv('EXECUTION_TIME')

def main():

    print("Initiating data collection...")
    # Crear instancia del conector

    connector = ZKConnector()
    
    # Crear instancia del controlador
    controller = AttendanceController(connector)

    # Procesar asistencias
    controller.process_attendance()


while True:
    
    ntp_date, ntp_time = getting_date_time()

    if ntp_time == os.getenv('EXECUTION_TIME'):
        main()