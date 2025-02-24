from zk import ZK
import traceback
from dotenv import load_dotenv
from config.Logging import Logger
import os

class ZKConnector:
    def __init__(self):
        load_dotenv()
        self.zk = ZK(
            os.getenv('ZK_DEVICE_IP'),
            port=int(os.getenv('ZK_DEVICE_PORT', '4370')),
            timeout=int(os.getenv('ZK_DEVICE_TIMEOUT', '5')),
            password=os.getenv('ZK_DEVICE_PASSWORD', '0')
        )
        self.log = Logger.get_logger()
        self.conn = None

    def connect(self):
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
        try:
            if self.conn:
                self.conn.enable_device()
                self.conn.disconnect()
                self.conn = None
        except Exception as e:
            self.log.error(f"Error disconnecting: {e}")