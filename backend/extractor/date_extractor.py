import pytz
import datetime
import re

REGEX_DATE = r"(3[01]|[12][0-9]|0?[1-9])[-\/:|](1[0-2]|0?[1-9])([-\/:|](2[0-1][0-9][0-9]))"
REGEX_DAY_MONTH = r"(3[01]|[12][0-9]|0?[1-9])[-\/:|](1[0-2]|0?[1-9])"
REGEX_MONTH_YEAR = r"(1[0-2]|0?[1-9])([-\/:|](2[0-1][0-9][0-9]))"

def regex_date(msg, timezone="Asia/Ho_Chi_Minh"):
    ''' use regex to capture date string format '''

    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz=tz)

    date_str = []
    regex = REGEX_DATE
    regex_day_month = REGEX_DAY_MONTH
    regex_month_year = REGEX_MONTH_YEAR
    pattern = re.compile("(%s|%s|%s)" % (
        regex, regex_month_year, regex_day_month), re.UNICODE)

    matches = pattern.finditer(msg)
    for match in matches:
        _dt = match.group(0)
        _dt = _dt.replace("/", "-").replace("|", "-").replace(":", "-")
        for i in range(len(_dt.split("-"))):
            if len(_dt.split("-")[i]) == 1:
                _dt = _dt.replace(_dt.split("-")[i], "0"+_dt.split("-")[i])
        if len(_dt.split("-")) == 2:
            pos1 = _dt.split("-")[0]
            pos2 = _dt.split("-")[1]
            if 0 < int(pos1) < 32 and 0 < int(pos2) < 13:
                _dt = pos1+"-"+pos2+"-"+str(now.year)
        date_str.append(_dt)
    return date_str

