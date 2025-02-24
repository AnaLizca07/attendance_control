import os
from datetime import date
from typing import Union, Optional
from dotenv import load_dotenv # type: ignore

load_dotenv()

ZK_DEVICE = {
    'ip': os.getenv('ZK_DEVICE_IP'),
    'port': int(os.getenv('ZK_DEVICE_PORT')),
    'password': os.getenv('ZK_DEVICE_PASSWORD'),
    'timeout': int(os.getenv('ZK_DEVICE_TIMEOUT'))
}

class FilePathManager:
    """
    Class that manages file paths for the application.
    
    This utility handles directory creation and standardized file naming
    for attendance records and device information files.
    
    Attributes:
        base_dir (str): Base directory for the application.
        database_dir (str): Directory for all data files.
        output_dir (str): Directory for attendance output files.
        device_dir (str): Directory for device information files.
    """

    def __init__(self, base_dir: Optional[str] = None):
        """
        Initializes the file path manager and creates required directories.
        
        Args:
            base_dir (Optional[str]): Custom base directory path. If None, uses the
                                      parent directory of the current file location.
        """
        # Get the data directory
        self.base_dir = base_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.database_dir = os.path.join(self.base_dir, 'data')
        self.output_dir = os.path.join(self.database_dir, 'attandance_output')
        self.device_dir = os.path.join(self.database_dir, 'device_info')

        # Create directories if they do not exist
        for directory in [self.database_dir, self.output_dir, self.device_dir]:
            os.makedirs(directory, exist_ok=True)

    def get_json_filename(self, identifier: Union[date, str], file_type: str = 'attendance') -> str:
        """
        Generates standardized file paths based on an identifier and file type.
        
        The method handles two types of identifiers:
        - date objects: Converted to YYYYMMDD format and saved in the output directory
        - strings: Sanitized to ensure filesystem safety and saved in the device directory
        
        Args:
            identifier (Union[date, str]): Date or string to use in the filename.
            file_type (str): Type of file (defaults to 'attendance').
            
        Returns:
            str: Full path to the JSON file.
            
        Raises:
            ValueError: If the identifier is empty.
        """
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