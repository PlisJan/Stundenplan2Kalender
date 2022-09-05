from bs4 import BeautifulSoup


def getTeacher(session, baseUrl):

    teacherDict = {}

    lehrerListe = session.get(
        f"{baseUrl}/lehrerliste.php")

    soup = BeautifulSoup(lehrerListe.content, "html.parser")

    teachers = soup.find_all(class_=["zeile_u", "zeile_g"])

    for teacher in teachers:
        data = teacher.findChildren("td")
        teacherDict[data[0].text] = data[1].text

    return teacherDict
