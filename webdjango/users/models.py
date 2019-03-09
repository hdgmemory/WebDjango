from django.db import models

# Create your models here.
class User(models.Model):
    #会员id
    user_id = models.AutoField(auto_created=True,primary_key=True,db_column='user_id')
    #用户名
    username = models.CharField(max_length=50)
    #密码
    userpass = models.IntegerField()
