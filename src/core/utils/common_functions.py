from datetime import datetime
import os
from pathlib import Path

def get_today_str() -> str:
    """Get current date in a human-readable format."""
    today = datetime.now()
    return f"{today.strftime('%a %b')} {today.day}, {today.year}"

def get_file_path(file_name: str) -> str:
    return Path(__file__).parent / os.path.join("jsons", file_name)

