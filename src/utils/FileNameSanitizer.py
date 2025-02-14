import re

class FileNameSanitizer:
    INVALID_CHARS_PATTERN = re.compile(r'[<>:"/\\|?*]')
    
    @classmethod
    def sanitize(cls, filename: str) -> str:
        return cls.INVALID_CHARS_PATTERN.sub('_', filename)