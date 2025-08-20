import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from a00_accounts.forms import FormRegisterUser, FormLoginView

# Create your tests here.
@pytest.mark.django_db
def test_register_user_get():
    client = Client()
    url = reverse("account_register")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_users_db_content(registered_users):
    users = User.objects.all()
    assert users.count() > 0
    assert len(registered_users) > 0
    assert len(registered_users) == users.count() 

@pytest.mark.parametrize("us, fn, ln, e1, e2, p1, p2", [
    ("Usser55", "Barney", "Calhoun", "barneycalhoun@blackmesa.com", "barneycalhoun@blackmesa.com", "BlackMesa123", "BlackMesa123"),
    ("User66", "Richard", "Keller", "richardkeller@blackmesa.com", "richardkeller@blackmesa.com", "BlackMesa123", "BlackMesa123"),
    ("User77", "Adrian", "Shephard", "adrianshepard@blackmesa.com", "adrianshepard@blackmesa.com", "BlackMesa123", "BlackMesa123"),
    ("User88", "Gina", "Cross", "ginacross@blackmesa.com", "ginacross@blackmesa.com", "BlackMesa123", "BlackMesa123")
])
@pytest.mark.django_db
def test_register_user_post_valid(registered_users, us, fn, ln, e1, e2, p1, p2):
    data = {"username" : us, 
    "first_name" : fn, 
    "last_name" : ln, 
    "email1" : e1,
    "email2" : e2,
    "password1" : p1,
    "password2" : p2}

    client = Client()
    url = reverse("account_register")
    response = client.post(path= url, data= data)

    assert response.status_code == 302
    assert User.objects.get(username= us)
    user = User.objects.get(username= us)
    assert user.username == us

# @pytest.mark.django_db
# def test_register_user_post_invalid():
#     assert True

# @pytest.mark.django_db
# def test_view_user_login_get():
#     client = Client()
#     url = reverse("account_login")
#     response = client.get(path= url)

#     assert response.status_code == 200

@pytest.mark.parametrize("us, pa", [
    ("User11", "password1234"),
    ("User22", "password1234"),
    ("User33", "password1234"),
    ("User44", "password1234")
])
@pytest.mark.django_db
def test_view_user_login_post(registered_users, us, pa):
    client = Client()
    url = reverse("account_login")
    response = client.post(url, data={"username" : us, "password" : pa})

    try: 
        assert response.context["error"] == []
    except TypeError:
        assert True

    assert response.status_code == 302 # Error if form.is_valid():