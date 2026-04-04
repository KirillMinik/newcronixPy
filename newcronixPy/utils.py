from datetime import datetime


def parse_time(time_str: str):
    return datetime.strptime(time_str, "%H:%M")