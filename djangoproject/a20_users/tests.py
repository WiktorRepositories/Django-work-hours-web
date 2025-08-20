import pytest
from datetime import time
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.urls import reverse

# Create your tests here.

@pytest.mark.django_db
def test_view_user_cooperation_get(registered_users):
    client = Client()
    # user = User.objects.create(username= "User11", password= "password1234")
    client.login(username= "User11", password= "password1234")
    url = reverse("user_connections_overview")
    response = client.get(url)
    
    assert response.status_code == 200