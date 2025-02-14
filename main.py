# main.py
import time
import schedule
import threading
# import multiprocessing
from datetime import datetime
from utils.zk_connector import ZKConnector
from config.time_sync import getting_date_time
from controllers.attendance_controller import AttendanceController
from controllers.device_controller import DeviceController

EXECUTION_TIME = "07:38"

def main():

    print("Iniciando recolección de datos...")
    # Crear instancia del conector

    connector = ZKConnector()
    
    # Crear instancia del controlador
    controller = AttendanceController(connector)

    # Procesar asistencias
    controller.process_attendance()

schedule.every().day.at(EXECUTION_TIME).do(main)

while True:    
    ntp_date , ntp_time = getting_date_time()
    if ntp_date and ntp_time:
        print(f"Date: {ntp_date}, Time: {ntp_time}")
    else:
        print("The time could not be synchronized.")

    if ntp_time:

        if ntp_time == EXECUTION_TIME:
            schedule.run_pending()  

