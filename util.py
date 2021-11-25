from datetime import datetime, timedelta
from pytz import timezone
from tzlocal import get_localzone
import time
import sys
import logging
from Conf import conf


def config_logging(file_name: str, console_level: int=logging.INFO, file_level: int=logging.INFO):
    file_handler = logging.FileHandler(file_name, mode='a', encoding="utf8")
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(module)s.%(lineno)d %(name)s:\t%(message)s')
        )
    file_handler.setLevel(file_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '[%(asctime)s %(levelname)s] %(message)s',
        datefmt="%Y/%m/%d %H:%M:%S")
        )
    console_handler.setLevel(console_level)

    logging.basicConfig(
        level=min(console_level, file_level),
        handlers=[file_handler, console_handler],
        )

if conf["isDebug"]:
    config_logging("kawaii_island.log", logging.DEBUG, logging.DEBUG)
else:
    config_logging("kawaii_island.log", logging.INFO, logging.INFO)

def log_debug(content):
    logging.debug(content)
def log_info(content):
    logging.info(content)

def log_exception():
    logging.exception(sys.exc_info())






def calculate_offset(now_stamp):
    """计算时区偏移量"""
    ts = time.time()
    utc_offset = int((datetime.fromtimestamp(ts) - datetime.utcfromtimestamp(ts)).total_seconds() / 3600)
    return utc_offset

