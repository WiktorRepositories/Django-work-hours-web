from typing import Any
from django import forms
from django.utils.safestring import SafeString
from a11_informations.models import Countries_ISO3166

#********************************************************************************************
# Form to enter data for countries 
class FormCountriesISO(forms.Form):#{
    name = forms.CharField(max_length= 16)
    stateName = forms.CharField(max_length= 32)
    sovereign = forms.ModelChoiceField(queryset= Countries_ISO3166.objects.all(), required= False)
    a2 = forms.CharField(max_length= 2)
    a3 = forms.CharField(max_length= 3)
    numb = forms.CharField(max_length= 3)
    #}
    
    def clean(self) -> dict[str, Any] | None:#{
        cleaned_data:dict = super().clean() # type: ignore
        
        a2:str = cleaned_data.get("a2", "")
        a3:str = cleaned_data.get("a3", "")
        
        cleaned_data["a2"] = a2.upper()
        cleaned_data["a3"] = a3.upper()
        
        return cleaned_data
    #}
#============================================================================================

#********************************************************************************************
# 

#============================================================================================