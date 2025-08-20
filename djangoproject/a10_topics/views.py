from django.http import HttpRequest, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from a00_accounts.models import Cooperation
from a10_topics.models import  ProjectMachines, Netzplan, Vorgang, NetzplanVorgang
from a10_topics.forms import FormShowPeopleInProject

#------------------------------------------------------------------------------------------------

class ViewProjectCooperation_overview(View):
    def get(self, request:HttpRequest):#{
        form = FormShowPeopleInProject()

        cooperations = Cooperation.objects.all()
        dict_cooperations = []
        for c in cooperations:
            description = c.description
            users = [str(i) for i in c.users.all()]
            projects = [str(i) for i in c.projects.all()]
            description = c.description
            dict_cooperations.append({"pk" : c.pk,"description" : description, "users" : users, "projects" : projects})
        context = {"form" :form ,"cooperations" : dict_cooperations}
        return render(request= request, template_name="project_connections.html", context= context)
    #}
    
    def post(self, request:HttpRequest):#{
        form = FormShowPeopleInProject(request.POST)

        if form.is_valid():#[
            machine_project = form.cleaned_data["machine_project"]
            cooperations = Cooperation.objects.filter(projects= machine_project)

            dict_cooperations = []
            for c in cooperations:
                description = c.description
                users = [str(i) for i in c.users.all()]
                projects = [str(i) for i in c.projects.all()]
                description = c.description
                dict_cooperations.append({"pk" : c.pk,"description" : description, "users" : users, "projects" : projects})
            context = {"cooperations" : dict_cooperations}
            return render(request= request, template_name="project_connections.html", context= context)
        #]
        else:
            error = f"Input filter error!"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error, "form" :form})
    #}

#------------------------------------------------------------------------------------------------

class ViewProjectMachines_overview(View):
    URL_NAME = "machines_overview"
    HTML_NAME = "machines_overview.html"
    
    # Method get 'default'
    def get(self, request:HttpRequest):
        query_set = ProjectMachines.objects.all()
        context = {"machines" : query_set}
        return render(request= request, template_name= self.HTML_NAME, context= context)
    #}

    # Method post, form is send
    def post(self, request:HttpRequest):#{
        project = request.POST.get("project", "")
        machine = request.POST.get("machine", "")
        description = request.POST.get("description", "")

        if project and machine and description:
            ProjectMachines.objects.create(project=project, machine= machine, description= description)
            return HttpResponseRedirect(reverse(self.URL_NAME))
        else:
            error = f"Add Machine Error! Some input blank: project= {project}, machine= {machine}, description= {description}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
    #}

class ViewProjectMachine_modify(View):
    HTML_NAME = "machine_modify.html"
    # Method get 'default'
    def get(self, request:HttpRequest, id):#{
        try:
            project_machine = ProjectMachines.objects.get(pk=id)
        except ProjectMachines.DoesNotExist:
            error = f"Machine delete error! Item with idx= {id} does not exist!"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
        else:
            return render(request= request, template_name= self.HTML_NAME, context= {"project_machine" : project_machine})
    #}

    # Method post, form is send
    def post(self, request:HttpRequest, id):#{
        project = request.POST.get("project", "")
        machine = request.POST.get("machine", "")
        description = request.POST.get("description", "")

        if project or machine or description:#[
            projectMachine = ProjectMachines.objects.get(pk=id)
            if project:
                projectMachine.project = project
            if machine:
                projectMachine.machine = machine
            if description:
                projectMachine.description = description
            projectMachine.save()
            return HttpResponseRedirect(reverse(ViewProjectMachines_overview.URL_NAME))
        #]
        else:
            error = f"Existed machine item modify error! Blank input: project= {project}, machine= {machine}, description= {description}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
    #}

class ViewProjectMachine_delete(View):
    HTML_NAME = "machine_delete.html"
    # Method get 'default'
    def get(self, request:HttpRequest, id):#{
        try:
            machine = ProjectMachines.objects.get(pk=id)
        except ProjectMachines.DoesNotExist:
            error = f"Machine delete error! Item with idx= {id} does not exist!"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
        else:
            return render(request= request, template_name= self.HTML_NAME, context= {"machine" : machine})
    #}

    # Method post, form is send
    def post(self, request:HttpRequest, id):#{
        operation = request.POST.get("operation", "")

        if operation == "delete":#[
            projectMachine = ProjectMachines.objects.get(pk= id)
            projectMachine.delete()
            return HttpResponseRedirect(reverse(ViewProjectMachines_overview.URL_NAME))
        #]
        elif operation == "cancel":#[
            return HttpResponseRedirect(reverse(ViewProjectMachines_overview.URL_NAME))
        #]
        else:
            error = f"Machine item delete: Input form error! Nor delete, not cancel! operation= {operation}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
    #}

#------------------------------------------------------------------------------------------------

class ViewNetzplan_overview(View):
    URL_NAME =  "netzplan_overview"
    HTML_NAME = "netzplan_overview.html"

    def get(self, request:HttpRequest):#{
        query_set = Netzplan.objects.all()
        return render(request= request, template_name= self.HTML_NAME, context= {"netzplan_items" : query_set})
    #}
    
    def post(self, request:HttpRequest):#{
        number = request.POST.get("number", "")
        description = request.POST.get("description", "")

        if number and description:
            Netzplan.objects.create(number= number, description= description)
            return HttpResponseRedirect(reverse(self.URL_NAME))
        else:
            error = f"Add Netzplan Error! Some input blank: number= {number}, description= {description}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
    #}
    
class ViewNetzplan_delete(View):
    HTML_NAME = "netzplan_delete.html"

    def get(self, request:HttpRequest, id:int):#{
        try: 
            netzplan = Netzplan.objects.get(pk= id)
        except Netzplan.DoesNotExist:
            error = f"Netzplan delete: item index= {id} does not exist!"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
        else:
            return render(request= request, template_name= self.HTML_NAME, context= {"netzplan" : netzplan})
    #}

    def post(self, request:HttpRequest, id:int): #{
        operation = request.POST.get("operation", "")

        if operation == "delete":#[
            netzplan = Netzplan.objects.get(pk= id)
            netzplan.delete()
            return HttpResponseRedirect(reverse(ViewNetzplan_overview.URL_NAME))
        #]
        elif operation == "cancel":
            return HttpResponseRedirect(reverse(ViewNetzplan_overview.URL_NAME))
        #]
        else:
            error = f"Machine item delete: Input form error! Nor delete, not cancel! operation= {operation}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
    #}
    
class ViewNetzplan_modify(View):
    HTML_NAME = "netzplan_modify.html"

    def get(self, request:HttpRequest, id:int):#{
        try: 
            netzplan = Netzplan.objects.get(pk= id)
        except Netzplan.DoesNotExist:
            error = f"Netzplan modify: item index= {id} does not exist!"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
        else:
            return render(request= request, template_name= self.HTML_NAME, context= {"netzplan" : netzplan})
    #}
    
    def post(self, request:HttpRequest, id:int):#{
        number = request.POST.get("number", "")
        description = request.POST.get("description", "")

        if number or description:#[
            netzplan = Netzplan.objects.get(pk= id)
            if number:
                netzplan.number = number
            if description:
                netzplan.description = description
            netzplan.save()
            return HttpResponseRedirect(reverse(ViewNetzplan_overview.URL_NAME))
        #]
        else:
            error = f"Netzplan modify error! Empty input: number= {number}, description={description}."
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
    #}
        
#------------------------------------------------------------------------------------------------

class ViewVorgang_overview(View):
    URL_NAME =  "vorgang_overview"
    HTML_NAME = "vorgang_overview.html"

    def get(self, request:HttpRequest):#{
        query_set = Vorgang.objects.all()
        return render(request= request, template_name= self.HTML_NAME, context= {"vorgang_items" : query_set})
    #}
    
    def post(self, request:HttpRequest):#{
        number = request.POST.get("number", "")
        description = request.POST.get("description", "")

        if number and description:
            Vorgang.objects.create(number= number, description= description)
            return HttpResponseRedirect(reverse(self.URL_NAME))
        else:
            error = f"Vorgang add new: Input form blank data! number: {number}, description: {description}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
    #}
    
class ViewVorgang_delete(View):
    HTML_NAME = "vorgang_delete.html"

    def get(self, request:HttpRequest, id:int):#{
        try: 
            vorgang = Vorgang.objects.get(pk= id)
        except Vorgang.DoesNotExist:
            error = f"Vorgang delete: item index= {id} does not exist!"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
        else:
            return render(request= request, template_name= self.HTML_NAME, context= {"vorgangItem" : vorgang})
    #}

    def post(self, request:HttpRequest, id:int):#{
        operation = request.POST.get("operation", "")

        if operation == "delete":#[
            vorgangItem = Vorgang.objects.get(pk= id)
            vorgangItem.delete()
            return HttpResponseRedirect(reverse(ViewVorgang_overview.URL_NAME))
        #]
        elif operation == "cancel":#[
            return HttpResponseRedirect(reverse(ViewVorgang_overview.URL_NAME))
        #]
        else:
            error = f"Vorgang item delete: Input form error! Nor delete, not cancel! operation = {operation}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
    #}
    
class ViewVorgang_modify(View):
    HTML_NAME = "netzplan_modify.html"

    def get(self, request:HttpRequest, id:int):#{
        try: 
            vorgang = Vorgang.objects.get(pk= id)
        except Vorgang.DoesNotExist:
            error = f"Vorgang modify: item index= {id} does not exist!"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
        return render(request= request, template_name= self.HTML_NAME, context= {"vorgang" : vorgang})
    #}
    
    def post(self, request:HttpRequest, id:int):#{
        number = request.POST.get("number", "")
        description = request.POST.get("description", "")

        if number or description:#[
            vorgang = Vorgang.objects.get(pk= id)
            if number:
                vorgang.number = number
            if description:
                vorgang.description = description
            vorgang.save()
            return HttpResponseRedirect(reverse(ViewVorgang_overview.URL_NAME))
        #]
        else:
            error = f"Vorgang modify: Input form blank data: number: {number}, description: {description}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
    #}
        
#------------------------------------------------------------------------------------------------

class ViewNetzplanVorgang_overview(View):
    URL_NAME =  "netzplanvorgang_overview"
    HTML_NAME = "netzplanvorgang_overview.html"

    def get(self, request:HttpRequest):#{
        netzplanvorgang = NetzplanVorgang.objects.all()
        netzplan_items = Netzplan.objects.all()
        vorgang_items = Vorgang.objects.all()

        return render(request= request, template_name= self.HTML_NAME, 
                      context= {"netzplanvorgang" : netzplanvorgang, "netzplan_items":netzplan_items, "vorgang_items":vorgang_items})
    #}

    def post(self, request:HttpRequest):#{
        netzplan_id = request.POST.get("netzplan", "")
        vorgang_id = request.POST.get("vorgang", "")
        description = request.POST.get("description", "")

        if netzplan_id == "" or vorgang_id == "":#[
            error = f"Input form error! Info: {netzplan_id}, {vorgang_id}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
        #]
        if netzplan_id == "null" and vorgang_id == "null":#[
            error = "Both foreign keys empty! One need to by filled. " + f"{netzplan_id}, {vorgang_id}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
        #]
        if netzplan_id != "null":#[
            try:
                netzplan_id = int(netzplan_id)
            except ValueError:
                error = "Netzplan id conversion to int error! id= {}".format(netzplan_id)
                return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
            else:
                netzplan = Netzplan.objects.get(pk= netzplan_id)
        #]
        if vorgang_id != "null":#[
            try:
                vorgang_id = int(vorgang_id)
            except ValueError:
                error = "Vorgang id conversion to int error! id= {}".format(vorgang_id)
                return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
            else:
                vorgang = Vorgang.objects.get(pk= vorgang_id)
        #]
        netzplanvorgang = NetzplanVorgang.objects.create(netzplan= netzplan, vorgang= vorgang, description= description)
        return HttpResponseRedirect(reverse(ViewNetzplanVorgang_overview.URL_NAME))
    #}

class ViewNetzplanVorgang_delete(View):
    HTML_NAME = "netzplanvorgang_delete.html"

    def get(self, request:HttpRequest, id:int):#{
        try:
            netzplanvorgang = NetzplanVorgang.objects.get(pk= id)
        except NetzplanVorgang.DoesNotExist:
            error = f"NetzplanVorgang modify: item index= {id} does not exist!"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
        else:
            return render(request= request, template_name= self.HTML_NAME, context= {"netzplanvorgang":netzplanvorgang})
    #}

    def post(self, request:HttpRequest, id:int):
        operation = request.POST.get("operation", "")

        if operation == "delete":#[
            netzplanvorgang = NetzplanVorgang.objects.get(pk= id)
            netzplanvorgang.delete()
            return HttpResponseRedirect(reverse(ViewNetzplanVorgang_overview.URL_NAME))
        #]
        elif operation == "cancel":#[
            return HttpResponseRedirect(reverse(ViewNetzplanVorgang_overview.URL_NAME))
        #]
        else:
            error = f"NetzplanVorgang item delete: Input form error! Nor delete, not cancel! operation = {operation}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
    #}

class ViewNetzplanVorgang_modify(View):
    HTML_NAME = "netzplanvorgang_modify.html"

    def get(self, request:HttpRequest, id:int):#{
        try:
            netzplanvorgang = NetzplanVorgang.objects.get(pk= id)
        except NetzplanVorgang.DoesNotExist:
            error = f"NetzplanVorgang modify: item index= {id} does not exist!"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
        else:
            netzplan_items = Netzplan.objects.all()
            vorgang_items = Vorgang.objects.all()
            return render(request= request, template_name= self.HTML_NAME, 
                          context= {"netzplanvorgang":netzplanvorgang, "netzplan_items":netzplan_items, "vorgang_items":vorgang_items})
    #}

    def post(self, request:HttpRequest, id:int):
        netzplan_id = request.POST.get("netzplan", "")
        vorgang_id = request.POST.get("netzplan", "")
        description = request.POST.get("description", "")

        if netzplan_id or vorgang_id or description :#[
            netzplanvorgang = NetzplanVorgang.objects.get(pk= id)

            if netzplan_id and netzplan_id != "null":#[
                try:
                    netzplan_id = int(netzplan_id)
                except ValueError:
                    error = "Netzplan id conversion to int error! id= {}".format(netzplan_id)
                    return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
                else:
                    netzplan = Netzplan.objects.get(pk= netzplan_id)
                    netzplanvorgang.netzplan = netzplan
            #]
            if vorgang_id and vorgang_id != "null":#[
                try:
                    vorgang_id = int(vorgang_id)
                except ValueError:
                    error = "Vorgang id conversion to int error! id= {}".format(vorgang_id)
                    return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
                else:
                    vorgang = Vorgang.objects.get(pk= vorgang_id)
                    netzplanvorgang.vorgang = vorgang
            #]
            if description:
                netzplanvorgang.description = description

            netzplanvorgang.save()
            return HttpResponseRedirect(reverse(ViewNetzplanVorgang_overview.URL_NAME))
        #]
        else:
            error = f"Input form error! Info: {netzplan_id}, {vorgang_id}, {description}"
            return render(request= request, template_name= "a10_error_info.html", context= {"error" : error})
    #}

#------------------------------------------------------------------------------------------------