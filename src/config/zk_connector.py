from zk import ZK
import traceback
from dotenv import load_dotenv
from config.Logging import Logger
import os

class ZKConnector:
    """
    Class that manages connections to ZK biometric devices.
    
    This connector handles establishing connections to ZK devices, 
    enabling/disabling the device during operations, and safely
    disconnecting when operations are complete.
    
    Attributes:
        zk (ZK): ZK library connection object configured with device parameters.
        log: Logger instance for event logging.
        conn: Active connection to the ZK device.
    """
    def __init__(self):
        """
        Initializes the ZK connector with configuration from environment variables.
        
        Loads connection parameters from environment variables:
        - ZK_DEVICE_IP: IP address of the ZK device
        - ZK_DEVICE_PORT: Port number for connection
        - ZK_DEVICE_TIMEOUT: Connection timeout in seconds
        - ZK_DEVICE_PASSWORD: Password for device authentication
        """
        load_dotenv()
        self.zk = ZK(
            os.getenv('ZK_DEVICE_IP'),
            port=int(os.getenv('ZK_DEVICE_PORT', '')),
            timeout=int(os.getenv('ZK_DEVICE_TIMEOUT', '')),
            password=os.getenv('ZK_DEVICE_PASSWORD', '')
        )
        self.log = Logger.get_logger()
        self.conn = None

    def connect(self):
        """
        Establishes a connection with the ZK device and disables it for operations.
        
        Disabling the device prevents it from performing its regular functions
        while data is being accessed, which helps prevent data corruption.
        
        Returns:
            Connection object if successful, None if connection fails.
        
        Raises:
            Exception: Any exception that occurs during the connection process
                      will be caught, logged, and None will be returned.
        """
        try:
            if not self.conn:
                self.conn = self.zk.connect()
                if self.conn:
                    self.log.debug("Successfully connected to device")
                    self.conn.disable_device()
                else:
                   self.log.error("Connection failed") 
            return self.conn
        except Exception as e:
            self.log.error(f"Error connecting to device: {e}")
            self.log.error(f"Error type: {type(e)}")
            self.log.error(traceback.format_exc())
            return None

    def disconnect(self):
        """
        Safely disconnects from the ZK device after re-enabling it.
        
        This method re-enables the device to resume its normal operations
        before disconnecting, ensuring the device returns to a functional state.
        
        Raises:
            Exception: Any exception that occurs during disconnection
                      will be caught and logged.
        """
        try:
            if self.conn:
                self.conn.enable_device()
                self.conn.disconnect()
                self.conn = None
        except Exception as e:
            self.log.error(f"Error disconnecting: {e}")