# import sys
# sys.path.append('/home/hoangnam/Documents/code/xProjects/bkchatbot')


from dateutil import parser
from backend.db import db
from backend.crawler.schedule_crawler import get_schedule
from backend.crawler.calender_crawler import get_callender
import json

def get_respone(sender_id, msg, entities):
    if not entities:
        return 'xin lỗi, hãy cho tớ thời gian cụ thể hơn được không?'

    # just for debug
    with open('/home/hoangnam/Documents/code/xProjects/bkchatbot/backend/logic/debug/entities.json', 'a') as f:
        json.dump(entities, f)
    
    # if sid not have yet??
        # ask user
    
    # already have sid
    sid = db.get_sid(sender_id)
    schedule_table = get_schedule_table(sid)
    start_time_str = get_start_time_str(entities)
    return get_response_text(start_time_str, schedule_table)


def get_schedule_table(sid):
    if db.has_schedule(sid):
        schedule_table = db.get_schedule(sid)
    else:
        schedule_table = get_schedule(sid)
        db.set_schedule(sid, schedule_table)
    return schedule_table


# start_time help detect this time is morning or afternoon
def get_start_time_str(entities):
    start_time_str = ''
    if len(entities) > 0:
        value = entities[0]['value']
        if isinstance(value, str):
            start_time_str = value
        elif isinstance(value, dict):
            start_time_str = value['from']
    return start_time_str


def get_response_text(start_time_str, schedule_table):
    if not start_time_str:
        return 'xin lỗi, hãy cho tớ thời gian cụ thể hơn được không?'

    start_time = parser.parse(start_time_str)
    time = start_time.hour
    # because Monday is 0
    weekday = start_time.weekday() + 2

    schedule = []
    for row in schedule_table:
        subject_start_time = int(row['time'].split(',')[1].split('-')[0].split('h')[0].strip())
        # morning
        if (time == 4) and (subject_start_time >= 12):
            continue
        # afternoon
        if (time == 12) and (subject_start_time < 12):
            continue

        weekday_of_subject = int(row['time'].split(',')[0].split(' ')[1].strip())
        week_now = int(get_callender()[1])
        if (weekday_of_subject == weekday) and (week_now in get_weeks_of_subject(row)):
            schedule.append("|".join(row.values()))
    if len(schedule) == 0:
        return "Không có môn học nào vào thời gian đó bạn nhé!"
    else:
        return "\n".join(schedule)

# get list of weeks
def get_weeks_of_subject(subject_schedule):
    weeks = subject_schedule['weeks']
    week_A_start = int(weeks.split(',')[0].split('-')[0])
    week_A_end = int(weeks.split(',')[0].split('-')[1])
    week_B_start = int(weeks.split(',')[1].split('-')[0])
    week_B_end = int(weeks.split(',')[1].split('-')[1])

    weeks = list(range(week_A_start, week_A_end + 1))
    weeks.extend(list(range(week_B_start, week_B_end + 1)))
    return weeks

# entities = [{'start': 0, 'end': 15, 'text': 'ngày 02-06-2020', 'value': '2020-06-02T00:00:00.000+07:00', 'confidence': 1.0, 'additional_info': {'values': [{'value': '2020-06-02T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}], 'value': '2020-06-02T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}, 'entity': 'time', 'extractor': 'DucklingHTTPExtractor'}]
# print(get_respone('2591237020976102', '', entities))