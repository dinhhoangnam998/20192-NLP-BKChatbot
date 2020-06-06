from datetime import datetime
from .crawlerschedule import get_schedule
from .dateextractor import regex_date

def sender2student(sender_id):
    # TODO: just hardcode for now
    student_id = 20162793
    return student_id

def get_schedule_for_weekday(weekday, schedule_table):
    schedule = []
    for k,v in schedule_table.items():
        if v['day_of_week'] == weekday:
            schedule.append(str(v))
    return schedule


def get_response_msg(sender_id, msg):
    student_id = sender2student(sender_id)
    schedule_table = get_schedule(student_id)
    date_str = regex_date(msg)[0]
    weekday = datetime.strptime(date_str, '%Y-%m-%d').weekday()
    schedule = get_schedule_for_weekday(weekday, schedule_table)
    response = "".join(schedule)
    return response


