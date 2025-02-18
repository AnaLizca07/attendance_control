import logging
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os


class NetworkRetry:
    def __init__(self):
        load_dotenv()
        self.max_retries = os.getenv('MAX_RETRIES')  # Intentará durante 1 hora (12 intentos * 5 minutos)
        self.retry_delay = os.getenv('RETRY_DELAY')  # Intentará durante 1 hora (12 intentos * 5 minutos)
        self.backup_file = Path.home() / 'Documents' / 'output' / 'pending_execution.json'
        self.expired_file = Path.home() / 'Documents' / 'output' / 'expired_execution.json'

    def save_pending_execution(self, date: str) -> None:
        try:
            data = {
                'date': date,
                'timestamp': datetime.now().isoformat(),
                'retry_count': 0
            }
            
            self.backup_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.backup_file, 'w') as f:
                json.dump(data, f)
                
            logging.info(f"Guardada ejecución pendiente para fecha: {date}")
        except Exception as e:
            logging.error(f"Error guardando ejecución pendiente: {str(e)}")

    def load_pending_execution(self) -> dict:
        try:
            if self.backup_file.exists():
                with open(self.backup_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Error cargando ejecución pendiente: {str(e)}")
        return None

    def clear_pending_execution(self) -> None:
        try:
            if self.backup_file.exists():
                self.backup_file.unlink()
        except Exception as e:
            logging.error(f"Error eliminando archivo de ejecución pendiente: {str(e)}")

    def mark_as_expired(self) -> None:
        try:
            if self.backup_file.exists():
                with open(self.backup_file, 'r') as f:
                    data = json.load(f)
                    data['status'] = 'expired'
                
                with open(self.expired_file, 'w') as f:
                    json.dump(data, f)

                self.clear_pending_execution()
                logging.info(f"Se ha marcado como expirado la ejecución pendiente.")
        except Exception as e:
            logging.error(f"Error marcando ejecución como expirado: {str(e)}")
