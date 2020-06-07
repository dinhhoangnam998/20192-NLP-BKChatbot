import re

from backend.db import db
from backend.crawler import schedule_crawler
from .levenshtein import get_similarity

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
    rows = set()
    for row in schedule_table:
        if row['subject_name'] in msg:
            rows.add(row)
    
    list_regex = re.findall(r'\"(.*?)\"', msg)
    best_similarity = 0.5
    for regex in list_regex:
        best = None
        for row in schedule_table:
            similar = get_similarity(regex, row['subject_name'])
            if similar > best_similarity:
                best_similarity = similar
                best = row
        if best:
            rows.add(row)
    
    return list(rows)
