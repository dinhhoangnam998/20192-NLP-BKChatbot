from datetime import datetime
from backend.db import db
from backend.crawler.schedule_crawler import get_schedule
from backend.extractor.date_extractor import regex_date
from backend.crawler.calender_crawler import get_callender


def get_response_msg(sender_id, msg):
    # require sid already exits on db
    sid = db.get_sid(sender_id)
    if db.has_schedule(sid):
        schedule_table = db.get_schedule(sid)
    else:
        schedule_table = get_schedule(sid)
        db.set_schedule(sid, schedule_table)

    # just first date for now
    date_str = regex_date(msg)[0]
    weekday = datetime.strptime(date_str, '%d-%m-%Y').weekday()
    result = get_schedule_for_weekday(weekday, schedule_table)
    return "".join(result)
    

def get_schedule_for_weekday(weekday, schedule_table):
    schedule = []
    for k, v in schedule_table.items():
        weekday_of_subject = int(v['time'].split(',')[0].split(' ')[1].strip())
        week_now = int(get_callender()[1])
        if (weekday_of_subject == weekday) and (week_now in get_weeks_of_subject(v)):
            schedule.append(str(v))
    return schedule

def get_weeks_of_subject(subject_schedule):
    weeks = subject_schedule['weeks']
    week_A_start = int(weeks.split(',')[0].split('-')[0])
    week_A_end = int(weeks.split(',')[0].split('-')[1])
    week_B_start = int(weeks.split(',')[1].split('-')[0])
    week_B_end = int(weeks.split(',')[1].split('-')[1])

    weeks = list(range(week_A_start, week_A_end + 1))
    weeks.extend(list(range(week_B_start, week_B_end + 1)))
    return weeks

