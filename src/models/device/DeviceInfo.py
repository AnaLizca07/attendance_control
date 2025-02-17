from dataclasses import dataclass
from models.device.DeviceDescription import DeviceDescription
from typing import Dict, List, Optional
import uuid

@dataclass
class DeviceInfo:
    device_id : str
    device_name: str
    description: DeviceDescription

    @classmethod
    def create(cls,device_name: str, description: DeviceDescription) -> 'DeviceInfo':
        return cls(
            device_id = str(uuid.uuid4()),
            device_name=device_name,
            description=description
        )
    
    @classmethod
    def from_dict(cls, data: Optional[Dict]) -> Optional['DeviceInfo']:
        if not data or not isinstance(data, dict):
            return None
            
        try:
            description = DeviceDescription.create(
                serial_number=data.get('serial_number', ''),
                mac_address=data.get('mac_address', ''),
                network_params=data.get('network_params', {})
            )
            
            return cls(
                device_id = data.get('device_id', str(uuid.uuid4())),
                device_name=data.get('device_name', ''),
                description=description
            )
        except Exception:
            return None