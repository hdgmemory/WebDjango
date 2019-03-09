from django.db import models
from myshop.models import ManagerMessage

# Create your models here.
class GoodsType(models.Model):
    type_id = models.AutoField(auto_created=True,primary_key=True,default=0,db_column='type_id')
    type_name = models.CharField(max_length=50)
    type_sort = models.IntegerField(default=0)

class GoodsInfo(models.Model):
    goods_name = models.CharField(max_length=50,default='')
    goods_price = models.FloatField()
    goods_xprice = models.FloatField()
    goods_count = models.IntegerField(default='0')
    goods_info = models.CharField(max_length=50)
    goods_pic = models.ImageField(default='',upload_to='media/uploads')
    goods_method = models.CharField(default='',max_length=50)
    goods_address = models.CharField(default='',max_length=100)
    goods_content = models.TextField()
    manage = models.ForeignKey(ManagerMessage,default='',db_column='manage_id')
    type = models.ForeignKey(GoodsType,db_column='type_id')