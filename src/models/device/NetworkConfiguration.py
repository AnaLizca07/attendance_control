from dataclasses import dataclass
from typing import Dict

@dataclass
class NetworkConfiguration:
    """
    Data class that represents network configuration parameters.
    
    This class stores network-related settings like IP address and gateway.
    
    Attributes:
        ip (str): The IP address.
        gateway (str): The gateway address.
    """
    ip: str
    gateway: str
    
    @classmethod
    def from_dict(cls, network_params: Dict[str, str]) -> 'NetworkConfiguration':
        """
        Creates a NetworkConfiguration instance from a dictionary of network parameters.
        
        Args:
            network_params (Dict[str, str]): Dictionary containing network configuration 
                                            parameters with 'ip' and 'gateway' keys.
                                            
        Returns:
            NetworkConfiguration: A new instance with the specified parameters.
                                 Empty strings are used as defaults if keys are missing.
        """
        return cls(
            ip=network_params.get('ip', ''),
            gateway=network_params.get('gateway', '')
        )