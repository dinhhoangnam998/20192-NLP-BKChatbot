import sys
# sys.path.append(r'C:\Users\HoangNam\Documents\Code\xProject\20192-NLP-BTL-BKChatbot')
# sys.path.append('/home/hoangnam/Documents/code/xProjects/bkchatbot')
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
    if not rows:
        response = "Không tìm thấy thông tin nào về môn học đó trong thời khóa biểu của bạn! 🧐 "
    for row in rows:
        response += "|".join([row['semester'], row['time'], row['classroom'], row['subject_name']]) + '\n'

    return response


def get_match_rows(schedule_table, msg):
    list_regex = re.findall(r'\"(.*?)\"', msg)
    cleaned_msg = clean_string(msg)
    rows = []

    for row in schedule_table:
        subject_name = row['subject_name'].lower()
        if subject_name in cleaned_msg:
            rows.append(row)
        else:
            for regex in list_regex:
                similar = get_similarity(regex, subject_name)
                if similar >= 0.5:
                    rows.append(row)
    
    return rows

# get_response('2591237020976102', 'cho xin lịch học môn "Khai phá Web" bot ơi')