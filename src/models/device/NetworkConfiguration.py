from dataclasses import dataclass
from typing import Dict

@dataclass
class NetworkConfiguration:
    ip: str
    gateway: str
    
    @classmethod
    def from_dict(cls, network_params: Dict[str, str]) -> 'NetworkConfiguration':
        return cls(
            ip=network_params.get('ip', ''),
            gateway=network_params.get('gateway', '')
        )