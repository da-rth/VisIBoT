from datetime import datetime


def time_until(next_mins: int) -> str:
    """
    Calculates the timestamp at which the specified minute number will next occur.

    Example:
    - if the time is 12:03:00 and next_mins=15, time_until(15) will produce the timestamp 12:15:00
    - if the time is 12:45:30 and next_mins=15, time_until(15) will produce the timestamp 13:15:00

    Args:
        next_mins (int): The nth minute into an hour, used to calculate the time_until timestamp

    Returns:
        str: A datetime timestamp string in the format HH:MM:SS
    """
    now_dt = datetime.utcnow()

    if now_dt.minute >= next_mins:
        hour = now_dt.hour+1
        hour = hour if hour < 23 else 0
        next_dt = now_dt.replace(second=0, minute=next_mins, hour=hour)
    else:
        next_dt = now_dt.replace(second=0, minute=next_mins)

    return next_dt.strftime('%H:%M:%S')
