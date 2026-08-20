import os

class InputValidationError(Exception):
    """Custom exception raised when user input fails validation rules."""
    pass

def validate_text(text: str, field_name: str = "Input text") -> str:
    """
    Validates that the provided text is a non-empty string.
    Returns cleaned stripped text or raises InputValidationError.
    """
    if text is None or not isinstance(text, str):
        raise InputValidationError(f"{field_name} must be a valid text string.")
    
    cleaned = text.strip()
    if not cleaned:
        raise InputValidationError(f"{field_name} cannot be empty or contain only whitespace.")
    
    return cleaned

def validate_file_path(file_path: str, max_size_mb: float = 5.0) -> str:
    """
    Validates that a file path exists, is a .txt file, and is within size limits.
    """
    if not file_path or not isinstance(file_path, str):
        raise InputValidationError("File path must be a non-empty string.")
    
    if not os.path.exists(file_path):
        raise InputValidationError(f"File not found: {file_path}")
    
    if not os.path.isfile(file_path):
        raise InputValidationError(f"Path is not a file: {file_path}")
    
    if not file_path.lower().endswith(".txt"):
        raise InputValidationError(f"Unsupported file type for '{file_path}'. Only .txt files are supported.")
    
    size_bytes = os.path.getsize(file_path)
    if size_bytes == 0:
        raise InputValidationError(f"The file '{file_path}' is empty (0 bytes).")
    
    max_bytes = max_size_mb * 1024 * 1024
    if size_bytes > max_bytes:
        raise InputValidationError(f"File size exceeds limit of {max_size_mb}MB.")
    
    return file_path
