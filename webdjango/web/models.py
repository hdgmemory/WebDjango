from django.db import models
from goods.models import GoodsInfo,ManagerMessage
from users.models import  User
from django.utils import timezone
from cart.models import Order_details
# Create your models here.
class GoodsComment(models.Model):
    #主键
    comment_id = models.AutoField(auto_created=True,primary_key=True,db_column='comment_id')
    #商品的外键
    goods = models.ForeignKey(GoodsInfo,db_column="goods_id")
    #评论人
    user = models.ForeignKey(User,db_column="user_id")
    #评论内容
    comment_content = models.TextField()
    #评论时间
    comment_time = models.DateTimeField(default=timezone.now)
    #回复
    huifu = models.CharField(max_length=200)
    #评论状态
    status = models.IntegerField(default=0)
    #卖家
    manage = models.ForeignKey(ManagerMessage,db_column="manage_id")
    #订单的外键
    details = models.ForeignKey(Order_details,db_column="details_id")