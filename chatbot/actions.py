# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
import lxml.html

def get_schedule(student_id):
    url = "http://sis.hust.edu.vn/ModulePlans/Timetables.aspx"
    form = {'__EVENTTARGET': '', 'ctl00$MainContent$Studentid': f'{student_id}', 'ctl00$MainContent$btFind': ''}
    response = requests.post(url, data=form)

    schedule_table = {}

    if response.status_code == 200:
        doc = lxml.html.fromstring(response.text)
        table_elements = doc.xpath(
            '//table[@id="MainContent_gvStudentRegister_DXMainTable"]')[0]
        tr_elements = table_elements.xpath(
            './/tr[@class="dxgvDataRow_SisTheme"]')

        for tr in tr_elements:
            time = tr[0].text_content().strip()
            weeks = tr[1].text_content().strip()
            classroom = tr[2].text_content().strip()
            class_code = tr[3].text_content().strip()
            class_type = tr[4].text_content().strip()
            group = tr[5].text_content().strip()
            subject_code = tr[6].text_content().strip()
            subject_name = tr[7].text_content().strip()
            note = tr[8].text_content().strip()

            day_of_week = start_time = end_time = ''
            if time:
                day_of_week = time.split(',')[0].split(' ')[1].strip()
                start_time = time.split(',')[1].split('-')[0].strip()
                end_time = time.split(',')[1].split('-')[1].strip()

            week_A_start = int(weeks.split(',')[0].split('-')[0])
            week_A_end = int(weeks.split(',')[0].split('-')[1])
            week_B_start = int(weeks.split(',')[1].split('-')[0])
            week_B_end = int(weeks.split(',')[1].split('-')[1])
            weeks = list(range(week_A_start, week_A_end + 1))
            weeks.extend(list(range(week_B_start, week_B_end + 1)))

            subject_schedule = dict(day_of_week=day_of_week, start_time=start_time, end_time=end_time, weeks=weeks, classroom=classroom, class_code=class_code, class_type=class_type, group=group, subject_code=subject_code, subject_name=subject_name, note=note)
            schedule_table[subject_name] =  subject_schedule
        return schedule_table

import pytz
import datetime
import re

REGEX_DATE = r"(3[01]|[12][0-9]|0?[1-9])[-\/:|](1[0-2]|0?[1-9])([-\/:|](2[0-1][0-9][0-9]))"
REGEX_DAY_MONTH = r"(3[01]|[12][0-9]|0?[1-9])[-\/:|](1[0-2]|0?[1-9])"
REGEX_MONTH_YEAR = r"(1[0-2]|0?[1-9])([-\/:|](2[0-1][0-9][0-9]))"

def regex_date(msg, timezone="Asia/Ho_Chi_Minh"):
    ''' use regex to capture date string format '''

    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz=tz)

    date_str = []
    regex = REGEX_DATE
    regex_day_month = REGEX_DAY_MONTH
    regex_month_year = REGEX_MONTH_YEAR
    pattern = re.compile("(%s|%s|%s)" % (
        regex, regex_month_year, regex_day_month), re.UNICODE)

    matches = pattern.finditer(msg)
    for match in matches:
        _dt = match.group(0)
        _dt = _dt.replace("/", "-").replace("|", "-").replace(":", "-")
        for i in range(len(_dt.split("-"))):
            if len(_dt.split("-")[i]) == 1:
                _dt = _dt.replace(_dt.split("-")[i], "0"+_dt.split("-")[i])
        if len(_dt.split("-")) == 2:
            pos1 = _dt.split("-")[0]
            pos2 = _dt.split("-")[1]
            if 0 < int(pos1) < 32 and 0 < int(pos2) < 13:
                _dt = pos1+"-"+pos2+"-"+str(now.year)
        date_str.append(_dt)
    return date_str



def sender2student(sender_id):
    # TODO: just hardcode for now
    student_id = 20162793
    return student_id

def get_schedule_for_weekday(weekday, schedule_table):
    schedule = []
    for k,v in schedule_table.items():
        print('weekday +2:' , weekday + 2)
        if int(v['day_of_week']) == weekday + 2:
            schedule.append(str(v))
    return schedule


def get_response_msg(sender_id, msg):
    student_id = sender2student(sender_id)
    schedule_table = get_schedule(student_id)
    date_str = regex_date(msg)[0]
    weekday = datetime.datetime.strptime(date_str, '%d-%m-%Y').weekday()
    schedule = get_schedule_for_weekday(weekday, schedule_table)
    response = "".join(schedule)
    return response

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

class ActionShowSchedule(Action):

    def name(self) -> Text:
        return "action_show_schedule"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender_id = tracker.sender_id
        message = tracker.latest_message.get('text')
        response = get_response_msg(sender_id, message)
        dispatcher.utter_message(text=response)
        return []