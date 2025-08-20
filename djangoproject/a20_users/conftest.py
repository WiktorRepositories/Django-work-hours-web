import pytest
from datetime import time
from django.contrib.contenttypes.models import ContentType
from a00_accounts.models import User
from a20_users.models import UserSettings, UsersWorkTimes

@pytest.fixture()
def registered_users():
    users = []

    kwargs = {"username" : "User11", 
    "first_name" : "Jhon", 
    "last_name" : "Conor", 
    "email" : "jhonconor@gmail.com"}
    user1 = User.objects.create(**kwargs)
    user1.set_password("password1234")
    user1.save()
    users.append(user1)

    kwargs = {"username" : "User22", 
    "first_name" : "Army", 
    "last_name" : "Black", 
    "email" : "armyblack@gmail.com"}
    user2 = User.objects.create(**kwargs)
    user2.set_password("password1234")
    user2.save()
    users.append(user2)

    kwargs = {"username" : "User33", 
    "first_name" : "Annie", 
    "last_name" : "Tomson", 
    "email" : "annietomson@gmail.com"}
    user3 = User.objects.create(**kwargs)
    user3.set_password("password1234")
    user3.save()
    users.append(user3)

    kwargs = {"username" : "User44", 
    "first_name" : "Aron", 
    "last_name" : "Nowak", 
    "email" : "aronnowak@gmail.com"}
    user4 = User.objects.create(**kwargs)
    user4.set_password("password1234")
    user4.save()
    users.append(user4)

    return users    