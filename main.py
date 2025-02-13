# main.py
import time
import schedule
import threading
# import multiprocessing
from datetime import datetime
from utils.zk_connector import ZKConnector
from controllers.attendance_controller import AttendanceController
from controllers.device_controller import DeviceController


def main():

    print("Iniciando recolección de datos...")
    # Crear instancia del conector
    connector = ZKConnector()

    deviceController = DeviceController(connector)
    deviceController.get_device_info()
    
    # Crear instancia del controlador
    controller = AttendanceController(connector)

    # Definir la fecha específica
    specific_date = datetime.now()  # Por ejemplo, para el 11 de febrero de 2025

    # Procesar asistencias
    controller.process_attendance(specific_date)

schedule.every().day.at("07:00").do(main)

while True:       
    schedule.run_pending()
