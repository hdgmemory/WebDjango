
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import ManagerMessage
from cart.models import Order,Order_details,GoodsAddress
from goods.models import GoodsInfo
from web.models import GoodsComment
from PIL import Image,ImageDraw,ImageFont
import random,json
from io import  BytesIO
# Create your views here.
def main(request):
    manage_id = request.session.get("manage_id")
    sql = "select  distinct d.order_id  from cart_order as d inner join cart_order_details as x on d.order_id = x.order_id where x.manage_id = " + str(manage_id)
    order = Order.objects.raw(sql)
    count = 0
    for i in order:
        count = count + 1
    print(count)
    goods_num = GoodsInfo.objects.filter(manage_id=manage_id).count()
    return render(request, "manager/main.html", {"goods_num": goods_num, "count": count})
# 卖家登录模板页面
def login(request):
    return  render(request,'manager/login.html')
# 卖家登录实现功能
def logindo(request):
    #获取用户名
    username = request.POST.get('username')
    userpass = request.POST.get('userpass')
    # 查询数据库中是否有这个用户名
    result = ManagerMessage.objects.get(username=username,userpass=userpass)
    manage_id = ManagerMessage.objects.get(username=username,userpass=userpass).id
    if result:
        # 把用户信息存储到session中
        request.session['username'] = username
        request.session['manage_id'] = manage_id
        return redirect('/myshop/main')
    else:
        return HttpResponse('登录失败')
# 注销用户
def loginout(request):
    del request.session['username']
    return redirect('/myshop/login')

def dingdan_list(request):
    manage_id = request.session.get('manage_id')
    sql = "select  distinct d.order_id,d.order_num,d.order_time,d.order_status,d.address_id  from cart_order as d inner join cart_order_details as x on d.order_id = x.order_id where x.manage_id = " + str(manage_id)
    number = Order.objects.raw(sql)
    # get传值前台模板传递的page参数  如果没有 默认值是1
    page = request.GET.get("page", 1)
    page = int(page)
    # 一页显示几条
    show = 1
    # limit show*(page-1),show

    # 如果有3条数据  一页显示2条    一共有2页
    # 如果有3条数  一页显示1条  一共有3页

    # 一共有几条数据
    count = 0
    for i in number:
        count += 1
    # print(count)

    # 判断页数 num_page
    if count % show == 0:
        # 整除了
        num_page = count / show
    else:
        # 没整除
        num_page = count // show + 1

    # print(num_page)
    num_page = int(num_page)
    # 判断是否有上一页
    if page == 1:  # 如果我是第一页
        has_pre = False
    else:
        has_pre = True

    # 判断是否有下一页
    if page == num_page:
        has_next = False
    else:
        has_next = True

    # 正常点击下一页
    next_page = page + 1

    # 正常点击上一页
    pre_page = page - 1

    # 出现页码
    range_page = range(1, num_page + 1)  # 123

    order = Order.objects.raw("select  distinct d.order_id,d.order_num,d.order_time,d.order_status,d.address_id  from cart_order as d inner join cart_order_details as x on d.order_id = x.order_id where x.manage_id =%s order by d.order_id desc limit %s,%s",[str(manage_id), (page - 1) * show, show])

    return render(request, "manager/order_list.html", locals())
    # return render(request,'manager/order_list.html',{'result':result})




def dingdan_detail(request,order_id,address_id):
    manage_id = request.session.get('manage_id')
    order_detail = Order_details.objects.filter(manage_id=manage_id,order_id=order_id).all()
    add = GoodsAddress.objects.filter(address_id=address_id).get()
    order = Order.objects.filter(order_id=order_id).get()
    return  render(request,'manager/order_detail.html',{"order_detail":order_detail,'add':add,'order':order})

def manage_status(request):
    order_id = request.POST.get('order_id')
    result = Order.objects.filter(order_id=order_id).update(
        order_status = 2
    )
    if result:
        return redirect('/myshop/dingdan_list')
    else:
        return HttpResponse('发货失败')

def manage_comment(request):
    # 评论人  #商品图片  商品名  回复 评论内容   评论时间  操作
    manage_id = request.session.get("manage_id")
    sql = "select * from web_goodscomment inner join users_user on web_goodscomment.user_id = users_user.user_id inner join goods_goodsinfo on web_goodscomment.goods_id = goods_goodsinfo.id where web_goodscomment.manage_id =" + str(manage_id)
    result = GoodsComment.objects.raw(sql)
    return render(request, "manager/manage_comment.html", {"result": result})

def manage_commentdo(request,comment_id,details_id):
    return render(request, "manager/comment_huifu.html", {"comment_id": comment_id, "details_id": details_id})

def comment_huifudo(request):
    comment_id = request.POST.get("comment_id")
    details_id = request.POST.get("details_id")
    huifu = request.POST.get("huifu")
    result = GoodsComment.objects.filter(comment_id=comment_id).update(
        status=1,
        huifu=huifu
    )
    Order_details.objects.filter(details_id=details_id).update(status=2)

    if result:
        return redirect("/myshop/manage_comment")
    else:
        return HttpResponse(1)

def verify_code(request):
    # 验证码的宽度
    width = 100
    # 高度
    height = 50

    # 创建画布 三个参数 mode "RGB" size 大小  颜色
    img = Image.new("RGB", (width, height), (random.randint(0,100),random.randint(0,100),random.randint(0,255)))

    # 第二个画板
    draw = ImageDraw.Draw(img)

    # 验证码的备选值
    str = "ABCDEFGHJKLMNPQRSTWXYZ123456789abcdefghjklmnpqrstwxyz"

    # 引入字体 simkai.ttf 楷体gb2312  40 字号
    # font = ImageFont.truetype("simkai.ttf", 40)
    font = ImageFont.truetype("STHeiti Medium.ttc", 40)
    # 定义一个装验证码的容器
    code_str = ""
    # 起始位置
    position = 5

    # 2.加入随机的干扰点
    for i in range(0, 150):
        xy = (random.randrange(0, 100), random.randrange(0, 25))
        # 干扰点的颜色
        fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))

        # draw.point(xy,options)

        draw.point(xy, fill=fill)


        # 3.干扰线
    for i in range(0, 50):
        color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        x, y = random.randrange(0, 100), random.randrange(0, 50)
        m, n = random.randrange(0, 100), random.randrange(0, 50)
        draw.line(((x, y), (m, n)), fill=color)

    # 4生成文字
    for i in range(0, random.randrange(4, 6)):
        # 随机的字体  20    0,20
        code = str[random.randrange(0, len(str))]
        # 字体的颜色
        fontColor = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        # 位置   验证码  操作
        draw.text((position, 0), code, font=font, fill=fontColor)
        position += 20
        code_str += code
    # 5保存图片
    io = BytesIO()
    # 写入内存
    img.save(io, "png")

    # 保存到session中
    request.session['verify_code'] = code_str.lower()

    return HttpResponse(io.getvalue(), "image/png")

#只是提供ajax 提交地址的验证
def check_code(request):
    # 比对存入session的验证码和用户输入的验证码是否一致
    code = request.GET.get("code")
    newcode = request.session['verify_code']
    # 将用户输入的变成小写
    code = code.lower()
    data = {}
    if code == "":
        data['msg'] = "验证码不能为空"
        data['status'] = 0
        return HttpResponse(json.dumps(data))

    if code == newcode:
        data['msg'] = "验证码正确"
        data['status'] = 1
        return HttpResponse(json.dumps(data))
    else:
        data['msg'] = "验证码错误"
        data['status'] = 0
        # return JsonResponse(data)
        return HttpResponse(json.dumps(data))
