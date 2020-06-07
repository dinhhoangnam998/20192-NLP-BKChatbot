from dateutil import parser

from backend.crawler import calender_crawler
from backend.logic.schedule_by_time.schedule_utils import get_weeks_of_subject
from backend.logic.schedule_by_time.schedule_utils import get_time_str


# e.g. hôm nay, hôm qua, ngày mai, thứ 2, thứ tư, chủ nhật, thứ năm tuần trước, thứ bảy tuần này, 04-06-2020, 10/06/2020 ....
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


# e.g. sáng mai, tối hôm qua, chiều hôm nay, sáng thứ 4 tuần này, chiều thứ 5 tuần sau, ....
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
        schedule.append(subject)
    return schedule
        

# e.g. 9 giờ sáng mai,  7 giờ tối hôm qua, 4 giờ chiều thứ 2, ....
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


# e.g. tuần sau, tuần trước, tuần này, ....
def filter_by_week(schedule_table, time_entity):
    schedule = []
    for row in schedule_table:
        weeks_of_subject = get_weeks_of_subject(row)
        week_now = int(calender_crawler.crawl_callender()[1])
        if week_now in weeks_of_subject:
            schedule.append(row)
    return schedule


# e.g. tháng 3, tháng sau, tháng trước ....
def filter_by_month(schedule_table, time_entity):
    return schedule_table


def filter_by_year(schedule_table, time_entity):
    return schedule_table


def filter_by_multi_week(schedule_table, time_entity):
    return schedule_table


def filter_by_multi_month(schedule_table, time_entity):
    return schedule_table

