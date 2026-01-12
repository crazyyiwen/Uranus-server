from datetime import datetime

def get_today_str() -> str:
    """Get current date in a human-readable format."""
    today = datetime.now()
    return f"{today.strftime('%a %b')} {today.day}, {today.year}"

