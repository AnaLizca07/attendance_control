from dataclasses import dataclass
from typing import Dict
from models.device.NetworkConfiguration import NetworkConfiguration

@dataclass
class DeviceDescription:
    """
    Data class representing the technical description of a device.
    
    This class stores identifying information such as serial number,
    MAC address, and network configuration details for a device.
    
    Attributes:
        serial_number (str): The device's serial number.
        mac_address (str): The device's MAC address.
        network_config (NetworkConfiguration): The device's network configuration.
    """
    serial_number: str
    mac_address: str
    network_config: NetworkConfiguration

    @classmethod
    def create(cls, serial_number: str, mac_address: str, 
              network_params: Dict[str, str]) -> 'DeviceDescription':
        """
        Creates a DeviceDescription instance with the specified parameters.
        
        Args:
            serial_number (str): The device's serial number.
            mac_address (str): The device's MAC address.
            network_params (Dict[str, str]): Dictionary containing network configuration
                                            parameters for the device.
            
        Returns:
            DeviceDescription: A new instance with the specified parameters, where
                              network_params is converted to a NetworkConfiguration object.
        """
        return cls(
            serial_number=serial_number,
            mac_address=mac_address,
            network_config=NetworkConfiguration.from_dict(network_params)
        )