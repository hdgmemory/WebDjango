from django.conf.urls import url, include
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'goods_list/',views.goods_list,name='goods_list'),
    url(r'goods_add/',views.goods_add,name='goods_add'),
    url(r'goods_addo/',views.goods_addo,name='goods_addo'),
    # url(r'delete/(?P<id>\d+)',views.delete,name='delete'),
    url(r'update/(?P<id>\d+)',views.update,name='update'),
    url(r'edit/',views.edit,name='edit'),
    url(r'dele',views.dele,name='dele')
]
