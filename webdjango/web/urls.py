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
   url(r'openstore/',views.openstore,name='openstore'),
   url(r'openstoredo/', views.openstoredo, name='openstoredo'),
   url(r'index/',views.index,name='index'),
   url(r'goods_detail/(?P<pk>\d+)',views.goods_detail,name='goods_detail'),
   url(r'goods_type/',views.goods_type,name='goods_type'),
   url(r'type_list/(?P<id>\d+)',views.type_list,name='type_list'),
   url(r'type_list/(?P<id>\d+)',views.type_list,name='type_list'),
   url(r'order_xiang/(?P<address_id>\d+)/(?P<order_id>\d+)',views.order_xiang,name='order_xiang'),
   url(r'user_center',views.user_center,name='user_center'),
   url(r'all_store',views.all_store,name='all_store'),
   url(r'store_detail/(?P<manage_id>\d+)',views.store_detail,name='store_detail'),
   url(r'store_type/(?P<manage_id>\d+)/(?P<type_id>\d+)',views.store_type,name='store_type'),


]
