from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
#---------------------------------------------------------------------
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from a00_accounts.models import Cooperation
from a00_accounts.forms import FormRegisterUser, FormLoginView, FormCooperation
from a20_users.models import UserSettings
from mylib.timecalculations import isoformat_date
from datetime import  date, timedelta
#---------------------------------------------------------------------
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

#**********************************************************************************************
# User connections
class ViewUsersConnections_overview(View):#{
    # permission_required = ["book.add_genere_form"]
    def get(self, request:HttpRequest):
        cooperations = Cooperation.objects.all()
        form = FormCooperation()
        cooperations = Cooperation.objects.all()

        dict_cooperations = []
        for c in cooperations:
            description = c.description
            users = [str(i) for i in c.users.all()]
            projects = [str(i) for i in c.projects.all()]
            description = c.description
            dict_cooperations.append({"pk" : c.pk,"description" : description, "users" : users, "projects" : projects})

        context = {"form" : form, "cooperations" : dict_cooperations}
        return render(request= request, template_name= "users_connections_overview.html", context= context)
    #}

    def post(self, request:HttpRequest):#{}
        form = FormCooperation(request.POST)
        if form.is_valid():#[
            if form.cleaned_data["description"] and form.cleaned_data["users"] and form.cleaned_data["projects"]:#[
                cooperation = Cooperation.objects.create(description= form.cleaned_data["description"])
                for i in form.cleaned_data["users"]:
                    cooperation.users.add(i)

                for i in form.cleaned_data["projects"]:
                    cooperation.projects.add(i)
                cooperation.save()
            #]
            return HttpResponseRedirect(reverse("users_connections_overview"))
        #]
        else:
            error = f"Users connections input form is not valid!"
            return render(request= request, template_name= "a00_error_info.html", context= {"error" : error})
    #}
#---------------------------------------------------------------------
class ViewUsersConnections_delete(LoginRequiredMixin ,View):
    def get(self, request:HttpRequest, id:int):
        try:
            cooperation = Cooperation.objects.get(pk= id)
        except Cooperation.DoesNotExist:
            error = f"Cooperation delete error! Item with idx= {id} does not exist!"
            return render(request= request, template_name= "a00_error_info.html", context= {"error" : error}) 
        else:
            return render(request= request,template_name= "users_connections_delete.html", context= {"cooperation" : cooperation})          

    def post(self, request:HttpRequest, id:int):
        operation = request.POST.get("operation", "")

        if operation == "delete":#[
            cooperation = Cooperation.objects.get(pk= id)
            cooperation.delete()
            return HttpResponseRedirect(reverse("users_connections_overview"))
        #]
        elif operation == "cancel":#[
            return HttpResponseRedirect(reverse("users_connections_overview"))
        #]
        else:
            error = f"Machine item delete: Input form error! Nor delete, not cancel! operation= {operation}"
            return render(request= request, template_name= "a00_error_info.html", context= {"error" : error})
    #}
#---------------------------------------------------------------------
class ViewUsersConnections_modify(LoginRequiredMixin, View):
    def get(self, request:HttpRequest, id:int):
        try:
            cooperation = Cooperation.objects.get(pk= id)
        except Cooperation.DoesNotExist:
            error = f"Cooperation delete error! Item with idx= {id} does not exist!"
            return render(request= request, template_name= "a00_error_info.html", context= {"error" : error}) 
        else:
            form = FormCooperation()
            return render(request= request,template_name= "users_connections_modify.html", context= {"cooperation" : cooperation, "form" :form})   

    def post(self, request:HttpRequest, id:int):#{
        form = FormCooperation(request.POST)
        if form.is_valid():#[
            cooperation = Cooperation.objects.get(pk= id)

            if form.cleaned_data["description"]:
                cooperation.description = form.cleaned_data["description"]

            if form.cleaned_data["users"]:
                for i in form.cleaned_data["users"]:
                    cooperation.users.add(i)

            if form.cleaned_data["projects"]:
                for i in form.cleaned_data["projects"]:
                    cooperation.projects.add(i)

            cooperation.save()

            return HttpResponseRedirect(reverse("users_connections_overview"))
        #]
        else:#[
            error = f"Input form invalid! {form.cleaned_data}"
            return render(request= request, template_name= "a00_error_info.html", context= {"error" : error, "form" : form})
    #}
#---------------------------------------------------------------------
#==============================================================================================

#---------------------------------------------------------------------
def default_time()->tuple[date, date, int]:#{
    data_start = date.today()
    date_end = data_start + timedelta(days= 7)
    return data_start, date_end, 7
#}

def set_innitial_session(request:HttpRequest, key:str):
    (data_start, date_end, amount_days) = default_time()

    if request.session.get(key, None):
        return
    
    settings = {}
    settings["date_start"] = data_start.isoformat()
    settings["date_end"] = date_end.isoformat()
    settings["days_amount"] = amount_days
    request.session[key] = settings
    request.session.modified = True
#---------------------------------------------------------------------
class ViewsUserRegister(View):
    
    def get(self, request:HttpRequest):
        form = FormRegisterUser()
        return render(request= request, template_name= "user_register.html", context= {"form" : form})
    
    def post(self, request:HttpRequest):
        form = FormRegisterUser(request.POST)
        if form.is_valid():
            user = form.save(commit= False)

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]

            user.email = form.cleaned_data["email1"]
            user.set_password(form.cleaned_data["password1"])

            form.save()
            
            userSettings = UserSettings.objects.create(user= user)
            
            set_innitial_session(request, "VIEW_SETTINGS")
            return redirect(to= "welcome_user", us= user.username, ac= 'reg')
        
        else:
            error = f"Wrong register data!"
            return render(request= request, template_name= "a00_error_info.html", context= {"error" : error, "form" : form})


class ViewsUserLogin(View):
    def get(self, request:HttpRequest):
        form = FormLoginView()
        return render(request= request, template_name= "user_login.html", context= {"form" : form})
    
    def post(self, request:HttpRequest):
        context = {}
        errList = []

        form = FormLoginView(request.POST)
        context["form"] = form
        context["error"] = errList
        if form.is_valid():
            username = form.cleaned_data.get("username", "")
            password = form.cleaned_data.get("password", "")
            user = authenticate(username= username, password= password)
            if user is not None:
                login(request= request, user= user)
                set_innitial_session(request, "VIEW_SETTINGS")
                return redirect(to= "welcome_user", us= username, ac= 'log')
                nexturl = request.GET.get("next", "home")
                return redirect(nexturl)
            else:
                errList.append("user == None")
        else:
            form = FormLoginView()
            context["form"] = form
            errList.append("is_valid == False")
            
        return render(request= request, template_name= "user_login.html", context= context)
    

def viewsUserLogout(request:HttpRequest):
    logout(request)
    return redirect("home")
    
#---------------------------------------------------------------------------------------------------------------
    
class ViewsAllUsersData(View):
    HTML_FILE = "admin_users_overview.html"
    URL_LINK = "admin_users_overview"
    def get(self, request:HttpRequest):
        users = User.objects.exclude(username= "admin")
        return render(request= request, template_name= ViewsAllUsersData.HTML_FILE, context= {"users" : users})
    

class ViewUserDelete(LoginRequiredMixin, View):
    HTML_FILE = "admin_user_delete.html"

    def get(self, request:HttpRequest, id:int):

        user = User.objects.get(pk= id)
        form = FormRegisterUser()
        return render(request= request ,template_name= ViewUserDelete.HTML_FILE, context= {"user" : user ,"form" : form})
    
    def post(self, request:HttpRequest, id:int):#{
        operation = request.POST.get("operation", "")

        if operation  == "delete":#[
            user = User.objects.get(pk= id)
            # userSettings = UserSettings.objects.get(user= user)
            # userSettings.delete()
            user.delete()
            return HttpResponseRedirect(reverse(ViewsAllUsersData.URL_LINK))
        #]
        elif operation == "cancel":#[
            return HttpResponseRedirect(reverse(ViewsAllUsersData.URL_LINK))
        #]
        else:
            error = f"User settings item delete: Input form error! Nor delete, not cancel! operation = {operation}"
            return render(request= request, template_name= "a00_error_info.html", context= {"error" : error})
    #}    

class ViewUserModify(LoginRequiredMixin, View):
    def get(self, request:HttpRequest, id:int):
        user = User.objects.get(pk= id)
        form = FormRegisterUser()
        return render(request= request ,template_name= "admin_user_modify.html", context= {"user" : user ,"form" : form})
    
    def post(self, request:HttpRequest, id:int):
        form = FormRegisterUser(request.POST)
        if form.is_valid():
            user = User.objects.get(pk= id)

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email11"]

            user.set_password(form.cleaned_data["pass11"])

            form.save()
        return HttpResponseRedirect(reverse("admin_users_overview"))


#-----------------------------------------------------------------------------------------------------------------------

def view_userRegister(request:HttpRequest):
    context = {}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        context["form"] = form
        if form.is_valid():
            form.save()
            u = form.cleaned_data["username"]
            return redirect("welcome_user", u=u, lr="R")

        else:
            context["INFO"] = "Not valid!"

    else:
        form = UserCreationForm()
        context["form"] = form
        context["INFO"] = "Get method"
    return render(request= request, template_name= "v2_user_register.html", context= context)

def view_ShowUser(request:HttpRequest, us:str, ac:str):
    user = User.objects.get(username= us)

    if ac == "reg":
        return render(request= request, template_name= "welcome_new_user.html", context= {"user" : user})
    else: # ac == 'log'
        return render(request= request, template_name= "welcome_loged_user.html", context= {"user" : user})

#-----------------------------------------------------------------------------------------------------------------------

class ViewAdminUserSettings_overview(View):
    HTML_FILE = "admin_usr_sett_overview.html"
    URL_NAME = "admin_usr_sett_overview"

    def get(self, request:HttpRequest):
        users_settings = UserSettings.objects.all()
        return render(request= request, template_name= ViewAdminUserSettings_overview.HTML_FILE, context= {"users_settings" : users_settings})
    
    def post(self, request:HttpRequest):#{
        user_id = request.POST.get("user_id", "")
        if user_id:
            try:
                user = User.objects.get(pk= int(user_id))
            except User.DoesNotExist:
                error = f"Error: User(id)= {id} does not exist! Settings can not be created!"
                return render(request= request, template_name= "a00_error_info.html", context= {"error" : error})

            settings = UserSettings.objects.create(user= user)
            return HttpResponseRedirect(reverse(ViewAdminUserSettings_overview.URL_NAME))
        
        else:
            error = f"Error: Input form error! user_id= {user_id}"
            return render(request= request, template_name= "a00_error_info.html", context= {"error" : error})
#}
#-----------------------------------------------------------------------------------------------------------------------
class ViewAdminUserSettings_modify(View):
    HTML_FILE = "admin_usr_sett_modify.html"
    URL_NAME = "admin_usr_sett_modify"

    def get(self, request:HttpRequest, id:int):#{
        try:
            user_settings = UserSettings.objects.get(pk= id)
        except UserSettings.DoesNotExist:
            error = f"Error: User settings id= {id} does not exist!"
            return render(request= request, template_name= "a00_error_info.html", context= {"error" : error})
        else:
            return render(request= request, template_name= ViewAdminUserSettings_modify.HTML_FILE, context= {"user_settings" : user_settings})
    #}
    def post(self, request:HttpRequest, id:int):#{
        datestart =  isoformat_date(request.POST.get("date_start", ""))
        dateend = isoformat_date(request.POST.get("date_end", ""))
        weekdate = isoformat_date(request.POST.get("weeknum", ""))

        if (dateend and datestart) or weekdate:#{
            user_settings = UserSettings.objects.get(pk= id)

            if weekdate:
                user_settings.weekSelected = weekdate
            
            if (dateend and datestart) and (datestart <= dateend):
                user_settings.rangeStart = datestart
                user_settings.rangeEnd = dateend
                
            user_settings.save()
            return HttpResponseRedirect(reverse(ViewAdminUserSettings_overview.URL_NAME))
        #}
        error = f"Error: data input empty! ({datestart} && {dateend}) || {weekdate}"
        return render(request= request, template_name= "a00_error_info.html", context= {"error" : error})
    #}
#}
    