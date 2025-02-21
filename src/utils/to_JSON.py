import json
from config.Logging import Logger

class ToJSON:
    @staticmethod
    def save_json_output(data, filename):
        log = Logger.get_logger()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        log.debug(f"\nData saved in: {filename}")