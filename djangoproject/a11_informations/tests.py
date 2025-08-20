import pytest
from datetime import time
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from a11_informations.models import WorkTimesStandard, MailReciever

#-------------------------------------------------------------------------

@pytest.mark.django_db
def test_workhours_overview_get(workhours):
    client = Client()
    url = reverse("worktimes_overview")
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["workhours"].count() == len(workhours)
    for i in workhours:
        assert i in response.context["workhours"]

#-------------------------------------------------------------------------

@pytest.mark.parametrize("s,d,w,b", [
    ("DE", "6 hours", time(6,00,0), time(0,15,0)),
    ("DE", "8 hours", time(8,00,0), time(0,30,0)),
    ("DE", "10 hours", time(10,00,0), time(0,45,0)),
    ("PL", "6 hours", time(6,00,0), time(0,00,0)),
    ("PL", "8 hours", time(8,00,0), time(0,15,0)),
    ("PL", "10 hours", time(10,00,0), time(0,30,0)),
])
@pytest.mark.django_db
def test_workhours_overview_post(s,d,w,b):
    client = Client()
    data = {"srccode" : s,
            "description" : d,
            "workTime" : w,
            "breakTime" : b}
    url = reverse("worktimes_overview")
    response = client.post(path= url, data= data)

    assert response.status_code == 302
    assert WorkTime_db.objects.get(**data)

#-------------------------------------------------------------------------
