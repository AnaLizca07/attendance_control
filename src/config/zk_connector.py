from zk import ZK
from dotenv import load_dotenv
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
        self.conn = None

    def connect(self):
        try:
            if not self.conn:
                self.conn = self.zk.connect()
                if self.conn:
                    print("Successfully connected to device")
                    self.conn.disable_device()
                else:
                   print("Connection failed") 
            return self.conn
        except Exception as e:
            print(f"Error connecting to device: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            print(traceback.format_exc())
            return None

    def disconnect(self):
        try:
            if self.conn:
                self.conn.enable_device()
                self.conn.disconnect()
                self.conn = None
        except Exception as e:
            print(f"Error disconnecting: {e}")