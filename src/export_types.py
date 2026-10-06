"""Export Type Definitions."""
from enum import Enum

class ExportFormat(str, Enum):
    MARKDOWN = "markdown"
    CSV = "csv"
    JSON = "json"
    HTML = "html"
