from typing import Dict

class DeviceDataValidator:
    @staticmethod
    def validate_network_params(params: Dict) -> bool:
        required_fields = {'ip', 'gateway'}
        return all(
            params.get(field) is not None 
            for field in required_fields
        )
    
    @staticmethod
    def validate_device_name(name: str) -> bool:
        return bool(name and isinstance(name, str))
    
    @staticmethod
    def validate_mac_address(mac: str) -> bool:
        return bool(mac and isinstance(mac, str))
    
    @staticmethod
    def validate_serial_number(serial: str) -> bool:
        return bool(serial and isinstance(serial, str))