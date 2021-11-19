from datetime import datetime, timedelta
from pytz import timezone
from tzlocal import get_localzone
import time

def calculate_offset(now_stamp):
    """计算时区偏移量"""
    ts = time.time()
    utc_offset = int((datetime.fromtimestamp(ts) - datetime.utcfromtimestamp(ts)).total_seconds() / 3600)
    print("TimeZone Offset：",utc_offset)
    return utc_offset

