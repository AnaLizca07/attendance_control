from zk import const

class Device:
    @staticmethod
    def get_device_info(conn):
        device_info = {
            "device_name": conn.get_device_name(),
            "description": 
            {
            "serial_number": conn.get_serialnumber(),
            "mac_address": conn.get_mac(),
            "ip": conn.get_network_params().get("ip"),
            "gateway" : conn.get_network_params().get("gateway"),
            }
        }
        return device_info