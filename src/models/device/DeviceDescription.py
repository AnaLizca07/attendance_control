from dataclasses import dataclass
from typing import Dict
from models.device.NetworkConfiguration import NetworkConfiguration

@dataclass
class DeviceDescription:
    serial_number: str
    mac_address: str
    network_config: NetworkConfiguration

    @classmethod
    def create(cls, serial_number: str, mac_address: str, 
              network_params: Dict[str, str]) -> 'DeviceDescription':
        return cls(
            serial_number=serial_number,
            mac_address=mac_address,
            network_config=NetworkConfiguration.from_dict(network_params)
        )
