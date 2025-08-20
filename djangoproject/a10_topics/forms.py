from django.db import models
from django import forms
from django.contrib.auth.models import User
from a10_topics.models import ProjectMachines
from a00_accounts.models import Cooperation

class FormShowPeopleInProject(forms.Form):
    machine_project = forms.ModelChoiceField(queryset= ProjectMachines.objects.all(), required= True)