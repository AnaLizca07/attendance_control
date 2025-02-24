from typing import Dict

class DeviceDataValidator:
    """
    Utility class that provides static methods for validating device-related data.
    
    This class contains validation methods for various device properties such as
    network parameters, device name, MAC address, and serial number.
    """
    
    @staticmethod
    def validate_network_params(params: Dict) -> bool:
        """
        Validates that the required network parameters are present in the dictionary.
        
        Args:
            params (Dict): Dictionary containing network parameters.
            
        Returns:
            bool: True if all required fields ('ip' and 'gateway') are present and not None,
                  False otherwise.
        """
        required_fields = {'ip', 'gateway'}
        return all(
            params.get(field) is not None 
            for field in required_fields
        )
    
    @staticmethod
    def validate_device_name(name: str) -> bool:
        """
        Validates a device name.
        
        Args:
            name (str): The device name to validate.
            
        Returns:
            bool: True if name is a non-empty string, False otherwise.
        """
        return bool(name and isinstance(name, str))
    
    @staticmethod
    def validate_mac_address(mac: str) -> bool:
        """
        Validates a MAC address.
        
        Args:
            mac (str): The MAC address to validate.
            
        Returns:
            bool: True if MAC is a non-empty string, False otherwise.
        """
        return bool(mac and isinstance(mac, str))
    
    @staticmethod
    def validate_serial_number(serial: str) -> bool:
        """
        Validates a device serial number.
        
        Args:
            serial (str): The serial number to validate.
            
        Returns:
            bool: True if the serial number is a non-empty string, False otherwise.
        """
        return bool(serial and isinstance(serial, str))