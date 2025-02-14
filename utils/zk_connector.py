from zk import ZK, const
from dotenv import load_dotenv
import os

class ZKConnector: 
    def __init__(self):
        load_dotenv()
        self.zk = ZK(
            os.getenv('ZK_DEVICE_IP'), 
            port = int(os.getenv('ZK_DEVICE_PORT')),
            timeout = int(os.getenv('ZK_DEVICE_TIMEOUT')), 
            password = os.getenv('ZK_DEVICE_PASSWORD')
        )
        self.conn = None

    def connect(self):
        try:
            self.conn = self.zk.connect()
            self.zk.disable_device()
            return self.conn
        except Exception as e:
            print(f"Error connecting to device: {e}")
            return None
        
    def disconnect(self):
        if self.conn:
            self.zk.enable_device()
            self.zk.disconnect()