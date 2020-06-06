import json
from backend.crawler.calender_crawler import get_callender

fbid2sid = {'2591237020976102': '20162793'}
sid2schedule = {}

# sid
def has_sid(fbid):
    return fbid in fbid2sid

def set_sid(fbid, sid):
    global fbid2sid
    fbid2sid[fbid] = sid

def get_sid(fbid):
    return fbid2sid[fbid]

# schedule
def has_schedule(sid):
    return (sid in sid2schedule)
    #  and (list(sid2schedule[sid].values)[0]['semester'] == get_callender()[0])

def set_schedule(sid, schedule):
    global sid2schedule
    sid2schedule[sid] = schedule

def get_schedule(sid):
    return sid2schedule[sid]

# save & load
def save_fbid2sid():
    with open('fbid2sid.json', 'w') as f:
        json.dump(fbid2sid, f)

def save_sid2schedule():
    with open('sid2schedule.json', 'w') as f:
        json.dump(fbid2sid, f)

def load_fbid2sid():
    global fbid2sid
    with open('fbid2sid.json') as f:
        fbid2sid = json.load(f)

def load_sid2schedule():
    global sid2schedule
    with open('sid2schedule.json') as f:
        sid2schedule = json.load(f)
