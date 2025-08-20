import pytest
from django.test import Client
from django.urls import reverse

@pytest.mark.django_db
def test_main_page():
    cli = Client()
    url = "/"
    responde = cli.get(url)
    assert responde.status_code == 200