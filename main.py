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

EXECUTION_TIME = "17:28"

def main():

    print("Iniciando recolección de datos...")
    # Crear instancia del conector

    ntp_date, ntp_time = getting_date_time()

    connector = ZKConnector()

    deviceController = DeviceController(connector)
    deviceController.get_device_info()
    
    # Crear instancia del controlador
    controller = AttendanceController(connector)

    # Definir la fecha específica
    specific_date = datetime.strptime(ntp_date, "%Y-%m-%d")  # Por ejemplo, para el 11 de febrero de 2025

    # Procesar asistencias
    controller.process_attendance(specific_date)

schedule.every().day.at(EXECUTION_TIME).do(main)

while True:    
    ntp_date , ntp_time = getting_date_time()

    if ntp_time:

        if ntp_time == EXECUTION_TIME:
            schedule.run_pending()  

