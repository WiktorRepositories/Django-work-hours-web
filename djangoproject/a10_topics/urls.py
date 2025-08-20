from django.urls import path
from a10_topics.views import ViewProjectMachines_overview, ViewProjectMachine_modify, ViewProjectMachine_delete, ViewNetzplan_overview, ViewNetzplan_modify, ViewNetzplan_delete, ViewVorgang_overview, ViewVorgang_delete, ViewVorgang_modify, ViewNetzplanVorgang_overview, ViewNetzplanVorgang_delete, ViewNetzplanVorgang_modify, ViewProjectCooperation_overview

urlpatterns = [
    # URLS for machine data menagment
    path(route= "machines_overview/",       view= ViewProjectMachines_overview.as_view(), name= "machines_overview"),
    path(route= "machine_delete/<int:id>",  view= ViewProjectMachine_delete.as_view(),    name= "machine_delete"),
    path(route= "machine_modify/<int:id>",  view= ViewProjectMachine_modify.as_view(),    name= "machine_modify"),

    # URLS for work types data menagment
    path(route= "netzplan_overview/",      view= ViewNetzplan_overview.as_view(), name= "netzplan_overview"),
    path(route= "netzplan_delete/<int:id>",view= ViewNetzplan_delete.as_view(),   name= "netzplan_delete"),
    path(route= "netzplan_modify/<int:id>",view= ViewNetzplan_modify.as_view(),   name= "netzplan_modify"),

    # URLS for work data data menagment
    path(route= "vorgang_overview/",     view= ViewVorgang_overview.as_view(),  name= "vorgang_overview"),
    path(route= "vorgang_delete/<int:id>",view= ViewVorgang_delete.as_view(),    name= "vorgang_delete"),
    path(route= "vorgang_modify/<int:id>",view= ViewVorgang_modify.as_view(),    name= "vorgang_modify"),


    path(route= "netzplanvorgang_overview/", view= ViewNetzplanVorgang_overview.as_view(), name= "netzplanvorgang_overview"),
    path(route= "netzplanvorgang_delete/<int:id>", view= ViewNetzplanVorgang_delete.as_view(), name= "netzplanvorgang_delete"),
    path(route= "netzplanvorgang_modify/<int:id>", view= ViewNetzplanVorgang_modify.as_view(), name= "netzplanvorgang_modify"),


    path(route= "project_connections/", view= ViewProjectCooperation_overview.as_view(), name= "project_connections"),
]