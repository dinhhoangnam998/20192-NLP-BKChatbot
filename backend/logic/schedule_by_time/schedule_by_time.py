import sys
# sys.path.append('/home/hoangnam/Documents/code/xProjects/bkchatbot')

import json
from dateutil import parser

from backend.db import db
from backend.crawler import schedule_crawler
from backend.logic.schedule_by_time.schedule_utils import make_pretty_string
from backend.logic.schedule_by_time.schedule_filter import *


def get_response(sender_id, time_entities):
    if not time_entities: 
        return 'xin lỗi, bạn có thể cho tớ thời gian cụ thể hơn được không?'

    with open(r'/home/hoangnam/Documents/code/xProjects/bkchatbot/backend/logic/debug/time_entities.json', 'a') as f:
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

        if(check_out_of_semester(time_entity)):
            schedule.append((text_extracted, [{'semester': None}]))
            continue

        type = time_entity['additional_info']['type']
        
        if type == 'value':
            grain = time_entity['additional_info']['grain']
            if grain == 'day':
                sub_schedule = filter_by_weekday(schedule_table, time_entity)
            elif grain == 'hour':
                sub_schedule = filter_by_hour(schedule_table, time_entity)
            elif grain == 'week':
                sub_schedule = filter_by_week(schedule_table, time_entity)
            elif grain == 'month':
                sub_schedule = filter_by_month(schedule_table, time_entity)
            elif grain == 'year':
                sub_schedule = filter_by_year(schedule_table, time_entity)
        
        elif type == 'interval':
            grain = time_entity['additional_info']['from']['grain']
            if grain == 'hour':
                sub_schedule = filter_by_session(schedule_table, time_entity)
            elif grain == 'week':
                sub_schedule = filter_by_multi_week(schedule_table, time_entity)
            elif grain == 'month':
                sub_schedule = filter_by_multi_month(schedule_table, time_entity)

        schedule.append((text_extracted, sub_schedule))

    return schedule



# time_entities = [ { "start": 0, "end": 9, "text": "t\u1ed1i th\u1ee9 2", "value": { "to": "2020-06-09T00:00:00.000+07:00", "from": "2020-06-08T18:00:00.000+07:00" }, "confidence": 1.0, "additional_info": { "values": [ { "to": { "value": "2020-06-09T00:00:00.000+07:00", "grain": "hour" }, "from": { "value": "2020-06-08T18:00:00.000+07:00", "grain": "hour" }, "type": "interval" }, { "to": { "value": "2020-06-16T00:00:00.000+07:00", "grain": "hour" }, "from": { "value": "2020-06-15T18:00:00.000+07:00", "grain": "hour" }, "type": "interval" }, { "to": { "value": "2020-06-23T00:00:00.000+07:00", "grain": "hour" }, "from": { "value": "2020-06-22T18:00:00.000+07:00", "grain": "hour" }, "type": "interval" } ], "to": { "value": "2020-06-09T00:00:00.000+07:00", "grain": "hour" }, "from": { "value": "2020-06-08T18:00:00.000+07:00", "grain": "hour" }, "type": "interval" }, "entity": "time", "extractor": "DucklingHTTPExtractor" } ]
# print(get_response('2591237020976102', time_entities))
