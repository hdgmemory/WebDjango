from django.db import models

# Create your models here.

class ManagerMessage(models.Model):
    username = models.CharField(max_length=50,default='')
    userpass = models.CharField(max_length=50,default='')
    # 卖家显示昵称
    nickname = models.CharField(max_length=100,null=True,default='')
    # 卖家店铺昵称
    shop_nickname = models.CharField(max_length=100,null=True,default='')
    # 店铺logo
    shop_logo = models.ImageField(max_length=100,upload_to='uploads',null=True,default='')
    # 店铺地址
    shop_address = models.CharField(max_length=100,null=True,default='')
