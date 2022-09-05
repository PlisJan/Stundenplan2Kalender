import re
from datetime import date, datetime, timedelta
from uuid import uuid4
from getpass import getpass

import pytz
from bs4 import BeautifulSoup
from dateutil.relativedelta import MO, relativedelta
from icalendar import Calendar, Event

from getTeacher import getTeacher
from login import createLoggedInSession

BASE_URL = input("Url: ")
USERNAME = input("Benutzername: ")
PASSWORD = getpass("Passwort: ")

lessonLength = input("Stundenlänge in min (Standard: 45): ")

if lessonLength == "":
    lessonLength = 45


class Subject:
    teacher: str
    subjectName: str
    room: str

    def __init__(self, subjectName, teacher, room):
        self.teacher = teacher
        self.subjectName = subjectName
        self.room = room

    def __str__(self):
        return f"Subject: {self.subjectName}, Teacher: {self.teacher}, Room: {self.room}"


session = createLoggedInSession(
    BASE_URL, USERNAME, PASSWORD)


teacherDict = getTeacher(session, BASE_URL)

stundenplan = session.get(BASE_URL+"/stdplan.php")


soup = BeautifulSoup(stundenplan.content, "html.parser")

lessons = soup.find_all(class_="stdplan-stunde-zeit")

lessonsList = []
for lesson in lessons:
    lessonsList.append([int(v) for v in lesson.text.split(":")])

subjects = soup.find_all(class_=["stdplan-eintrag", "stdplan-empty-eintrag"])

today = date.today()
thisMonday: date = today + relativedelta(weekday=MO(0))


cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//Stundenplan2Kalendar//plisjan03.github.io//')

i = -1

for subject in subjects:
    i += 1
    if ("stdplan-empty-eintrag" in subject.attrs.get("class")):
        # print("Empty Lesson")
        pass
    else:
        event = Event()
        children = subject.findChildren("span")

        splittedData = children[1].text.strip().split("\n")

        newSubj = Subject(re.sub(r"[\n \r]", "", children[0].text),
                          re.sub(r"[\n \r]", "", splittedData[0]),
                          re.sub(r"[\n \r]", "", splittedData[1])
                          )
        timeinfo = lessonsList[int(i/5)]

        event.add('name', newSubj.subjectName)
        event.add('summary', newSubj.subjectName)
        event.add('description', teacherDict.get(
            newSubj.teacher) or newSubj.teacher)
        event.add('dtstart', datetime(thisMonday.year,
                                      thisMonday.month,
                                      thisMonday.day,
                                      timeinfo[0],
                                      timeinfo[1],
                                      0)+timedelta(days=i % 5))
        event.add('dtend', datetime(thisMonday.year,
                                    thisMonday.month,
                                    thisMonday.day,
                                    timeinfo[0],
                                    timeinfo[1],
                                    0)+timedelta(days=i % 5, minutes=lessonLength))
        event.add('dtstamp', datetime.now())
        event.add('location', newSubj.room)
        event.add("uid", uuid4())
        event.add('rrule', {'FREQ': "weekly",
                  'UNTIL': datetime.today()+timedelta(days=323)})
        cal.add_component(event)

f = open("out.ics", "wb")
f.write(cal.to_ical())
f.close()
