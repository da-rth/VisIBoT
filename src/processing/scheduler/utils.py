from datetime import datetime


def time_until(next_mins: int):
    now_dt = datetime.utcnow()

    if now_dt.minute >= next_mins:
        hour = now_dt.hour+1
        hour = hour if hour < 23 else 0
        next_dt = now_dt.replace(second=0, minute=next_mins, hour=hour)
    else:
        next_dt = now_dt.replace(second=0, minute=next_mins)

    return next_dt.strftime('%H:%M:%S')
