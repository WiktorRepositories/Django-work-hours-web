from typing import Any
from django import forms
from django.contrib.auth.models import User
from a11_informations.models import WorkTimesStandard
from a20_users.models import ProjectMachines, NetzplanVorgang

class FormWorktimeEntry(forms.Form):#{
    date = forms.DateField(required= False)

    travel_start = forms.TimeField(required= False)
    travel_end = forms.TimeField(required= False, widget= forms.TimeInput(attrs= {"cols" : 5, "rows" :1}))

    work_start = forms.TimeField(required= False, widget= forms.TimeInput(attrs= {"cols" : 5, "rows" :1})) 
    work_end = forms.TimeField(required= False, widget= forms.TimeInput(attrs= {"cols" : 5, "rows" :1}))

    worktimes_standard = forms.ModelChoiceField(queryset= WorkTimesStandard.objects.all(), required= False)

    project_machine = forms.ModelChoiceField(queryset= ProjectMachines.objects.all(), required= False)
    netzplan_vorgang = forms.ModelChoiceField(queryset= NetzplanVorgang.objects.all(), required= False)
#}

class FormAdminWorktimeEntry(forms.Form):#{
    user = forms.ModelChoiceField(queryset= User.objects.all(), required= False)

    date = forms.DateField(required= False)

    travel_start = forms.TimeField(required= False)
    travel_end = forms.TimeField(required= False, widget= forms.TimeInput(attrs= {"cols" : 5, "rows" :1}))

    work_start = forms.TimeField(required= False, widget= forms.TimeInput(attrs= {"cols" : 5, "rows" :1})) 
    work_end = forms.TimeField(required= False, widget= forms.TimeInput(attrs= {"cols" : 5, "rows" :1}))

    worktimes_standard = forms.ModelChoiceField(queryset= WorkTimesStandard.objects.all(), required= False)

    project_machine = forms.ModelChoiceField(queryset= ProjectMachines.objects.all(), required= False)
    netzplan_vorgang = forms.ModelChoiceField(queryset= NetzplanVorgang.objects.all(), required= False)
    #}
    def clean(self) -> dict[str, Any] | None:#{
        cleaned_data:dict = super().clean() # type: ignore

        tuser = cleaned_data.get("user")
        tdate = cleaned_data.get("date")

        tworktimes_standard = cleaned_data.get("worktimes_standard")
        tproject_machine = cleaned_data.get("project_machine")
        tnetzplan_vorgang = cleaned_data.get("netzplan_vorgang")

        if not tuser:
            raise forms.ValidationError("User is not choisen")

        if not tdate:
            raise forms.ValidationError("Date is not choisen")
    
        if not tworktimes_standard:
            raise forms.ValidationError("Worktimes standard is not choisen")
        
        if not tproject_machine:
            raise forms.ValidationError("Project and machine is not choisen")
        
        if not tnetzplan_vorgang:
            raise forms.ValidationError("Netzplan and vorgang is not choisen")
        
        return cleaned_data
    #}

