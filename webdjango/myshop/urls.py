from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'main/',views.main,name='main'),
    url(r'login/',views.login,name='login'),
    url(r'logindo/',views.logindo,name='logindo'),
    url(r'loginout/',views.loginout,name='loginout'),
    url(r'dingdan_list/',views.dingdan_list,name='dingdan_list'),
    url(r'dingdan_detail/(?P<order_id>\d+)/(?P<address_id>\d+)',views.dingdan_detail,name='dingdan_detail'),
    url(r'manage_status/',views.manage_status,name='manage_status'),
    url(r'manage_comment/',views.manage_comment,name='manage_comment'),
    url(r'manage_commentdo/(?P<comment_id>\d+)/(?P<details_id>\d+)',views.manage_commentdo,name='manage_commentdo'),
    url(r'comment_huifudo/', views.comment_huifudo, name='comment_huifudo'),
    url(r'verify_code/', views.verify_code, name='verify_code'),
    url(r'check_code/', views.check_code, name='check_code'),
]
