# import sys
# sys.path.append('/home/hoangnam/Documents/code/xProjects/bkchatbot')

import json
from dateutil import parser

from backend.db import db
from backend.crawler import calender_crawler
from backend.crawler import schedule_crawler


def get_response(sender_id, time_entities):
    if not time_entities: 
        return 'xin lỗi, bạn có thể cho tớ thời gian cụ thể hơn được không?'

    with open('/home/hoangnam/Documents/code/xProjects/bkchatbot/backend/logic/debug/time_entities.json', 'a') as f:
        json.dump(time_entities, f)

    sid = db.get_sid(sender_id)

    if not db.has_schedule_table(sid):
        db.set_schedule_table(sid, schedule_crawler.crawl_schedule_table(sid))

    schedule = schedule_filter(db.get_schedule_table(sid), time_entities)

    response = make_pretty_string(schedule)
    return response


def schedule_filter(schedule_table, time_entities):
    schedule = []

    for time_entity in time_entities:
        text_extracted = time_entity['text']
        type = time_entity['additional_info']['type']
        if type == 'value':
            grain = time_entity['additional_info']['grain']
            if grain == 'day':
                sub_schedule = (filter_by_weekday(schedule_table, time_entity))
            elif grain == 'hour':
                sub_schedule = (filter_by_hour(schedule_table, time_entity))
            elif grain == 'week':
                sub_schedule = (filter_by_week(schedule_table, time_entity))
            elif grain == 'month':
                sub_schedule = (filter_by_month(schedule_table, time_entity))
            elif grain == 'year':
                sub_schedule = (filter_by_year(schedule_table, time_entity))
        elif type == 'interval':
            grain = time_entity['additional_info']['from']['grain']
            if grain == 'hour':
                sub_schedule = (filter_by_session(schedule_table, time_entity))
            elif grain == 'week':
                sub_schedule = (filter_by_multi_week(schedule_table, time_entity))
            elif grain == 'month':
                sub_schedule = (filter_by_multi_month(schedule_table, time_entity))
        schedule.append({text_extracted: sub_schedule})
    return schedule



def filter_by_weekday(schedule_table, time_entity):
    time_str = get_time_str(time_entity)
    time = parser.parse(time_str)
    weekday = time.weekday() + 2

    schedule = []
    for row in schedule_table:
        weekday_of_subject = int(row['time'].split(',')[0].split(' ')[1].strip())
        weeks_of_subject = get_weeks_of_subject(row)
        week_now = int(calender_crawler.crawl_callender()[1])
        if (weekday_of_subject == weekday) and (week_now in weeks_of_subject):
            schedule.append(row)
    return schedule


def filter_by_hour(schedule_table, time_entity):
    subjects_of_day = filter_by_weekday(schedule_table, time_entity)
    schedule = []
    hour = parser.parse(get_time_str(time_entity)).hour
    for subject in subjects_of_day:
        subject_start_hour = int(subject['time'].split(',')[1].split('-')[0].split('h')[0].strip())
        subject_end_hour = int(subject['time'].split(',')[1].split('-')[1].split('h')[0].strip())
        if subject_start_hour <= hour <= subject_end_hour:
            schedule.append(subject)
    return schedule

def filter_by_week(schedule_table, time_entity):
    schedule = []
    for row in schedule_table:
        weeks_of_subject = get_weeks_of_subject(row)
        week_now = int(calender_crawler.crawl_callender()[1])
        if week_now in weeks_of_subject:
            schedule.append(row)
    return schedule


def filter_by_month(schedule_table, time_entity):
    return schedule_table

def filter_by_year(schedule_table, time_entity):
    return []



def filter_by_session(schedule_table, time_entity):
    subjects_of_day = filter_by_weekday(schedule_table, time_entity)
    start_session_hour = parser.parse(time_entity['value']['from']).hour
    schedule = []
    for subject in subjects_of_day:
        subject_start_time = int(subject['time'].split(',')[1].split('-')[0].split('h')[0].strip())
        if (start_session_hour == 4) and (subject_start_time >= 12): # morning
            continue
        if (start_session_hour == 12) and (subject_start_time < 12): # afternoon
            continue
        schedule.append(subject_start_time)
    return schedule
        

def filter_by_multi_week(schedule_table, time_entity):
    return []


def filter_by_multi_month(schedule_table, time_entity):
    return []



def make_pretty_string(schedule):
    pretty_string = ''
    for sub_schedule_of_time_entity in schedule:
        for text_extracted, subjects in sub_schedule_of_time_entity.items():
            pretty_string += (text_extracted + ':\n')
            for subject in subjects:
                pretty_string += "|".join([subject['semester'], subject['time'], subject['classroom'], subject['subject_name']]) + '\n'
            pretty_string += '\n'
    return pretty_string

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

def get_time_str(time_entity):
    type = time_entity['additional_info']['type']
    if (type == 'value'):
        return time_entity['value']
    else:
        return time_entity['value']['from']

# time_entities = [{'start': 0, 'end': 15, 'text': 'ngày 03-06-2020', 'value': '2020-06-03T00:00:00.000+07:00', 'confidence': 1.0, 'additional_info': {'values': [{'value': '2020-06-03T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}], 'value': '2020-06-03T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}, 'entity': 'time', 'extractor': 'DucklingHTTPExtractor'}, {'start': 19, 'end': 34, 'text': 'ngày 04-06-2020', 'value': '2020-06-04T00:00:00.000+07:00', 'confidence': 1.0, 'additional_info': {'values': [{'value': '2020-06-04T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}], 'value': '2020-06-04T00:00:00.000+07:00', 'grain': 'day', 'type': 'value'}, 'entity': 'time', 'extractor': 'DucklingHTTPExtractor'}]
# print(get_response('2591237020976102', time_entities))
