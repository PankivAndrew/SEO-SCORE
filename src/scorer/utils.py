from datetime import datetime
from pytz import timezone


def get_current_timestamp():
    return int(datetime.timestamp(datetime.now(timezone('Europe/Berlin'))))
