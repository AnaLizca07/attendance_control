# config/settings.py

# Configuración del dispositivo ZK
ZK_DEVICE = {
    'ip': '192.168.0.3',
    'port': 4370,
    'password': 2121,
    'timeout': 10
}

# Rutas del sistema
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Crear directorio de output si no existe
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_json_filename(date):
    """Genera un nombre de archivo basado en la fecha"""
    date_str = date.strftime('%Y%m%d')
    timestamp = datetime.now().strftime('%H%M%S')
    return os.path.join(OUTPUT_DIR, f'attendance_{date_str}_{timestamp}.json')