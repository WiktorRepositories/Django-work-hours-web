from django.urls import path
from a11_informations.views import ViewMails_overview, ViewMail_modify, ViewMail_delete, ViewWorktimes_overview, ViewWorktime_modify, ViewWorktime_delete, ViewCountryISO_overview, ViewCountryISO_delete, ViewCountryISO_modify

urlpatterns = [
    path(route= "mails_overview/", view= ViewMails_overview.as_view(), name= "mails_overview"),
    path(route= "mail_delete/<int:id>", view= ViewMail_delete.as_view(), name= "mail_delete"),
    path(route= "mail_modify/<int:id>", view= ViewMail_modify.as_view(), name= "mail_modify"),

    path(route= "worktimes_overview/", view= ViewWorktimes_overview.as_view(), name= "worktimes_overview"),
    path(route= "worktime_delete/<int:id>", view= ViewWorktime_delete.as_view(), name= "worktime_delete"),
    path(route= "worktime_modify/<int:id>", view= ViewWorktime_modify.as_view(), name= "worktime_modify"),
    
    path(route= "countries_overview/", view= ViewCountryISO_overview.as_view(), name= "countries_overview"),
    path(route= "countries_delete/<int:id>", view= ViewCountryISO_delete.as_view(), name= "countries_delete"),
    path(route= "countries_modify/<int:id>", view= ViewCountryISO_modify.as_view(), name= "countries_modify"),
]