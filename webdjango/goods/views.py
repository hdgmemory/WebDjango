# -*- coding: utf-8 -*
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import GoodsInfo,GoodsType
from django.conf import settings
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
def goods_list(request):
    list = GoodsInfo.objects.order_by('-id')
    manage_id = str(request.session['manage_id'])
    list = GoodsInfo.objects.raw('select * from goods_goodsinfo,goods_goodstype where goods_goodsinfo.type_id=goods_goodstype.type_id and goods_goodsinfo.manage_id='+manage_id)
    return  render(request,'goods/goods_list.html',{'list':list})

def goods_add(request):
    list = GoodsType.objects.all()
    return render(request,'goods/goods_add.html',{'list':list})
def goods_addo(request):
    goods_name = request.POST.get('goods_name')
    goods_price = request.POST.get('goods_price')
    goods_xprice = request.POST.get('goods_xprice')
    goods_count = request.POST.get('goods_count')
    goods_method = request.POST.get('goods_method')
    goods_info = request.POST.get('goods_info')
    goods_address = request.POST.get('goods_address')
    goods_content = request.POST.get('goods_content')
    type_id = request.POST.get('type_id')
    manage_id = request.session['manage_id']
    goods_pic = request.FILES.get('goods_pic')

    result = GoodsInfo.objects.create(
        goods_name = goods_name,
        goods_price = goods_price,
        goods_xprice = goods_xprice,
        goods_count = goods_count,
        goods_method = goods_method,
        goods_info = goods_info,
        type_id = type_id,
        manage_id = manage_id,
        goods_address = goods_address,
        goods_content = goods_content,
        goods_pic=goods_pic,
    )
    if result:
        return redirect('/goods/goods_list')
    else:
        return HttpResponse('添加失败')

# def delete(request,id):
#    result = GoodsInfo.objects.get(pk=id).delete()
#    if result:
#        return redirect('/goods/goods_list')
#    else:
#        return HttpResponse("删除失败")

def update(request,id):
    result = GoodsInfo.objects.get(pk=id)
    type = GoodsType.objects.order_by("-type_id")
    if result:
        return render(request,'goods/goods_update.html',{'result':result,"type":type})
    else:
        return HttpResponse('失败')
def edit(request):
    goods_id = request.POST.get('id')
    goods_name = request.POST.get('goods_name')
    goods_price = request.POST.get('goods_price')
    goods_xprice = request.POST.get('goods_xprice')
    goods_count = request.POST.get('goods_count')
    goods_pic = request.FILES.get('goods_pic')
    goods_method = request.POST.get('goods_method')
    goods_info = request.POST.get('goods_info')
    goods_address = request.POST.get('goods_address')
    goods_content = request.POST.get('goods_content')
    # 商家的id
    manage_id = request.session['manage_id']
    type_id = request.POST.get("type_id")
    print(goods_pic)
    save_path = '%s/media/uploads/%s' % (settings.MEDIA_ROOT, goods_pic.name)

    print(save_path,1111111)

    # wb 2进制的方式写  chunks文件的内容
    with open(save_path, 'wb') as f:
        for content in goods_pic.chunks():
            f.write(content)

    res = GoodsInfo.objects.filter(id=goods_id).update(
        goods_name=goods_name,
        goods_price=goods_price,
        goods_xprice=goods_xprice,
        goods_count=goods_count,
        goods_method=goods_method,
        goods_info=goods_info,
        goods_pic=  "media/uploads/%s" % goods_pic.name,

        goods_address=goods_address,
        goods_content=goods_content,
        manage_id=manage_id,
        type_id = type_id,

    )
    if res:
        return redirect('/goods/goods_list')
    else:
        return HttpResponse("修改失败")
@csrf_exempt
def dele(request):
    id = request.POST.get('id')
    res = GoodsInfo.objects.get(pk=id).delete()
    if res[0]==1:
        return  HttpResponse(1)
    else:
        return HttpResponse(2)




