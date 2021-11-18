from datetime import datetime, timedelta
from pytz import timezone
from tzlocal import get_localzone

def calculate_offset(now_stamp):
    """计算时区偏移量"""
    local_time = datetime.fromtimestamp(now_stamp, tz=get_localzone())
    utc_time = datetime.utcfromtimestamp(now_stamp)
    offset = int(local_time.hour - utc_time.hour) * 3600

    print("TimeZone Offset：",int(local_time.hour - utc_time.hour))
    return offset

