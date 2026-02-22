from datetime import datetime

def get_current_datetime():
    """Returns the current date and time in a formatted string."""
    return datetime.now().strftime("%A, %d %B, %Y %H:%M:%S")
