import os
from datetime import date
from typing import Union, Optional
from dotenv import load_dotenv

load_dotenv()

ZK_DEVICE = {
    'ip': os.getenv('ZK_DEVICE_IP'),
    'port': int(os.getenv('ZK_DEVICE_PORT')),
    'password': os.getenv('ZK_DEVICE_PASSWORD'),
    'timeout': int(os.getenv('ZK_DEVICE_TIMEOUT'))
}

class FilePathManager:
    def __init__(self, base_dir: Optional[str] = None):
        self.documents_dir = os.path.join(os.path.expanduser('~'), 'Documents')
        self.output_dir = os.path.join(self.documents_dir, 'output')
        self.device_dir = os.path.join(self.output_dir, 'device_info')
        
        for directory in [self.output_dir, self.device_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def get_json_filename(self, identifier: Union[date, str], file_type: str = 'attendance') -> str:
        if not identifier:
            raise ValueError("empty identifier")
            
        if isinstance(identifier, date):
            clean_id = identifier.strftime('%Y%m%d')
            target_dir = self.output_dir
        else:
            clean_id = "".join(c if c.isalnum() else "_" for c in str(identifier))
            target_dir = self.device_dir
            
        filename = f"{file_type}_{clean_id}.json"
        return os.path.join(target_dir, filename)