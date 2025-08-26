from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from a00_accounts.models import Cooperation
from a20_users.models import UserSettings, UsersWorkTimes
from a20_users.forms import FormWorktimeEntry, FormAdminWorktimeEntry
from datetime import  date, timedelta, time
from mylib.timecalculations import isoformat_date

#======================================================================================================================
A20_ERROR_HTML = "a20_error_info.html"
#======================================================================================================================

#**********************************************************************************************************************
# Settings sotred inside data base
def _save_session_settings(settings:dict, session:dict):#{
    for key in settings:
        if (settings.get(key, None) != None) and (settings.get(key) != session.get(key)):
            session[key] = settings[key]
#}
def _save_last_input(current_input:dict, request:HttpRequest, key:str, ):#{
    if request.session.get(key, None):
        _save_session_settings(current_input, request.session[key])
    else:
        request.session[key] = current_input
    request.session.modified = True
#}
def _save_cookies(form_cleaned_data:dict, request:HttpRequest, form_names:list, key:str):#{
    current_entries = {}
    for key in form_names:
        val = form_cleaned_data[key]
        current_entries[key] = val.isoformat() if val else ""
    _save_last_input(current_entries, request, key)
#}
def _default_time()->tuple[date, date, int]:#{
    data_start = date.today()
    date_end = data_start + timedelta(days= 7)
    return data_start, date_end, 7
#}
def _save_view_settings(settings:dict, session:dict):#{
    for key in settings:
        if settings.get(key) and (settings.get(key) != session.get(key)):
            session[key] = settings[key]
#}
#======================================================================================================================

#**********************************************************************************************************************
# Settings sotred inside data base
class ViewLogedUserSettings(View):
    HTML_FILE = "user_settings.html"
    URL_LINK = "user_settings"
    
    def get(self, request:HttpRequest):#{
        user_settings = UserSettings.objects.get(user= request.user)
        context = {"usersettings" : user_settings}
        return render(request= request, template_name= self.HTML_FILE, context= context)
    #}
    def post(self, request:HttpRequest):#{
        datestart = isoformat_date(request.POST.get("date_start", ""))
        dateend = isoformat_date(request.POST.get("date_end", ""))
        weekdate = isoformat_date(request.POST.get("weeknum", ""))

        if (dateend and datestart) or weekdate:#[
            user_settings = UserSettings.objects.get(user_id= request.user)

            if weekdate:#[
                user_settings.weekSelected = weekdate
            #]
            if (dateend and datestart) and (datestart <= dateend):#[
                user_settings.rangeStart = datestart
                user_settings.rangeEnd = dateend
            #]  
            user_settings.save()
            return HttpResponseRedirect(reverse(self.URL_LINK)) 
        #]
        else:
            error = f"Error: data input empty! ({datestart} && {dateend}) || {weekdate}"
            return render(request= request, template_name= A20_ERROR_HTML, context= {"error" : error})
    #}
#======================================================================================================================

#**********************************************************************************************************************
# View loged user cooperation on some projects
def view_user_cooperation_get(request:HttpRequest):#{
    query_set = Cooperation.objects.filter(users= request.user)
    dict_query_set = []
    for c in query_set:
        description = c.description
        users = [str(i) for i in c.users.all()]
        projects = [str(i) for i in c.projects.all()]
        description = c.description
        dict_query_set.append({"pk" : c.pk,"description" : description, "users" : users, "projects" : projects})
    context = {"cooperations" : dict_query_set}
    return render(request= request, template_name="user_connections_overview.html", context= context)
#}
#======================================================================================================================

#**********************************************************************************************************************
# 
class ViewUserWeek_overview(View):
    HTML_FILE = "week_overview_grouby_v2.html"
    URL_LINK = "week_overview_grouby"
    
    @staticmethod
    def _create_isostring_list(datestart:date, days:int)->list[str]:#{
        date_list = []
        for i in range(days):
            date_list.append(datestart)
            datestart += timedelta(days= 1)
        return date_list
    #}
    def get(self, request:HttpRequest):#{
        settings:dict = request.session["VIEW_SETTINGS"]
        date_start:date = date.fromisoformat(settings["date_start"])
        date_end:date = date.fromisoformat(settings["date_end"])
        days_amount:int = settings["days_amount"]

        iso_date_list = self._create_isostring_list(date_start, days_amount)

        weekhours = UsersWorkTimes.objects.filter(user= request.user).filter(date__gte= date_start).filter(date__lte= date_end).values(
            "date","travel_start", "travel_end", "work_start", "work_end", "workimes_standard__description", "project_machine", "netzplan_vorgang")
        json_weekhours = list(weekhours)
        #json_weekhours = [model_to_dict(i) for i in  weekhours]
        link_dir = "/a20_users/xday_overview/"

        context = {"iso_date_list": iso_date_list, "settings": settings, "json_weekhours": json_weekhours, "json_link_dir": link_dir}
        return render(request= request, template_name= self.HTML_FILE, context= context)
    #}
    def post(self, request:HttpRequest):#{
        date_now = request.POST.get("date_now", "")
        days_amount = request.POST.get("days_amount", "")
        
        if date_now:#[
            settings = {}
            settings["days_amount"] = int(days_amount)

            date_start = date.fromisoformat(date_now)
            date_end = date_start + timedelta(days= int(days_amount))

            settings["date_start"] = date_start.isoformat()
            settings["date_end"] = date_end.isoformat()

            if request.session.get("VIEW_SETTINGS"):
                _save_view_settings(settings, request.session["VIEW_SETTINGS"])
            else:
                request.session["VIEW_SETTINGS"] = {}
                _save_view_settings(settings, request.session["VIEW_SETTINGS"])
            request.session.modified = True
        #]
        return HttpResponseRedirect(reverse(self.URL_LINK))
    #}
#======================================================================================================================

#**********************************************************************************************************************
#  Query set for specyfic day
class ViewUserCurrentDay_overwiev(View):
    HTML_FILE = "xday_overview.html"
    URL_LINK = "xday_overview"

    def get(self, request:HttpRequest, cd:str):#{
        current_entries = request.session.get("LAST_ENTRY", {})

        form = FormWorktimeEntry(current_entries) 
        current_date = date.fromisoformat(cd)

        query_set = UsersWorkTimes.objects.filter(user= request.user).filter(date= current_date)
        context = {"query_set" : query_set, "form" : form, "id" : id, "cd" : cd}
        return render(request= request, template_name= self.HTML_FILE, context= context)
    #}
    def post(self, request:HttpRequest, cd:str):#{
        current_date = date.fromisoformat(cd)

        form = FormWorktimeEntry(data= request.POST)
        if form.is_valid():#[
            current_entries = {}

            for key in ["travel_start", "travel_end", "work_start", "work_end"]:
                val = form.cleaned_data[key]
                current_entries[key] = val.isoformat() if val else ""
            _save_last_input(current_entries, request, "LAST_ENTRY")
            
            # (currententry, ifCreated) = UsersWorkTimes.objects.get_or_create(user= request.user, date= current_date)
            new_user_work_times = UsersWorkTimes.objects.create(user= request.user, date= current_date)
            if form.cleaned_data["travel_start"]:
                new_user_work_times.travel_start = form.cleaned_data["travel_start"]

            if form.cleaned_data["travel_end"]:
                new_user_work_times.travel_end = form.cleaned_data["travel_end"]

            if form.cleaned_data["work_start"]:
                new_user_work_times.work_start = form.cleaned_data["work_start"]

            if form.cleaned_data["work_end"]:
                new_user_work_times.work_end = form.cleaned_data["work_end"]

            if form.cleaned_data["worktimes_standard"]:
                new_user_work_times.workimes_standard = form.cleaned_data["worktimes_standard"]

            if form.cleaned_data["project_machine"]:
                new_user_work_times.project_machine = str(form.cleaned_data["project_machine"])

            if form.cleaned_data["netzplan_vorgang"]:
                new_user_work_times.netzplan_vorgang = str(form.cleaned_data["netzplan_vorgang"])

            new_user_work_times.save()
            return HttpResponseRedirect(reverse(self.URL_LINK, args=[cd]))
        #]
        else:#[
            error = f"Input form error! cleaned_data= {form.changed_data}"
            return render(request= request, template_name= A20_ERROR_HTML, context= {"error" : error, "form" : form})
    #}
#======================================================================================================================

#**********************************************************************************************************************
#  
class ViewUserCurrentDay_modify(View):
    HTML_FILE = "xday_modify.html"
    URL_LINK = "xday_modify"

    def get(self, request:HttpRequest, id:int, cd:str):#{
        try:
            user_work_time = UsersWorkTimes.objects.get(pk= int(id))
        except UsersWorkTimes.DoesNotExist:
            error = f"Current user work entry does not exist! id={id}"
            return render(request= request, template_name= A20_ERROR_HTML, context= {"error" : error})
        
        current_entries = request.session.get("LAST_ENTRY", {})
        form = FormWorktimeEntry(current_entries) 

        context = {"uwt" : user_work_time, "form" : form, "cd" : cd}
        return render(request= request, template_name= self.HTML_FILE, context= context)
    #}
    def post(self, request:HttpRequest, id:int, cd:str):#{
        current_date = date.fromisoformat(cd)

        form = FormWorktimeEntry(data= request.POST)
        if form.is_valid():#[
            current_entries = {}

            for key in ["date","travel_start", "travel_end", "work_start", "work_end"]:
                val = form.cleaned_data[key]
                current_entries[key] = val.isoformat() if val else ""
            _save_last_input(current_entries, request, "LAST_ENTRY")
            
            user_work_time = UsersWorkTimes.objects.get(pk= id)
            if form.cleaned_data["travel_start"]:
                user_work_time.travel_start = form.cleaned_data["travel_start"]

            if form.cleaned_data["travel_end"]:
                user_work_time.travel_end = form.cleaned_data["travel_end"]

            if form.cleaned_data["work_start"]:
                user_work_time.work_start = form.cleaned_data["work_start"]

            if form.cleaned_data["work_end"]:
                user_work_time.work_end = form.cleaned_data["work_end"]

            if form.cleaned_data["worktimes_standard"]:
                user_work_time.workimes_standard = form.cleaned_data["worktimes_standard"]

            if form.cleaned_data["project_machine"]:
                user_work_time.project_machine = str(form.cleaned_data["project_machine"])

            if form.cleaned_data["netzplan_vorgang"]:
                user_work_time.netzplan_vorgang = str(form.cleaned_data["netzplan_vorgang"])

            user_work_time.save()
            return HttpResponseRedirect(reverse(ViewUserCurrentDay_overwiev.URL_LINK, args=[cd]))
        #]
        else:#[
            error = f"Input form error! cleaned_data= {form.changed_data}"
            return render(request= request, template_name= A20_ERROR_HTML, context= {"error" : error, "form" : form})
    #}
#======================================================================================================================

#**********************************************************************************************************************
# Administrator user hours overview with posibolity to add new and change
class ViewUserCurrentDay_delete(View):
    HTML_FILE = "xday_delete.html"
    
    def get(self, request:HttpRequest, id:int, cd:str):#{
        try:
            user_work_time = UsersWorkTimes.objects.get(pk= int(id))
        except UsersWorkTimes.DoesNotExist:#{
            error = f"Current user work entry does not exist! id={id}"
            return render(request= request, template_name= A20_ERROR_HTML, context= {"error" : error})
        #}
        current_entries = request.session.get("LAST_ENTRY", {})
        form = FormWorktimeEntry(current_entries) 

        context = {"currententry" : user_work_time, "form" : form, "cd" : cd}
        return render(request= request, template_name= self.HTML_FILE, context= context)
    #}
    def post(self, request:HttpRequest, id:int, cd:str):#{
        operation = request.POST.get("operation")
        
        if operation == "delete":
            user_work_time = UsersWorkTimes.objects.get(pk= int(id))
            user_work_time.delete()
            return HttpResponseRedirect(reverse(ViewUserCurrentDay_overwiev.URL_LINK, args=[cd]))
        elif operation == "cancel":
            return HttpResponseRedirect(reverse(ViewUserCurrentDay_overwiev.URL_LINK, args=[cd]))
        else:
            error = f"Input form error, not delete, not cancel!"
            return render(request= request, template_name= A20_ERROR_HTML, context= {"error" : error})
        #}
#======================================================================================================================

#**********************************************************************************************************************
# Administrator user hours overview with posibolity to add new and change
class ViewAdminAllHours_overview(View):
    HTML_FILE = "all_hours_overview.html"
    URL_LINK = "all_hours_overview"
    
    def get(self, request:HttpRequest):#{
        query_set = UsersWorkTimes.objects.all()

        defaultentries = {"travel_start" :  time(hour= 6, minute= 15), "travel_end" : time(hour= 18, minute= 0),
            "work_start" : time(hour= 7, minute= 15), "work_end" : time(hour= 17, minute= 15)}
        
        form = FormAdminWorktimeEntry(defaultentries) 

        context = {"form" : form, "query" : query_set}
        return render(request= request, template_name= self.HTML_FILE, context= context)
    #}
    def post(self, request:HttpRequest):#{
        form = FormAdminWorktimeEntry(data= request.POST)
        if form.is_valid():#[
            # save_cookies(form.cleaned_data, request, ["date", "travel_start", "travel_end", "work_start", "work_end"], "LAST_ENTRY")
            # user = form.cleaned_data["user"]
            # user_id = user.pk
            # instUser = User.objects.get(pk= user_id)
            newentry = UsersWorkTimes.objects.create(user= form.cleaned_data["user"],  
                                            date= form.cleaned_data["date"],

                                            travel_start= form.cleaned_data["travel_start"],
                                            travel_end= form.cleaned_data["travel_end"],

                                            work_start= form.cleaned_data["work_start"],
                                            work_end= form.cleaned_data["work_end"],
                                            workimes_standard= form.cleaned_data["worktimes_standard"],

                                            project_machine= str(form.cleaned_data["project_machine"]),
                                            netzplan_vorgang= str(form.cleaned_data["netzplan_vorgang"]))

            return HttpResponseRedirect(reverse("all_hours_overview"))
        #]
        else:#[
            error = f"Input form invalid!"
            return render(request= request, template_name= A20_ERROR_HTML, context= {"error" : error, "form" : form})
        #]
    #}
#======================================================================================================================

#**********************************************************************************************************************
# Administrator menage hours of the users
class ViewAdminAllHours_modify(View):
    HTML_FILE = "all_hours_modify.html"
    
    def get(self, request:HttpRequest, id:int):#{
        try:
            query_set = UsersWorkTimes.objects.get(pk= id)
        except UsersWorkTimes.DoesNotExist:
            error = f"Entry of id= {id} does not exist"
            return render(request= request, template_name= A20_ERROR_HTML, context= {"error" : error})
        else:
            defaultentries = {"travel_start" :  time(hour= 6, minute= 15), "travel_end" : time(hour= 18, minute= 0), "work_start" : time(hour= 7, minute= 15), "work_end" : time(hour= 17, minute= 15)}
            form = FormAdminWorktimeEntry(defaultentries) 
            context = {"form" : form, "query" : query_set}
            return render(request= request, template_name= self.HTML_FILE, context= context)
    #}
    def post(self, request:HttpRequest, id:int):#{
        form = FormAdminWorktimeEntry(data= request.POST)
        if form.is_valid():#[
            # save_cookies(form.cleaned_data, request, ["date", "travel_start", "travel_end", "work_start", "work_end"], "LAST_ENTRY")

            query_set = UsersWorkTimes.objects.get(pk= id)

            if form.cleaned_data["user"]:
                query_set.user= form.cleaned_data["user"]  

            if form.cleaned_data["date"]:
                query_set.date= form.cleaned_data["date"]

            if form.cleaned_data["travel_start"]:
                query_set.travel_start= form.cleaned_data["travel_start"]

            if form.cleaned_data["travel_end"]:
                query_set.travel_end= form.cleaned_data["travel_end"]

            if form.cleaned_data["work_start"]:
                query_set.work_start= form.cleaned_data["work_start"]

            if form.cleaned_data["work_end"]:
                query_set.work_end= form.cleaned_data["work_end"]

            if form.cleaned_data["worktimes_standard"]:
                query_set.workimes_standard= form.cleaned_data["worktimes_standard"]

            if form.cleaned_data["project_machine"]:
                query_set.project_machine= str(form.cleaned_data["project_machine"])

            if form.cleaned_data["netzplan_vorgang"]:
                query_set.netzplan_vorgang= str(form.cleaned_data["netzplan_vorgang"])
                                            
            query_set.save()

            return HttpResponseRedirect(reverse(ViewAdminAllHours_overview.URL_LINK))
        #]
        else:#[
            error = f"Input form invalid!"
            return render(request= request, template_name= A20_ERROR_HTML, context= {"error" : error, "form" : form})
    #}
#======================================================================================================================

#**********************************************************************************************************************
# Administrator menage hours of the users
class ViewAdminAllHours_delete(View):
    HTML_FILE = "xday_delete.html"
    
    def get(self, request:HttpRequest, id:int):#{
        try:
            query_set = UsersWorkTimes.objects.get(pk= id)
        except UsersWorkTimes.DoesNotExist:
            error = f"Current user entry does not exist!"
            return render(request= request, template_name= A20_ERROR_HTML, context= {"error" : error})
        else:
            return render(request= request, template_name= self.HTML_FILE, context= {"current_entry" : query_set})
    #}
    def post(self, request:HttpRequest, id:int):#{
        if request.POST.get("operation", "") == "delete":
            query_set = UsersWorkTimes.objects.get(pk= id)
            query_set.delete()
        return HttpResponseRedirect(reverse(ViewAdminAllHours_overview.URL_LINK))
    #}
#======================================================================================================================