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
from django.urls import path,re_path
from accounts.views import *
from expenses.views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("",home,name='home'),
    path('register/', register, name='register'),
    path('otp_verification/', otp_verification, name='otp_verification'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('Reset_Password/',Reset_Password,name='Reset_Password'),
    path('Balanceview',Balanceview.as_view(),name='Balanceview'),
    path('change_password/',change_password,name='change_password'),
    path('set-new-password/',set_new_password, name='set_new_password'),
    path('set_budget/',set_budget,name='set_budget'),
    path('dashboard/',dashboard,name='dashboard'),
    path('Profile/',Profile,name='Profile'),



    path('AddExpense/',AddExpense.as_view(),name='AddExpense'),
    path('ExpenseList/',ExpenseList.as_view(),name='ExpenseList'),
    re_path(r'^update/(?P<pk>\d+)/$', Expense_Update.as_view(), name='update'),
    re_path(r'^delete/(?P<pk>\d+)/$', Expense_Delete.as_view(), name='delete'),


]
