import pytest
from datetime import time
from django.contrib.contenttypes.models import ContentType
from a11_informations.models import MailReciever_db, WorkTime_db

@pytest.fixture()
def emails():
    listMails = []
    for i in range(4):
        srccode = f"AA{i}"
        email = f"BB{i}@valve.com"
        firstN = f"CC{i}"
        lastN = f"DD{i}"
        description = f"EE{i}"
        listMails.append(MailReciever_db.objects.create(srccode=srccode, email=email, firstName=firstN, lastName=lastN, description=description))
    return listMails

@pytest.fixture()
def workhours():
    listWorkhours = []
    for i in range(4):
        srccode = f"A{i}"
        description = f"B{i}"
        workTime = time(8+i, 0, 0)
        breakTime = time(0, 30+i, 0)
        listWorkhours.append(WorkTime_db.objects.create(srccode= srccode, description= description, workTime= workTime, breakTime= breakTime))
    return listWorkhours