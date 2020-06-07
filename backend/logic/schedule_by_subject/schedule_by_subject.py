import sys
sys.path.append('/home/hoangnam/Documents/code/xProjects/bkchatbot')
import re

from backend.db import db
from backend.crawler import schedule_crawler
from backend.logic.schedule_by_subject.levenshtein import get_similarity
from backend.logic.schedule_by_subject.levenshtein import clean_string

def get_response(sender_id, msg):
    sid = db.get_sid(sender_id)

    if not db.has_schedule_table(sid):
        db.set_schedule_table(sid, schedule_crawler.crawl_schedule_table(sid))

    rows = get_match_rows(db.get_schedule_table(sid), msg)

    response = ''
    for row in rows:
        response += "|".join([row['semester'], row['time'], row['classroom'], row['subject_name']]) + '\n'

    return response


def get_match_rows(schedule_table, msg):
    cleaned_msg = clean_string(msg)
    rows = []
    for row in schedule_table:
        subject_name = row['subject_name'].lower()
        if subject_name in cleaned_msg:
            rows.append(row)
    
    list_regex = re.findall(r'\"(.*?)\"', msg)
    for regex in list_regex:
        best_similarity = 0.5
        best = None
        for row in schedule_table:
            similar = get_similarity(regex, row['subject_name'])
            if similar > best_similarity:
                best_similarity = similar
                best = row
        if best:
            rows.append(best)
    
    return rows

get_response('2591237020976102', 'cho xin lịch học môn "Khai phá Web" bot ơi')