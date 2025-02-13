from models.device import Device
from views.to_JSON import ToJSON
import os
import re

class DeviceController: 
    def __init__(self, connector):
        self.connector = connector
        self.view = ToJSON()
        self.device_info_fetched = False
        self.device_info = None

    def get_device_info(self):
        """Get and process device information."""
        if self.device_info_fetched:
            return self.device_info

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
