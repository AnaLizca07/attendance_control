import logging
import os

# Definir la ruta del archivo de logs
LOGS_DIR = os.path.join(os.path.dirname(__file__), '../logs')
LOG_FILE_PATH = os.path.join(LOGS_DIR, 'attendance.log')

# Crear carpeta logs si no existe
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,  # Cambia a DEBUG si necesitas más detalles
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode='a', encoding='utf-8'),
        logging.StreamHandler()  # También muestra logs en la consola
    ]
)

# Logger principal
logger = logging.getLogger(__name__)

logger.info("📋 Sistema de logs inicializado.")
