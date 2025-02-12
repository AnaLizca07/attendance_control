from zk import ZK, const
from config.settings import ZK_DEVICE

class ZKConnector: 
    def __init__(self):
        self.zk = ZK(
            ZK_DEVICE['ip'], 
            port=ZK_DEVICE['port'], 
            timeout=ZK_DEVICE['timeout'], 
            password=ZK_DEVICE['password']
        )
        self.conn = None

    def connect(self):
        try:
            self.conn = self.zk.connect()
            print('Desactivando dispositivo')
            self.zk.disable_device()
            return self.conn
        except Exception as e:
            print(f"Error al conectar con el dispositivo: {e}")
            return None
        
    def disconnect(self):
        if self.conn:
            print('Activando dispositivo')
            self.zk.enable_device()
            self.zk.disconnect()
            print('Desconectado del dispositivo')