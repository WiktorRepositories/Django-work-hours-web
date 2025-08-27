from datetime import time
from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from a11_informations.models import MailReciever, WorkTimesStandard, Countries_ISO3166
from a11_informations.forms import FormCountriesISO

#===============================================================================================================================
A11_ERROR_HTML = "a11_error_info.html"
#===============================================================================================================================

class ViewMails_overview(View):#{
    URL_NAME = "mails_overview"
    HTML_NAME = "mails_overview.html"

    def get(self, request:HttpRequest):#{
        query_set = MailReciever.objects.all()
        context = {"mails" : query_set}
        return render(request= request, template_name= self.HTML_NAME, context= context)
    #}
    def post(self, request:HttpRequest):#{
        email = request.POST.get("email", "")
        firstName = request.POST.get("firstName", "")
        lastName = request.POST.get("lastName", "")
        description = request.POST.get("description", "")
        
        if email and firstName and lastName and description:#[
            short_name = f"{firstName[0:2]}{lastName[0:2]}"
            MailReciever.objects.create(short_name=short_name, email=email, firstName=firstName, lastName=lastName, description=description)
            return HttpResponseRedirect(reverse(self.URL_NAME))
        #]
        else:
            error = f"Not complete input email data error:\nEmail:{email}, Firstname{firstName}, Lastname{lastName}, Description{description}"
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error" : error})
    #}
#--------------------------------------------------------
class ViewMail_delete(View):
    HTML_NAME = "mail_delete.html"

    def get(self, request:HttpRequest, id:int):#{
        try:
            mail = MailReciever.objects.get(pk= id)
        except MailReciever.DoesNotExist:
            error = f"Main reciever does not exist!, id={id}"
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error" : error})
        else:
            return render(request= request, template_name= self.HTML_NAME, context= {"mail" : mail})
    #}
    def post(self, request:HttpRequest, id:int):#{
        operation = request.POST.get("operation", "")
        
        if operation == "delete":
            mail = MailReciever.objects.get(pk=id)
            mail.delete()
            return HttpResponseRedirect(reverse(ViewMails_overview.URL_NAME))
        elif operation == "cancel":
            return HttpResponseRedirect(reverse(ViewMails_overview.URL_NAME))
        else:
            error = f"Input form non delete, non cancel."
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error" : error})
    #}
#--------------------------------------------------------
class ViewMail_modify(View):
    HTML_NAME = "mail_modify.html"

    def get(self, request:HttpRequest, id:int):#{
        try:
            mail = MailReciever.objects.get(pk= id)
        except MailReciever.DoesNotExist:
            error = f"Main reciever does not exist!, id={id}"
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error" : error})
        else:
            return render(request= request, template_name= self.HTML_NAME, context= {"mail" : mail})
    #}
    def post(self, request:HttpRequest, id:int):#{
        email = request.POST.get("email", "")
        firstName = request.POST.get("firstName", "")
        lastName = request.POST.get("lastName", "")
        description = request.POST.get("description", "")

        if email or firstName or lastName or description:#{
            mail = MailReciever.objects.get(pk=id)
            short_name = f"{firstName[0:2]}{lastName[0:2]}"
            if short_name:
                mail.short_name = short_name
            if email:
                mail.email = email
            if firstName:
                mail.firstName = firstName
            if lastName:
                mail.lastName = lastName
            if description:
                mail.description
            mail.save()
        return HttpResponseRedirect(reverse(ViewMails_overview.URL_NAME))
    #}
#===============================================================================================================================

class ViewWorktimes_overview(View):
    HTML_NAME = "worktimes_overview.html"
    URL_NAME = "worktimes_overview"

    def get(self, request:HttpRequest):#{
        query_set = WorkTimesStandard.objects.all()
        context = {"worktimes" : query_set}
        return render(request= request, template_name= self.HTML_NAME, context= context)
    #}
    def post(self, request:HttpRequest):#{
        country = request.POST.get("country", "")
        description = request.POST.get("description", "")
        workTime = request.POST.get("workTime", "")
        breakTime = request.POST.get("breakTime", "")

        if country and description and workTime and breakTime:
            WorkTimesStandard.objects.create(country= country, description= description, workTime= workTime, breakTime= breakTime)
            return HttpResponseRedirect(reverse(self.URL_NAME))
        else:
            error = f"Not complete input work time standard:\nCuntry: {country}, Description: {description}, Worktime: {workTime}, Break {breakTime}"
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error" : error})
    #}
#--------------------------------------------------------
class ViewWorktime_delete(View):
    HTML_NAME = "worktime_delete.html"

    def get(self, request:HttpRequest, id:int):#{
        try:
            worktime = WorkTimesStandard.objects.get(pk= id)
        except WorkTimesStandard.DoesNotExist:
            worktime = None
        return render(request= request, template_name= self.HTML_NAME, context= {"worktime" : worktime})
    #}
    def post(self, request:HttpRequest, id:int):#{
        operation = request.POST.get("operation")
        if operation == "delete":
            worktime = WorkTimesStandard.objects.get(pk= id)
            worktime.delete()
            return HttpResponseRedirect(reverse(ViewWorktimes_overview.URL_NAME))
        elif operation == "cancel":
            return HttpResponseRedirect(reverse(ViewWorktimes_overview.URL_NAME))
        else:
            error = f"Input form non delete, non cancel."
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error" : error})
    #}
#--------------------------------------------------------
class ViewWorktime_modify(View):
    HTML_NAME = "worktime_modify.html"

    def get(self, request:HttpRequest, id:int):#{
        try:
            worktime = WorkTimesStandard.objects.get(pk= id)
        except WorkTimesStandard.DoesNotExist:
            error = f"Work times range standards does not exist!, id={id}!"
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error" : error})
        else:
            return render(request= request, template_name= self.HTML_NAME, context= {"worktime" : worktime})
    #}
    def post(self, request:HttpRequest, id:int):#{
        country = request.POST.get("country", "")
        description = request.POST.get("description", "")
        workTime = request.POST.get("workTime", "")
        breakTime = request.POST.get("breakTime", "")

        if country or description or workTime or breakTime:
            worktime = WorkTimesStandard.objects.get(pk= id)
            if country:
                worktime.country = country
            if description:
                worktime.description = description
            if workTime:
                worktime.workTime = workTime
            if breakTime:
                worktime.breakTime = breakTime
            worktime.save()
        return HttpResponseRedirect(reverse(ViewWorktimes_overview.URL_NAME))
    #}
#===============================================================================================================================

#-------------------------------------------------------------------------------------------------------------------------------
#
class ViewCountryISO_overview(View):
    HTML_FILE = "countries_overview.html"
    URL_LINK = "countries_overview"
    
    def get(self, request:HttpRequest):#{
        query_set = Countries_ISO3166.objects.all()
        form = FormCountriesISO()
        context = {"query_set" : query_set, "form":form}
        return render(request= request, template_name= self.HTML_FILE, context= context)
    #}
    def post(self, request:HttpRequest):#{
        form = FormCountriesISO(request.POST)
        if form.is_valid():#[
            name = form.cleaned_data.get("name", "")
            state = form.cleaned_data.get("stateName", "")
            a2 = form.cleaned_data.get("a2", "")
            a3 = form.cleaned_data.get("a3")
            numb = form.cleaned_data.get("numb", "")
            
            new_country = Countries_ISO3166.objects.create(name= name, stateName= state, A_2= a2, A_3= a3, num= numb)
            fk_country = form.cleaned_data["sovereign"]
            new_country.sovereign = fk_country
            new_country.save()
            return HttpResponseRedirect(reverse(self.URL_LINK))
        #]
        else:
            error = f"Error on input form data!"
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error":error, "form":form})
    #}
    
class ViewCountryISO_delete(View):
    HTML_FILE = "countries_delete.html"
    
    def get(self, request:HttpRequest, id:int):#{
        try:
            country = Countries_ISO3166.objects.get(pk= id);
        except Countries_ISO3166.DoesNotExist:
            error = f"This country does not exist!, id={id}!"
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error" : error})
        else:
            return render(request= request, template_name= self.HTML_FILE, context= {"country":country})
    #}
    def post(self, request:HttpRequest, id:int):#{
        operation = request.POST.get("operation")
        if operation == "delete":
            country = Countries_ISO3166.objects.get(pk= id)
            country.delete()
            return HttpResponseRedirect(reverse(ViewCountryISO_overview.URL_LINK))
        elif operation == "cancel":
            return HttpResponseRedirect(reverse(ViewCountryISO_overview.URL_LINK))
        else:
            error = f"Input form non delete, non cancel."
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error" : error})
    #}
    
class ViewCountryISO_modify(View):
    HTML_FILE = "countries_modify.html"
    
    def get(self, request:HttpRequest, id:int):#{
        try:
            country = Countries_ISO3166.objects.get(pk= id);
        except Countries_ISO3166.DoesNotExist:
            error = f"This country does not exist!, id={id}!"
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error" : error})
        else:
            default = {"name": country.name, "stateName":country.stateName, "a2":country.A_2, "a3":country.A_3, "numb":country.num}
            form = FormCountriesISO(default)
            return render(request= request, template_name= self.HTML_FILE, context= {"country":country, "form":form})
    #}
    def post(self, request:HttpRequest, id:int):#{
        form = FormCountriesISO(request.POST)
        if form.is_valid():#[
            country = Countries_ISO3166.objects.get(pk= id);
            if form.cleaned_data["name"]:
                country.name = form.cleaned_data["name"]
            if form.cleaned_data["stateName"]:
                country.stateName = form.cleaned_data["stateName"]
            if form.cleaned_data["sovereign"]:
                country.sovereign = form.cleaned_data["sovereign"]
            if form.cleaned_data["a2"]:
                country.A_2 = form.cleaned_data["a2"]
            if form.cleaned_data["a3"]:
                country.A_3 = form.cleaned_data["a3"]
            if form.cleaned_data["numb"]:
                country.num = form.cleaned_data["numb"]
            country.save()
            
            return HttpResponseRedirect(reverse(ViewCountryISO_overview.URL_LINK))
        #]
        else:
            error = f"Error on input form data!"
            return render(request= request, template_name= A11_ERROR_HTML, context= {"error":error, "form":form})
    #}
#===============================================================================================================================