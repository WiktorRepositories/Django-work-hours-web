from typing import Any
from django import forms
from django.contrib.auth.models import User
from a00_accounts.models import Cooperation, ProjectMachines

#----------------------------------------------------------------------------------------------
#
class FormCooperation(forms.ModelForm):
    class Meta:#{
        model = Cooperation
        fields = ("description", "users", "projects")
    #}
    description = forms.CharField(max_length= 32, required= True)
    users = forms.ModelMultipleChoiceField(queryset= User.objects.exclude(username= "admin"), required= True)
    projects = forms.ModelMultipleChoiceField(queryset= ProjectMachines.objects.all(), required= True)

    def clean(self) -> dict[str, Any] | None:
        cleaned_data:dict = super().clean() # type: ignore
#==============================================================================================

#----------------------------------------------------------------------------------------------
#
class FormRegisterUser(forms.ModelForm):#{
    class Meta:#{
        model = User
        fields = ("username","first_name", "last_name", "email1", "email2", "password1", "password2")
    #}
    first_name = forms.CharField(max_length= 16)
    last_name = forms.CharField(max_length= 16)

    email1 = forms.EmailField(max_length= 32)
    email2 = forms.EmailField(max_length= 32)

    password1 = forms.CharField(widget= forms.PasswordInput)
    password2 = forms.CharField(widget= forms.PasswordInput)
    
    def clean(self):#{
        cleaned_data:dict = super().clean() # type: ignore

        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        email1 = cleaned_data.get("email1")
        email2 = cleaned_data.get("email2")
        
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if first_name == last_name:
            raise forms.ValidationError("Name and surname same!")
        if email1 != email2:
            raise forms.ValidationError("Both emails not the same!")
        if password1 != password2:
            raise forms.ValidationError("Both passwords not the same!")
        
        return cleaned_data
    #}
        

#}
#==============================================================================================

#----------------------------------------------------------------------------------------------
#       
class FormLoginView(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
#==============================================================================================
