from typing import Optional
from models.device.Device import Device
from controllers.FileHandler import DeviceFileManager, DeviceInfo
from models.device.DeviceValidator import DeviceDataValidator
from config.Logging import Logger


class DeviceController:
    """
    Class that manages device interactions, information retrieval, and persistence.
    
    This controller handles the connection to a device, fetches device information,
    and saves it using a file manager.
    
    Attributes:
        connector: Connection handler for the device.
        file_manager (DeviceFileManager): Manager to handle saving device information.
        _device_info (Optional[DeviceInfo]): Cached device information.
    """
    def __init__(self, connector, file_manager: Optional[DeviceFileManager] = None):
        """
        Initializes the device controller.
        
        Args:
            connector: Connection handler for the device.
            file_manager (Optional[DeviceFileManager]): File manager for saving device information.
                                                        If None, a new DeviceFileManager is created.
        """
        self.connector = connector
        self.file_manager = file_manager or DeviceFileManager()
        self._device_info: Optional[DeviceInfo] = None
        
    @property
    def device_info(self) -> Optional[DeviceInfo]:
        """
        Property that provides access to the cached device information.
        
        Returns:
            Optional[DeviceInfo]: The cached device information, or None if not available.
        """
        return self._device_info
        
    def fetch_device_info(self) -> Optional[DeviceInfo]:
        """
        Connects to the device, retrieves device information, and saves it.
        
        This method establishes a connection with the device, retrieves the device
        information, saves it using the file manager, and caches it.
        
        Returns:
            Optional[DeviceInfo]: The retrieved device information, or None if an error occurred.
            
        Raises:
            ConnectionError: If connection with the device cannot be established.
            ValueError: If no device information is returned.
        """
        conn = None
        try:
            conn = self._establish_connection()
            if not conn:
                raise ConnectionError("Could not establish connection with device")
                
            device = Device(DeviceDataValidator())
            device_info = device.get_device_info(conn)
            
            if not device_info:
                raise ValueError("No device info returned")
            
            self.file_manager.save_device_info(device_info)
            self._device_info = device_info

            return device_info
            
        except Exception as e:
            self._log_error("Error fetching device info", e)
            return None
            
        finally:
            self._close_connection(conn)
        

    def get_device_info(self) -> Optional[DeviceInfo]:
        """
        Gets device information, fetching it if not already cached.
        
        This method returns the cached device information if available,
        otherwise it calls fetch_device_info() to retrieve it.
        
        Returns:
            Optional[DeviceInfo]: The device information, or None if an error occurred.
        """
        try:
            if not self._device_info:
                self._device_info = self.fetch_device_info()
            return self._device_info
                    
        except Exception as e:
            self._log_error("Error in get_device_info", e)
            return None
            
    def _establish_connection(self):
        """
        Establishes connection with the device.
        
        Returns:
            Connection object from the connector.
            
        Raises:
            ConnectionError: If connection cannot be established.
        """
        conn = self.connector.connect()
        if not conn:
            raise ConnectionError("Failed to establish connection")
        return conn
        
    def _close_connection(self, conn) -> None:
        """
        Safely closes the connection if it exists.
        
        Args:
            conn: Connection object to close.
        """
        if conn:
            try:
                self.connector.disconnect()
            except Exception as e:
                self._log_error("Error closing connection", e)
                
    @staticmethod
    def _log_error(message: str, error: Exception) -> None:
        """
        Centralizes error logging.
        
        Args:
            message (str): Error description message.
            error (Exception): Exception that occurred.
        """
        log = Logger.get_logger()
        """Centralizes error logging."""
        log.error(f"Error: {message} - {str(error)}")