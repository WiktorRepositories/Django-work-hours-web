from django.urls import path
from a00_accounts.views import ViewsUserRegister, ViewsUserLogin, viewsUserLogout, ViewsAllUsersData, ViewUserDelete, ViewUserModify
from a00_accounts.views import view_userRegister, view_ShowUser, ViewAdminUserSettings_overview, ViewAdminUserSettings_modify
from a00_accounts.views import ViewUsersConnections_overview, ViewUsersConnections_delete, ViewUsersConnections_modify

urlpatterns = [
    path(route= "account_register/",    view= ViewsUserRegister.as_view(),  name= "account_register"),
    path(route= "account_login/",       view= ViewsUserLogin.as_view(),     name= "account_login"),
    path(route= "account_logout/",      view= viewsUserLogout,    name= "account_logout"),

    path(route= "welcome_user/<str:us>/<str:ac>/", view= view_ShowUser, name="welcome_user"),

    path(route= "admin_users_overview/",view=ViewsAllUsersData.as_view(),   name= "admin_users_overview"),
    path(route= "admin_user_delete/<int:id>",view=ViewUserDelete.as_view(),   name= "admin_user_delete"),
    path(route= "admin_user_modify/<int:id>",view=ViewUserModify.as_view(),   name= "admin_user_modify"),

    # View all user settings 
    path(route= "admin_usr_sett_overview/", view= ViewAdminUserSettings_overview.as_view(), name="admin_usr_sett_overview"),
    # path(route= "admin_usr_sett_delete/<int:id>", view= ViewAdminUserSettings_delete.as_view(), name="admin_usr_sett_delete"),
    path(route= "admin_usr_sett_modify/<int:id>", view= ViewAdminUserSettings_modify.as_view(), name="admin_usr_sett_modify"),

    path(route= "users_connections_overview/", view= ViewUsersConnections_overview.as_view(), name= "users_connections_overview"),
    path(route= "users_connections_delete/<int:id>/", view= ViewUsersConnections_delete.as_view(), name= "users_connections_delete"),
    path(route= "users_connections_modify/<int:id>/", view= ViewUsersConnections_modify.as_view(), name= "users_connections_modify"),
]