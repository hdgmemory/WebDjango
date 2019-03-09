# -*- coding: utf-8 -*
from django.db import models
from goods.models import GoodsInfo
from myshop.models import ManagerMessage
from users.models import User
from django.utils import timezone
# Create your models here.

class CartMessage(models.Model):
    # 主键id
    cart_id = models.AutoField(auto_created=True,primary_key=True,db_column='cart_id')
    #商品数量
    num = models.IntegerField(default=0)
    #金额小计
    xiaoji = models.FloatField()
    #商品单价
    price = models.FloatField()
    #商品的外键
    goods = models.ForeignKey(GoodsInfo,db_column='goods_id')
    #用户会员的外键
    user = models.ForeignKey(User,db_column='user_id')
    #卖家的外键
    manage = models.ForeignKey(ManagerMessage,db_column='manage_id')

class GoodsAddress(models.Model):
    address_id = models.AutoField(auto_created=True,primary_key=True,db_column='address_id')
    uname = models.CharField(max_length=30)
    tel = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    user = models.ForeignKey(User,db_column='user_id')

class Order(models.Model):
    order_id = models.AutoField(auto_created=True,primary_key=True,db_column='order_id')
    user = models.ForeignKey(User,db_column='user_id',default='')
    order_time = models.DateTimeField(default=timezone.now)
    order_num = models.CharField(max_length=50)
    address = models.ForeignKey(GoodsAddress, db_column='address_id', default="")
    order_status = models.IntegerField(default=0)
    total = models.FloatField()

class Order_details(models.Model):
    details_id = models.AutoField(auto_created=True,primary_key=True,db_column='details_id')
    order = models.ForeignKey(Order,db_column='order_id',default="")
    goods = models.ForeignKey(GoodsInfo,db_column='goods_id',default="")
    manage = models.ForeignKey(ManagerMessage, db_column='manage_id')
    goods_name = models.CharField(max_length=200)
    goods_pic = models.CharField(max_length=200)
    goods_nprice = models.FloatField()
    goods_num = models.IntegerField()
    goods_xiaoji = models.FloatField()
    status = models.IntegerField(default=0)