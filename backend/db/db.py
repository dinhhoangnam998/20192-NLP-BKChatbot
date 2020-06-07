import json
from backend.crawler import calender_crawler 

# sender_id_to_sid = {'2591237020976102': '20162793', '1756189307838190': '20161925', '2643352335766377': '20161925'}
sender_id_to_sid = {}
sid_to_schedule_table = {}

# sid
def has_sid(sender_id):
    return sender_id in sender_id_to_sid

def set_sid(sender_id, sid):
    global sender_id_to_sid
    sender_id_to_sid[sender_id] = sid

def get_sid(sender_id):
    return sender_id_to_sid[sender_id]

# schedule
def has_schedule_table(sid):
    if sid not in sid_to_schedule_table:
        return False

    semester_now = calender_crawler.crawl_callender()[0]
    semester_of_schedule = sid_to_schedule_table[sid][0]['semester']
    return semester_of_schedule == semester_now

def set_schedule_table(sid, schedule_table):
    global sid_to_schedule_table
    sid_to_schedule_table[sid] = schedule_table

def get_schedule_table(sid):
    return sid_to_schedule_table[sid]

# save & load
def save_sender_id_to_sid():
    with open('sender_id_to_sid.json', 'w') as f:
        json.dump(sender_id_to_sid, f)

def save_sid_to_schedule_table():
    with open('sid_to_schedule_table.json', 'w') as f:
        json.dump(sender_id_to_sid, f)

def load_sender_id_to_sid():
    global sender_id_to_sid
    with open('sender_id_to_sid.json') as f:
        sender_id_to_sid = json.load(f)

def load_sid_to_schedule_table():
    global sid_to_schedule_table
    with open('sid_to_schedule_table.json') as f:
        sid_to_schedule_table = json.load(f)
