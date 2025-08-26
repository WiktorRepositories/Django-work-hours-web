from django.urls import path
from a20_users.views import ViewAdminAllHours_overview, ViewAdminAllHours_modify, ViewAdminAllHours_delete
from a20_users.views import ViewUserWeek_overview, ViewUserCurrentDay_delete ,ViewAdminAllHours_overview
from a20_users.views import ViewUserCurrentDay_modify, ViewUserCurrentDay_delete, ViewUserCurrentDay_overwiev, view_user_cooperation_get

urlpatterns = [
    path(route= "week_overview_grouby/",       view= ViewUserWeek_overview.as_view(),  name= "week_overview_grouby"),
    path(route= "xday_overview/<str:cd>",  view= ViewUserCurrentDay_overwiev.as_view(),name= "xday_overview"),
    path(route= "xday_modify/<int:id>/<str:cd>",view= ViewUserCurrentDay_modify.as_view(),  name= "xday_modify"),
    path(route= "xday_delete/<int:id>/<str:cd>",view= ViewUserCurrentDay_delete.as_view(),  name= "xday_delete"),

    path(route= "all_hours_overview/",      view=ViewAdminAllHours_overview.as_view(),name= "all_hours_overview"),
    path(route= "all_hours_modify/<int:id>",view=ViewAdminAllHours_modify.as_view(), name= "all_hours_modify"),
    
    path(route= "user_connections_overview/",view= view_user_cooperation_get, name= "user_connections_overview"),
]