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
    texts = get_extracted_text(time_entities)
    time_strs = get_time_str(time_entities)
    schedule = []

    for time_str, text in zip(time_strs, texts):
        schedule.append(text + ":")
        schedule_for_each_day = get_schedule_for_a_day(time_str, text, schedule_table)
        if not schedule_for_each_day:
            schedule.append("Không có môn học nào!\n")
        else:
            schedule.append('\n'.join(schedule_for_each_day))
            schedule.append("")

    if len(schedule) == 0:
        extracted_text = " & ".join(texts)
        return f"Không có môn học nào vào {extracted_text} bạn nhé!"
    else:
        return "\n".join(schedule)


# get time_str
def get_time_str(time_entities):
    time_strs = []
    for time_entity in time_entities:
        value = time_entity['value']
        if isinstance(value, str):
            time_str = value
        elif isinstance(value, dict):
            time_str = value['from']            
        time_strs.append(time_str)
    return time_strs


def get_extracted_text(time_entities):
    texts = []
    for time_entity in time_entities:
        texts.append(time_entity['text'])
    return texts


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


def get_schedule_for_a_day(time_str, text, schedule_table):
    schedule_for_a_day = []
    time = parser.parse(time_str)
    hour = time.hour              # hour help detect morning or afternoon
    weekday = time.weekday() + 2  # because Monday is 0

    for row in schedule_table:
        subject_start_time = int(row['time'].split(',')[1].split('-')[0].split('h')[0].strip())
        if (hour == 4) and (subject_start_time >= 12): # morning
            continue
        if (hour == 12) and (subject_start_time < 12): # afternoon
            continue
        weekday_of_subject = int(row['time'].split(',')[0].split(' ')[1].strip())
        week_now = int(calender_crawler.crawl_callender()[1])
        if (weekday_of_subject == weekday) and (week_now in get_weeks_of_subject(row)):
            schedule_for_a_day.append("|".join([row['semester'], row['time'], row['classroom'], row['subject_name']]))
    return schedule_for_a_day


# time_entities = [{'start': 0, 'end': 15, 'text': 'ngày 03-06-2020', 'value': '2020-06-03T00:00:00.000+07:00', 'confidence': 1.0, 'additional_info': {'values': [{'value': '2020-06-03T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}], 'value': '2020-06-03T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}, 'entity': 'time', 'extractor': 'DucklingHTTPExtractor'}, {'start': 19, 'end': 34, 'text': 'ngày 04-06-2020', 'value': '2020-06-04T00:00:00.000+07:00', 'confidence': 1.0, 'additional_info': {'values': [{'value': '2020-06-04T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}], 'value': '2020-06-04T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}, 'entity': 'time', 'extractor': 'DucklingHTTPExtractor'}]
# print(get_respone('2591237020976102', time_entities))

