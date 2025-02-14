from typing import Optional
from models.device.Device import Device
from controllers.FileHandler import DeviceFileManager, DeviceInfo
from models.device.DeviceValidator import DeviceDataValidator


class DeviceController:
    def __init__(self, connector, file_manager: Optional[DeviceFileManager] = None):
        self.connector = connector
        self.file_manager = file_manager or DeviceFileManager()
        self._device_info: Optional[DeviceInfo] = None
        
    @property
    def device_info(self) -> Optional[DeviceInfo]:
        return self._device_info
        
    def fetch_device_info(self) -> Optional[DeviceInfo]:

        conn = None
        try:
            conn = self._establish_connection()
            if not conn:
                raise ConnectionError("Could not establish connection with device")
                
            device = Device(DeviceDataValidator())
            device_info = device.get_device_info(conn)
            
            if not device_info:
                raise ValueError("No device info returned")
                
            return device_info
            
        except Exception as e:
            self._log_error("Error fetching device info", e)
            return None
            
        finally:
            self._close_connection(conn)
        
    def get_device_info(self) -> bool:
        try:
            device_info = self.fetch_device_info()
            if not device_info:
                print("Could not fetch device info")
                return False
                
            self.file_manager.save_device_info(device_info)
            self._device_info = device_info
            return True
            
        except Exception as e:
            self._log_error("Error in get_device_info", e)
            return False
            
    def _establish_connection(self):
        """Establishes connection with the device."""
        conn = self.connector.connect()
        if not conn:
            raise ConnectionError("Failed to establish connection")
        return conn
        
    def _close_connection(self, conn) -> None:
        """Safely closes the connection if it exists."""
        if conn:
            try:
                self.connector.disconnect()
            except Exception as e:
                self._log_error("Error closing connection", e)
                
    @staticmethod
    def _log_error(message: str, error: Exception) -> None:
        """Centralizes error logging."""
        print(f"Error: {message} - {str(error)}")