# main.py
from datetime import datetime
from utils.zk_connector import ZKConnector
from controllers.attendance_controller import AttendanceController
from controllers.device_controller import DeviceController

def main():
    # Crear instancia del conector
    connector = ZKConnector()

    deviceController = DeviceController(connector)
    deviceController.get_device_info()
    
    # Crear instancia del controlador
    #controller = AttendanceController(connector)
    
    # Definir la fecha específica
    #specific_date = datetime.now()  # Por ejemplo, para el 11 de febrero de 2025
    
    # Procesar asistencias
    #controller.process_attendance(specific_date)

if __name__ == "__main__":
    main()