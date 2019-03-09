# -*- coding: utf-8 -*
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
# Create your views here.
from myshop.models import ManagerMessage
from goods.models import GoodsType,GoodsInfo
from cart.models import GoodsAddress,Order,Order_details,CartMessage
from web.models import GoodsComment
def openstore(request):
    return render(request,'web/openstore.html')

def openstoredo(request):
    #获取用户开店注册数据
    username = request.POST.get('username')
    shop_nickname = request.POST.get('shop_nickname')
    nickname = request.POST.get('nickname')
    shop_address = request.POST.get('shop_address')
    shop_logo = request.FILES.get('shop_logo')
    #把用户注册信息加入数据库
    result = ManagerMessage.objects.create(
        username = username,
        userpass = '000000',
        shop_nickname = shop_nickname,
        nickname = nickname,
        shop_address = shop_address,
        shop_logo = shop_logo,
    )
    if result:
        return render(request,'web/welcome.html')
    else:
        return HttpResponse('开店失败')

def index(request):
    #查询所有商品的信息
    list = GoodsInfo.objects.order_by('id')
    return render(request,'web/index.html',{'list':list})

def goods_detail(request,pk):
    #查询当前id商品的信息
    detail = GoodsInfo.objects.get(pk=pk)
    manage_id = detail.manage_id
    list = GoodsInfo.objects.filter(manage_id=manage_id).exclude(pk=pk).all()[0:2]
    # 查询的是该商品的所有评论信息
    sql = "select * from users_user inner join web_goodscomment on web_goodscomment.user_id = users_user.user_id where web_goodscomment.goods_id =" + str(pk)
    comment = GoodsComment.objects.raw(sql)
    return render(request,'web/goods_details.html',{'detail':detail,'list':list,"comment":comment})

def goods_type(request):
    goods_list = GoodsInfo.objects.all()
    type_list = GoodsType.objects.all()
    return render(request,'web/goods_type.html',{'goods_list':goods_list,'type_list':type_list})

def type_list(request,id):
    list = GoodsInfo.objects.filter(type_id=id).all()
    return render(request, 'web/goods_type.html', {'goods_list':list})

def order_xiang(request,address_id,order_id):
    address = GoodsAddress.objects.filter(address_id=address_id).get()
    # 当前点击的订单
    order = Order.objects.filter(order_id=order_id).get()
    order_detail = Order_details.objects.filter(order_id=order_id).all()
    if address:
        return render(request,'web/order_xiang.html',{'address':address,'order':order,'order_detail':order_detail})
    else:
        return HttpResponse('获取失败')

# 个人中心
def user_center(request):
    user_id = request.session.get('uid')
    order = Order.objects.filter(user_id=user_id).all()
    goods_list = Order_details.objects.all()
    return render(request,'web/user_center.html',{'order':order,'goods_list':goods_list})

def all_store(request):
    manage = ManagerMessage.objects.all()
    return render(request,'web/all_store.html',{'manage':manage})

def store_detail(request,manage_id):
    type = GoodsType.objects.all()
    goods_list = GoodsInfo.objects.filter(manage_id=manage_id).all()
    return render(request,'web/store_detail.html',{'type':type,'goods_list':goods_list,'manage_id':manage_id})
def store_type(request,manage_id,type_id):
    type = GoodsType.objects.filter(type_id=type_id).all()
    goods_list = GoodsInfo.objects.filter(type_id=type_id,manage_id=manage_id).all()
    return render(request, 'web/store_detail.html', {'type': type, 'goods_list': goods_list,'manage_id':manage_id})