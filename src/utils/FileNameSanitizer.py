import re

class FileNameSanitizer:
    """
    Utility class that provides methods for sanitizing filenames.
    
    This class removes or replaces characters that are invalid in filenames
    across different operating systems, ensuring that generated filenames
    are safe to use in file systems.
    
    Attributes:
        INVALID_CHARS_PATTERN (re.Pattern): Compiled regular expression pattern
                                           that matches invalid filename characters.
    """
    INVALID_CHARS_PATTERN = re.compile(r'[<>:"/\\|?*]')
    
    @classmethod
    def sanitize(cls, filename: str) -> str:
        """
        Sanitizes a filename by replacing invalid characters with underscores.
        
        This method removes characters that are typically not allowed in filenames
        across different operating systems, including: < > : " / \ | ? *
        
        Args:
            filename (str): The original filename to sanitize.
            
        Returns:
            str: The sanitized filename with invalid characters replaced by underscores.
        """
        return cls.INVALID_CHARS_PATTERN.sub('_', filename)