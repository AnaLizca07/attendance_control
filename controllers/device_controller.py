from models.device import Device
from views.console_views import ConsoleView
from config.settings import get_json_filename_device
import os
import re

class DeviceController: 
    def __init__(self, connector):
        self.connector = connector
        self.view = ConsoleView()

    def get_device_info(self):
        """Get and process device information."""
        conn = None
        try:
            # Attempt connection
            conn = self.connector.connect()
            if not conn:
                print("Error: Could not establish connection with device")
                return False

            # Get device information
            device_info = Device.get_device_info(conn)
            device_id = device_info.get('device_name', 'unknown_device')

            sanitized_device_id = re.sub(r'[<>:"/\\|?*]', '_', device_id)

            # Prepare JSON output
            json_output = {
                'device': device_id,
                'description': device_info.get('description', {})
            }

            # Display information
            self.view.display_device_info(device_info)

            # Generate filename with timestamp
            json_filename = f"device_{sanitized_device_id}.json"
            
            # Ensure directory exists
            os.makedirs('output', exist_ok=True)
            json_filepath = os.path.join('output', json_filename)

            # Save to JSON
            self.view.save_json_output(json_output, json_filepath)
            return True

        except Exception as e:
            print(f"Error getting device information: {str(e)}")
            return False
        finally:
            if conn:
                self.connector.disconnect()
