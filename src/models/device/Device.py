from typing import Optional
from models.device.DeviceValidator import DeviceDataValidator
from models.device.DeviceInfo import DeviceInfo
from models.device.DeviceDescription import DeviceDescription
from config.Logging import Logger

class Device:
    def __init__(self, data_validator: Optional[DeviceDataValidator] = None):
        self.validator = data_validator or DeviceDataValidator()
        self.log = Logger.get_logger()

    def get_device_info(self, conn) -> Optional[DeviceInfo]:
        try:
            device_name = conn.get_device_name()
            if not self.validator.validate_device_name(device_name):
                raise ValueError("Invalid device name")

            serial_number = conn.get_serialnumber()
            mac_address = conn.get_mac()
            network_params = conn.get_network_params()

            if not all([
                self.validator.validate_serial_number(serial_number),
                self.validator.validate_mac_address(mac_address),
                self.validator.validate_network_params(network_params)
            ]):
                raise ValueError("Invalid device parameters")

            description = DeviceDescription.create(
                serial_number=serial_number,
                mac_address=mac_address,
                network_params=network_params
            )

            return DeviceInfo.create(
                device_name=device_name,
                description=description
            )

        except Exception as e:
            self._handle_error(f"Error getting device info: {str(e)}")
            return None

    def _handle_error(self, error_message: str) -> None:
        self.log.error(error_message)