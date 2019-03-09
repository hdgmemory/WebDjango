"""webdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'users_zhuce/',views.users_zhuce,name='users_zhuce'),
    url(r'users_logindo/',views.users_logindo,name='users_logindo'),
    url(r'users_check/',views.users_check,name='users_check'),
    url(r'users_login/',views.users_login,name='users_login'),
    url(r'users_denglu/',views.users_denglu,name='users_denglu'),
    url(r'users_logout/',views.users_logout,name='users_logout'),
    url(r'phone_zhuce/',views.phone_zhuce,name='phone_zhuce'),
    url(r'send_message/',views.send_message,name='send_message'),
    url(r'phone_zhucedo/',views.phone_zhucedo,name='phone_zhucedo'),
    url(r'phone_hedui/',views.phone_hedui,name='phone_hedui'),
    url(r'email_zhuce/', views.email_zhuce,name="email_zhuce"),
    url(r'email_zhucedo/', views.email_zhucedo,name="email_zhucedo"),
    url(r'jihuo/', views.jihuo,name="jihuo"),
    url(r'shouhuo/(?P<order_id>\d+)', views.shouhuo,name="shouhuo"),
    url(r'comment/(?P<details_id>\d+)', views.comment,name="comment"),
    url(r'commentdo', views.commentdo,name="commentdo"),



]
