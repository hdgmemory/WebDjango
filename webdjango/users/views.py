# -*- coding: utf-8 -*
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import User
import random
import urllib
import http.client
import json
from users.models import User
from django.contrib import  messages
from django.core.mail import send_mail
from cart.models import Order,Order_details
import datetime
from web.models import GoodsComment
#短信的主机地址
host  = "106.ihuyi.com"

#发送的地址
sms_send_uri = "/webservice/sms.php?method=Submit"

#账号
account  = "C55979412"

#秘钥
password = "d983ed9c00cdad7e2e4129ad867143cb"

def users_zhuce(request):
    return render(request,'users/users_zhuce.html')

def users_check(request):
    username = request.POST['value']
    result = User.objects.filter(username=username)
    if result:
        return HttpResponse(1)
    else:
        return HttpResponse(2)

def users_logindo(requset):
    username = requset.POST.get('username')
    userpass = requset.POST.get('userpass')
    result = User.objects.create(
        username=username,
        userpass=userpass
    )
    if result:
        return render(requset,'users/users_login.html')
    else:
        return HttpResponse('会员注册失败')

# 会员登录
def users_login(request):
    return render(request,'users/users_login.html')

def users_denglu(request):
    username = request.POST.get('username')
    userpass = request.POST.get('userpass')
    result = User.objects.filter(username=username,userpass=userpass)
    if result:
        user = User.objects.get(username=username, userpass=userpass)
        # 在session中保存一个前台会员的用户名 后台的叫username
        request.session['user'] = username
        request.session['uid'] = user.user_id
        # return render(request,"web/index.html")
        return redirect("/web/index")
    else:
        return redirect('/users/users_zhuce')

def users_logout(request):
    del request.session['user']
    del request.session['uid']
    return redirect('/users/users_login')

def phone_zhuce(request):
    # 显示视图
    return render(request,'users/phone_zhuce.html')

def send_message(request):
    # 发送验证码的逻辑代码
    mobile = request.POST.get('mobile')
    request.session['mobile']=mobile
    # 随机验证码
    message_code = ''
    for i in range(6):
        a = random.randint(0,9)
        message_code += str(a)
    text = "您的验证码是：" + message_code + "。请不要把验证码泄露给其他人。"
    # 请求的参数 第一个参数 账号 appid
    params = urllib.parse.urlencode({"account":account,"password":password,"content":text,"mobile":mobile,"format":"json"})
    # 请求的header头
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    # 连接
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    # 请求
    conn.request("POST", sms_send_uri, params, headers)
    # 获得呼应
    response = conn.getresponse()
    # 读取
    response_str = response.read()
    conn.close()
    # 把验证码放到一个变量中
    request.session['manage_code'] = message_code
    # 返回一个json格式
    return JsonResponse(eval(response_str.decode()))

def phone_zhucedo(request):
    mobile = request.POST.get('mobile')
    code = request.POST.get('code')
    userpass = request.POST.get('userpass')
    if code == request.session['manage_code']:
        result = User.objects.create(
            username = mobile,
            userpass = userpass
        )
        if result:
            del request.session['manage_code']
            return redirect('/users/users_login')
        else:
            return HttpResponse('注册失败')
    else:
        messages.add_message(request, messages.INFO, "验证码错误")
        return redirect("/users/phone_zhuce")

def phone_hedui(request):
    mobile = request.session['mobile']
    result = User.objects.filter(username=mobile).get()
    if result[0]==1:
        return HttpResponse(1)
    else:
        return HttpResponse(2)

def email_zhuce(request):
    return render(request,'users/email_zhuce.html')

def email_zhucedo(request):
    # 把user表添加一个字段 status  激活
    # 发送邮件   写入数据库
    username = request.POST.get('username')
    userpass = request.POST.get('userpass')
    result = User.objects.create(username=username,userpass=userpass)
    if result:
        # 发送邮件 第一个参数  主题   内容  发送者   接收者  不引发异常
        mail = send_mail("全球生鲜商城欢迎您的注册！","会员"+username+"你好！我们将竭诚服务!请尽快激活您的账号！http://localhost:8000/users/jihuo","18238795835@163.com",[username],fail_silently=True)
        # false 时候  send_email出现错误将引发异常
        print(mail)
        return HttpResponse('邮件发送成功')
    else:
        return redirect('/users/users_login')

def  jihuo(request):
    #激活的是谁
    return HttpResponse("激活成功")

def shouhuo(request,order_id):
    result = Order.objects.filter(order_id = order_id).update(order_status=3)
    if result:
        return redirect("/web/user_center")
    else:
        return HttpResponse("收货失败")

 #订单详情中
def comment(request,details_id):
    return render(request, "users/comment.html", {"details_id": details_id})

def commentdo(request):
    #评论人
    user_id = request.session.get("uid")
    #details_id
    details_id = request.POST.get("details_id")
    #评论内容
    comment_content = request.POST.get("comment_content")
    #店家
    details = Order_details.objects.filter(details_id = details_id).get()
    manage_id = details.manage_id
    #商品的id
    goods_id = details.goods_id
    #时间
    comment_time = datetime.datetime.now()
    result = GoodsComment.objects.create(
        user_id=user_id,
        details_id=details_id,
        comment_content=comment_content,
        manage_id=manage_id,
        goods_id=goods_id,
        comment_time=comment_time
    )

    #在订单详情表中添加一个status
    Order_details.objects.filter(details_id = details_id).update(status = 1)

    if result:
        return redirect("/web/user_center")
    else:
        return HttpResponse("评论失败")