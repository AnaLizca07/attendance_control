import json
from config.Logging import Logger

class ToJSON:
    """
    Utility class for saving data in JSON format.
    
    This class provides a static method for saving Python data structures
    to JSON files with consistent formatting and proper encoding.
    """
    @staticmethod
    def save_json_output(data, filename):
        """
        Saves data to a JSON file with proper formatting.
        
        This method writes data to a file in JSON format with consistent 
        indentation and UTF-8 encoding to ensure proper handling of
        non-ASCII characters.
        
        Args:
            data: The Python data structure to save (must be JSON-serializable).
            filename: Path to the output file.
        
        Note:
            The method logs the save operation using the application's
            logging system.
        """
        log = Logger.get_logger()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        log.debug(f"\nData saved in: {filename}")