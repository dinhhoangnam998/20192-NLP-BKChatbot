import requests
import lxml.html

def get_callender():
    url = "http://sis.hust.edu.vn"
    response = requests.get(url)
    if response.status_code == 200:
        doc = lxml.html.fromstring(response.text)
        callender_element = doc.xpath('//span[@id="statisticMember_StatusTextLabel"]')[0]
        semester = callender_element.text_content().split(',')[0].split(' ')[2]
        week = callender_element.text_content().split(',')[1].split(' ')[2]
        return (semester, week)

