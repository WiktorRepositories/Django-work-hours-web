from django.views import View
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
#***************************************************************************
# Main page view
def main_page(request:HttpRequest):
    return render(request= request, template_name= "main_page.html", context= {"TAB_NAME" : "Home Page"})
#===========================================================================