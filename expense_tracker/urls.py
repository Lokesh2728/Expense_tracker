"""
URL configuration for expense_tracker project.

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
from django.urls import path,include
from accounts.views import *
from expenses.views import *

from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("",TemplateView.as_view(template_name='home.html'),name='home'),
    path('register/', register, name='register'),
    path('otp_verification/', otp_verification, name='otp_verification'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
]
