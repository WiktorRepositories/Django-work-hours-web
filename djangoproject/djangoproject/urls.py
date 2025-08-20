"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
# from djangoproject.views import main_page

urlpatterns = [
    path('admin/', admin.site.urls),
    #
    path("", TemplateView.as_view(template_name="main_page.html"), name="home"),
    # path("", main_page, name="home"),
    #
    path("a00_accounts/", include("a00_accounts.urls")),
    path("a10_topics/", include("a10_topics.urls")),
    path("a11_informations/", include("a11_informations.urls")),
    path("a20_users/", include("a20_users.urls")),
]
