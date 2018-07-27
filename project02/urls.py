"""project02 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from DataServer.views import logindb ,dbreadrest,getdata,gettoken,getefficiency,getdatadetail
from DataServer import views
from DataServer.userquery import userquery


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logindb/', views.logindb),
    path('login/', views.login),
    path('dbreadrest/', dbreadrest.as_view()),
    path('getdata/',getdata.as_view()),
    path('gettoken/',views.gettoken),
    path('getefficiency/',getefficiency.as_view()),
    path('getdatadetail/',getdatadetail.as_view()),
    path('userquery/',userquery.as_view()),
]
