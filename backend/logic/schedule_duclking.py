# import sys
# sys.path.append('/home/hoangnam/Documents/code/xProjects/bkchatbot')

import json
from dateutil import parser

from backend.db import db
from backend.crawler import calender_crawler
from backend.crawler import schedule_crawler


def get_respone(sender_id, time_entities):
    # if can not extract time
    if not time_entities: 
        return 'xin lỗi, bạn có thể cho tớ thời gian cụ thể hơn được không?'

    # just for debug
    with open('/home/hoangnam/Documents/code/xProjects/bkchatbot/backend/logic/debug/time_entities.json', 'a') as f:
        json.dump(time_entities, f)
    
    # if already have sid
    sid = db.get_sid(sender_id)
    if not db.has_schedule_table(sid):
        db.set_schedule_table(sid, schedule_crawler.crawl_schedule_table(sid))
    return filter_schedule(time_entities, db.get_schedule_table(sid))


def filter_schedule(time_entities, schedule_table):
    time_str = get_time_str(time_entities)
    if not time_str:              # just for fallback
        return 'xin lỗi, bạn có thể cho tớ thời gian cụ thể hơn được không?' 
    time = parser.parse(time_str)
    hour = time.hour              # hour help detect morning or afternoon
    weekday = time.weekday() + 2  # because Monday is 0

    schedule = []
    for row in schedule_table:
        subject_start_time = int(row['time'].split(',')[1].split('-')[0].split('h')[0].strip())
        if (hour == 4) and (subject_start_time >= 12): # morning
            continue
        if (hour == 12) and (subject_start_time < 12): # afternoon
            continue
        weekday_of_subject = int(row['time'].split(',')[0].split(' ')[1].strip())
        week_now = int(calender_crawler.crawl_callender()[1])
        if (weekday_of_subject == weekday) and (week_now in get_weeks_of_subject(row)):
            schedule.append("|".join([row['semester'], row['time'], row['classroom'], row['subject_name']]))
  
    if len(schedule) == 0:
        extracted_text = time_entities[0]['text']
        return f"Không có môn học nào vào {extracted_text} bạn nhé!"
    else:
        return "\n".join(schedule)

# get time_str
def get_time_str(time_entities):
    value = time_entities[0]['value']
    if isinstance(value, str):
        time_str = value
    elif isinstance(value, dict):
        time_str = value['from']
    else:
        time_str = ''
    return time_str

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

# time_entities = [{'start': 0, 'end': 15, 'text': 'ngày 02-06-2020', 'value': '2020-06-02T00:00:00.000+07:00', 'confidence': 1.0, 'additional_info': {'values': [{'value': '2020-06-02T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}], 'value': '2020-06-02T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}, 'entity': 'time', 'extractor': 'DucklingHTTPExtractor'}]
# print(get_respone('2591237020976102', time_entities))