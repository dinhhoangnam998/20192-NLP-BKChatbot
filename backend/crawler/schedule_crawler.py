import requests
import lxml.html

def crawl_schedule_table(student_id):
    url = "http://sis.hust.edu.vn/ModulePlans/Timetables.aspx"
    form = {'__EVENTTARGET': '', 'ctl00$MainContent$Studentid': f'{student_id}', 'ctl00$MainContent$btFind': ''}
    response = requests.post(url, data=form)

    schedule_table = []
    
    if response.status_code == 200:
        doc = lxml.html.fromstring(response.text)

        callender_element = doc.xpath('//span[@id="statisticMember_StatusTextLabel"]')[0]
        semester = callender_element.text_content().split(',')[0].split(' ')[2]
        # week = callender_element.text_content().split(',')[1].split(' ')[2]

        table_elements = doc.xpath('//table[@id="MainContent_gvStudentRegister_DXMainTable"]')[0]
        tr_elements = table_elements.xpath('.//tr[@class="dxgvDataRow_SisTheme"]')

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

            subject_schedule = dict(semester=semester, time=time, weeks=weeks, classroom=classroom, class_code=class_code, class_type=class_type, group=group, subject_code=subject_code, subject_name=subject_name, note=note)
            schedule_table.append(subject_schedule)

        return schedule_table

