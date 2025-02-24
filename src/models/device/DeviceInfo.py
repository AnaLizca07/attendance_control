from dataclasses import dataclass
from models.device.DeviceDescription import DeviceDescription
from typing import Dict, List, Optional

@dataclass
class DeviceInfo:
    """
    Data class representing core device information.
    
    This class stores essential device data including the device identifier,
    name, and detailed device description.
    
    Attributes:
        device_id (str): Unique identifier for the device, typically the serial number.
        device_name (str): User-friendly name for the device.
        description (DeviceDescription): Detailed technical description of the device.
    """
    device_id: str
    device_name: str
    description: DeviceDescription

    @classmethod
    def create(cls, device_name: str, description: DeviceDescription) -> 'DeviceInfo':
        """
        Creates a DeviceInfo instance using the device name and description.
        
        Uses the serial number from the description as the device_id.
        
        Args:
            device_name (str): User-friendly name for the device.
            description (DeviceDescription): Detailed description of the device.
            
        Returns:
            DeviceInfo: A new instance with the specified parameters.
        """
        device_id = description.serial_number

        return cls(
            device_id=device_id,
            device_name=device_name,
            description=description
        )
    
    @classmethod
    def from_dict(cls, data: Optional[Dict]) -> Optional['DeviceInfo']:
        """
        Creates a DeviceInfo instance from a dictionary of device data.
        
        Args:
            data (Optional[Dict]): Dictionary containing device information.
                                   Expected to contain keys for 'device_id', 'device_name',
                                   'serial_number', 'mac_address', and 'network_params'.
            
        Returns:
            Optional[DeviceInfo]: A new instance if the data is valid, None otherwise.
        """
        if not data or not isinstance(data, dict):
            return None
            
        try:
            description = DeviceDescription.create(
                serial_number=data.get('serial_number', ''),
                mac_address=data.get('mac_address', ''),
                network_params=data.get('network_params', {})
            )
            
            return cls(
                device_id=data.get('device_id', description.serial_number),
                device_name=data.get('device_name', ''),
                description=description
            )
        except Exception:
            return None