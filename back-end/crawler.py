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


print(get_schedule(20162793))