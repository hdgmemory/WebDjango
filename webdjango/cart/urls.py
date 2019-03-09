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
url(r'cart_add/',views.cart_add,name='cart_add'),
url(r'cart_list/',views.cart_list,name='cart_list'),
url(r'cart_jian/(?P<id>\d+)',views.cart_jian,name='cart_jian'),
url(r'cart_jia/(?P<id>\d+)',views.cart_jia,name='cart_jia'),
url(r'cart_del/(?P<id>\d+)',views.cart_del,name='cart_del'),
url(r'cart_empty/',views.cart_empty,name='cart_empty'),
url(r'order_list/',views.order_list,name='order_list'),
url(r'order_add/',views.order_add,name='order_add'),
url(r'order_details/',views.order_details,name='order_details'),
url(r'chakan_order/',views.chakan_order,name='chakan_order'),
url(r'alipy/(?P<order_num>\d+)/(?P<total>\d+)',views.alipy,name='alipy'),
url(r'return_url/', views.return_url, name='return_url'),


]
