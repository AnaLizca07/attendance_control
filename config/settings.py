import os


ZK_DEVICE = {
    'ip': '192.168.0.3',
    'port': 4370,
    'password': 2121,
    'timeout': 10
}


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_json_filename(date):
    date_str = date.strftime('%Y%m%d')
    return os.path.join(OUTPUT_DIR, f'attendance_{date_str}.json')

def get_json_filename_device(device_id):
    # Clean device_id by replacing invalid filename characters
    clean_device_id = "".join(c if c.isalnum() else "_" for c in str(device_id))
    
    filename = f"device_{clean_device_id}.json"
    
    # Create logs directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    return os.path.join('device_info', filename)