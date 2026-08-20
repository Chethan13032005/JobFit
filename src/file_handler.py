import os
from src.validator import validate_file_path, InputValidationError

def read_txt_file(file_path: str) -> str:
    """
    Safely reads and returns the text content of a .txt file.
    Handles FileNotFoundError, PermissionError, and UnicodeDecodeError cleanly.
    """
    validated_path = validate_file_path(file_path)
    
    try:
        with open(validated_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read().strip()
            
        if not content:
            raise InputValidationError(f"File '{os.path.basename(validated_path)}' contains no readable text.")
            
        return content
    except PermissionError:
        raise InputValidationError(f"Permission denied when attempting to read '{file_path}'.")
    except Exception as e:
        if isinstance(e, InputValidationError):
            raise e
        raise InputValidationError(f"Error reading file '{file_path}': {str(e)}")
