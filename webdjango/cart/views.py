
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from users.models import User
from cart.models import CartMessage,GoodsAddress,Order,Order_details
from django.db.models import Sum
from .models import CartMessage
import datetime
from django.utils import timezone
import random
# 客服端配置
from alipay.aop.api.AlipayClientConfig import  AlipayClientConfig
# 默认配置
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
# 数据层模型
from alipay.aop.api.domain.AlipayTradePagePayModel import  AlipayTradePagePayModel
# 数据请求
from  alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest



#把购买商品加到购物车
def cart_add(request):
    #判断用户是否登录
    user = request.session.get('user')
    if user==None:
        return redirect('/users/users_login')
    else:
        #如果登录了，把信息存到购物车数据库
        num = request.POST['num']
        price = request.POST.get('price')
        goods_id = request.POST.get('goods_id')
        user_id = request.session.get('uid')
        manage_id = request.POST.get('manage_id')
        print(type(num))
        xiaoji = int(num) * float(price)
        #判断同一用户是否购买过该商品

        count = CartMessage.objects.filter(goods_id=goods_id,user_id=user_id).count()
        if count>0:
            manage = CartMessage.objects.get(goods_id=goods_id,user_id=user_id)
            manage.num = int(manage.num)+int(num)
            manage.xiaoji = manage.num * manage.price
            manage.save()
        else:
             CartMessage.objects.create(
                num=num,
                price=price,
                goods_id=goods_id,
                user_id = user_id,
                manage_id=manage_id,
                xiaoji=xiaoji
            )
        return redirect('/cart/cart_list')
# 购物车列表
def cart_list(request):
    #先获取用户存储在session的id
    user_id = request.session.get('uid')
    if user_id==None:
        return redirect('users/login')
    else:
        cart_list = CartMessage.objects.raw("select * from cart_cartmessage inner join goods_goodsinfo on cart_cartmessage.goods_id  = goods_goodsinfo.id where cart_cartmessage.user_id="+str(user_id))
        sum = CartMessage.objects.filter(user_id=user_id).all().aggregate(total=Sum('xiaoji'))
        return render(request,'cart/cart_list.html',{'cart_list':cart_list,'sum':sum})
# 对商品数量进行加
def cart_jian(request,id):
    cart = CartMessage.objects.get(cart_id=id)
    #如果只有一个就删除，有多个的话就减一
    if cart.num==1:
        cart.delete()
    else:
        cart.num = cart.num -1
        cart.xiaoji = int(cart.num)*float(cart.price)
        cart.save()
    return redirect('cart/cart_list')
# 对商品数量进行加
def cart_jia(request,id):
    cart = CartMessage.objects.get(cart_id=id)
    #如果只有一个就删除，有多个的话就减一
    cart.num = cart.num + 1
    cart.xiaoji = int(cart.num)*float(cart.price)
    cart.save()
    return redirect('cart/cart_list')
# 删除商品
def cart_del(request,id):
    cart = CartMessage.objects.filter(cart_id=id).delete()
    if cart:
        return redirect('cart/cart_list')
    else:
        return HttpResponse('删除失败')
# 清空购物车
def cart_empty(request):
    user_id = request.session.get('uid')
    cart = CartMessage.objects.filter(user_id=user_id).all().delete()
    if cart:
        return redirect('/cart/cart_list')
    else:
        return HttpResponse('删除失败')
# 提交订单
def order_list(request):
    user_id = request.session.get('uid')
    count = CartMessage.objects.filter(user_id=user_id).count()
    if count==0:
        return HttpResponse('请先购物，再下订单')
    else:
        if user_id ==None:
            return redirect('/users/users_login')
        else:
            adress = GoodsAddress.objects.filter(user_id=user_id).all()
            cart = CartMessage.objects.raw("select * from cart_cartmessage inner join goods_goodsinfo on cart_cartmessage.goods_id  = goods_goodsinfo.id where cart_cartmessage.user_id=" + str(user_id))
            sum = CartMessage.objects.filter(user_id=user_id).all().aggregate(total=Sum('xiaoji'))
            return render(request,'cart/order_list.html',{'adress':adress,'cart':cart,'sum':sum})

# 添加订单到数据库
def order_add(request):
    user_id = request.session.get('uid')
    count = GoodsAddress.objects.filter(user_id=user_id).count()
    if count==0:
        return HttpResponse('请先添加收货地址')
    else:
        address_id = request.POST.get('address')
        order_status = 0
        user_id = user_id
        total = request.POST.get('total')
        order_num = timezone.now().strftime("%Y%m%d%H%M%S")+str(random.randint(1000,999999))
        order_time = datetime.datetime.now()
        result = Order.objects.create(
            address_id=address_id,
            order_status=order_status,
            user_id=user_id,
            total=total,
            order_num=order_num,
            order_time=order_time
        )
        if result:
            return redirect('/cart/order_details')
        else:
            return HttpResponse('添加订单失败')

# 订单详情
def order_details(request):
    user_id = request.session.get('uid')
    order = Order.objects.filter(user_id=user_id).last()
    order_id = order.order_id
    cart = CartMessage.objects.raw("select * from cart_cartmessage inner join goods_goodsinfo on cart_cartmessage.goods_id  = goods_goodsinfo.id where cart_cartmessage.user_id=" + str(user_id))
    for cart in cart:
        result = Order_details.objects.create(
            goods_name=cart.goods_name,
            goods_pic=cart.goods_pic,
            goods_nprice=cart.goods_price,
            goods_num=cart.num,
            goods_xiaoji=cart.xiaoji,
            goods_id=cart.goods_id,
            manage_id=cart.manage_id,
            order_id=order_id
        )
        if result:
            CartMessage.objects.filter(user_id=user_id).all().delete()
            return redirect('/cart/chakan_order/')
        else:
            return HttpResponse('订单提交失败')

def chakan_order(request):
    user_id = request.session.get('uid')
    if user_id==None:
        redirect('/users/users_login')
    else:
        order = Order.objects.filter(user_id=user_id).last()
        return render(request,'cart/chakan_order.html',{'order':order})

# 测试支付
def alipy(request,order_num,total):
    # 导入配置类
    alipy = AlipayClientConfig()
    # 支付宝的网关
    alipy.server_url ='https://openapi.alipaydev.com/gateway.do'
    # 商家APPID
    alipy.app_id = '2016092000556084'
    # 支付宝的私钥
    alipy.app_private_key = 'MIIEpgIBAAKCAQEAzfsgTn6BAcTMRg4P5cbtcNgN0kQLkOVA2DGhrY+nIcXkzL5IjDdR85ck/dIslv/TeESyHbF48ssS9CiBS6YUASiDa1bDv5A94GWos4FgFM4a8fKx4fc2QXhSY4rG+zIJAVSctwKnDTt0S8VtycS7GBu9uTAthLz4wZKNQexi1W6dSLkj7SDlYapR2zlmF+3NSB8ID52k7cQuPFR+tJSa0SMt0Q6w1kzjJmPDBW8tNo2lqGq9OguefZz4+wnGacaTjzB+e/P1Ni5oIc8L9JJyXfu3qUTop1QgogIOjCRAtM4RpQIp+GIGs72kljnosPqlUfn8kjBo9Ndj7SfzDoBpcQIDAQABAoIBAQCijsLDT9DuHWr9CpH/TAwNV2UpAOyD0HlpZVnsSIek/rF/59gHWI1DiY/3BMyN6p3wt34+MtZ5/kwaBnFry0jUVS3KI3Jely5ODsyhxcOXB8V6FofOBjR6XMPgrSA2FBnJRAZd5CkEJ1yzg78OUkU5VINZSC1UKXLECa2TTkP9nWDpnbWz37vvyZtZ+JtJvNcxwr7Bjw+HkZ7TxAqCMOqe6Avs7KkSCJXBOPXP+t/GyEgFKnwexVFuhUr4XcgzLrCo5+lQk0cXxTfn4rMC9h90y7onUZxxCL02dvVJ9q2Y5cklCnvkqvRG2k2tqPNQx4Fz4YuHtLuUuoYm9FhKJyoFAoGBAOfUVMGcSKzotZ9NuxTiwiPEKymhbPfSlR9E9pjiaEfylq9TLwN6omKZxSV4IZufXE319dHYDNiOG5UsZ5f9/ZouXxNuLCYqkB2i70wPNlaMVo3PcJ12f24puVXV2FxGu4wrdF7Xi/BFM68qy6xCRa08PFapstD+wy3//zQEPz5/AoGBAON04k5cZlwziNgh5gQFeu5OsyZcqNF2jGHAfuzfgV6GzuyJe5Df24tOSQqCMAucVIaJyHfF3ydnkKq99uGxJlcApNIluAz/7P3lAbgtGqSLBdwaERighfyiWF+dN4HGpiszBgAnJxvDdPbzA0eQxWum6eA/jaif10lEZ2XC1EAPAoGBAKy5KhzGD++jwg3aoBRDjlmPgokV2FYb8zbE7uWhagiQ2WvvEgwJhorn/laYVpHX/bGoG2opCgked7aAyv4XIqeI/RVA9GvLMmyiRJ/qhZWeIa6uaz0mWHL/azJkjTrTCFC634z6Ey0EoilUPUMubTNQubPn426LIWhYXw+mSmiJAoGBAMt+wg1LW4S30oFTap9Ea+QS4vK6SYsE3bmC58tydyKjxzMWGUfXD2tFgdF2AhgRKAop8QE/NVPisyoexGbM/7ks6Ujd2BlBSr0oCm7FY6W8f2SYqZz32IfakugQFx3zJK1Xe9HdNX8AUn+xkMiRPB8A+RLYqRsozgpNuZfwQ8Z/AoGBALb+uPBKRsaxC1q6jkL0MaeGNiCqO+StLCVMoFbTjatSrmw2wt386Qo0DYii+cS1KIXFixZJuw1m3vm4WR5JgoRj477xNVJTUFb/A/GMCLcum9IajLnuD+aqdV3vpGmpQdECsi1sbTMalcjaFozbZLkaJIB5akpfl//A+5UIbRbk'
    # 支付宝的公钥
    alipy.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzfsgTn6BAcTMRg4P5cbtcNgN0kQLkOVA2DGhrY+nIcXkzL5IjDdR85ck/dIslv/TeESyHbF48ssS9CiBS6YUASiDa1bDv5A94GWos4FgFM4a8fKx4fc2QXhSY4rG+zIJAVSctwKnDTt0S8VtycS7GBu9uTAthLz4wZKNQexi1W6dSLkj7SDlYapR2zlmF+3NSB8ID52k7cQuPFR+tJSa0SMt0Q6w1kzjJmPDBW8tNo2lqGq9OguefZz4+wnGacaTjzB+e/P1Ni5oIc8L9JJyXfu3qUTop1QgogIOjCRAtM4RpQIp+GIGs72kljnosPqlUfn8kjBo9Ndj7SfzDoBpcQIDAQAB'
    # 设置默认的客户端配置
    client = DefaultAlipayClient(alipay_client_config=alipy)
    # 订单号
    order_num = order_num

    if order_num == "":
        return HttpResponse("请确认订单号正确")

    # 判断用户的登录状态
    user_id = request.session.get("uid")
    if user_id == None:
        return redirect("/users/user_login")

    # 查询当前用户购买的订单
    order_info = Order.objects.filter(order_num=order_num, user_id=user_id).get()

    # 判断此订单是否有效
    # print(order_info)
    # return HttpResponse("1")
    if not order_info:
        return HttpResponse("订单有误")

    # 请求数据交易层模型
    model = AlipayTradePagePayModel()
    # 订单号
    model.out_trade_no = order_info.order_num
    # 订单的金额
    model.total_amount = total
    # 标题
    model.subject = "测试支付金额"
    # 订单描述
    model.body = "这是一个巨款订单"
    # 销售的产品码
    model.product_code = "FAST_INSTANT_TRADE_PAY"

    # 交易请求
    qingqiu = AlipayTradePagePayRequest(biz_model=model)

    # 发送上一步的请求  第一个参数是qingqiu  第二个是发送的方式
    # localhost:8000/cart/aliapy?2343243243&111
    # 回调地址
    #qingqiu.return_url = "http://47.107.229.163/cart/return_url/"
    qingqiu.return_url = "http://127.0.0.1:8000/cart/return_url/"
    xiangying = client.page_execute(qingqiu, http_method="GET")

    # print(xiangying)

    # return  HttpResponse(1)
    return redirect(xiangying)


# 从支付调回的地址 http://localhost:8000/cart/sss
def return_url(request):
    # 扫码成功 逻辑是
    # 得到上一步传递的参数
    order_num = request.GET.get("out_trade_no")

    result = Order.objects.filter(order_num=order_num).update(order_status=1)
    if result:
        return HttpResponse('支付成功')
    else:
        return HttpResponse("支付失败")

