from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from home.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, CartModel, OrderModel, OrderGoodsModel

from utils.function import get_order

# Create your views here.

def home(request):
    if request.method == 'GET':
        mainwheels = MainWheel.objects.all()
        mainnavs = MainNav.objects.all()
        mustbuys = MainMustBuy.objects.all()
        mainshops = MainShop.objects.all()
        mainshows = MainShow.objects.all()


        data = {
            'mainwheels': mainwheels,
            'mainnavs': mainnavs,
            'mustbuys': mustbuys,
            'mainshops': mainshops,
            'mainshows' : mainshows

        }

        return render(request, 'home/home.html', data)


def market(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('home:market_params',
                                           kwargs={'typeid': 104749, 'cid': 0, 'did': 0,}))


def marketparams(request, typeid, cid, did):
    if request.method == 'GET':
        foodtypes = FoodType.objects.all()

        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid, childcid=cid )
        if did == '0':
            pass
        if did == '1':
            pass
        elif did == '1':
            goods = goods.order_by('-productnum')
        elif did == '2':
            goods = goods.order_by('-price')
        elif did == '3':
            goods = goods.order_by('price')
        types = FoodType.objects.filter(typeid=typeid).first()
        childtypes = [i.split(':') for i in types.childtypenames.split('#')]



        data = {
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'childtypes':  childtypes,
            'did': did,
            'cid': cid,

        }
        return render(request, 'market/market.html', data)


@csrf_exempt
def add_to_card(request):
    if request.method == 'POST':
        user = request.user
        if user.id:
            goods_id = request.POST.get('good_id')

            cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            if cart:
                cart.c_num += 1

                cart.save()
                c_data = {'c_num': cart.c_num}
            else:
                CartModel.objects.create(user=user, goods_id=goods_id)
                c_data = {'c_num': 1}
            data = {
                'code': 200,
                'msg': '成功',
                'data': c_data,
            }
            return JsonResponse(data)
        else:
            data ={
                'code': 200,
                'msg': '没有登录',
                'data': '',
            }
            return JsonResponse(data)


@csrf_exempt
def minus_to_cart(request):
    if request.method == 'POST':
        user = request.user
        if user.id:
            goods_id = request.POST.get('good_id')

            cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            if cart:
                if cart.c_num == 1:
                    cart.delete()

                    date={'c_num': '0'}
                else:
                    cart.c_num -= 1
                    cart.save()
                    date= {'c_num': cart.c_num}

                data = {
                    'code': 200,
                    'msg': '成功',
                    'data': date,
                }
                return JsonResponse(data)
            else:
                data = {
                    'code': 200,
                    'msg': '没有购买记录',
                    'data':{'c_num': '0'},
                }
                return JsonResponse(data)
        else:
            data ={
                'code': 200,
                'msg': '没有登录',
                'data': {'c_num': '0'},
            }
            return JsonResponse(data)


def refresh_goods(request):
    if request.method == 'GET':
        user = request.user
        data = {}
        data['code'] = 200
        data['msg'] = '请求成功'
        if user.id:
            carts = CartModel.objects.filter(user=user)
            if carts:
                cart_data = [(cart.goods_id, cart.c_num) for cart in carts]
                data['data'] = cart_data
            return JsonResponse(data)
        else:
            data['code'] = 1001
            data['msg'] = '用户没有登录'
            return JsonResponse(data)


def cart(request):

    if request.method == 'GET':

        user = request.user

        if user.id:
            # 如果用户已经登录，则加载购物车的数据
            carts = CartModel.objects.filter(user=user)
            cartnum = [cart.is_select for cart in carts]
            all = True if len(carts)==sum(cartnum) else False

            return render(request, 'cart/cart.html', {'carts': carts, 'all': all})


@csrf_exempt
def delselect(request):
    if request.method == 'POST':
        user = request.user
        good_id = request.POST.get('good_id')
        c = CartModel.objects.filter(user=user, goods_id=good_id).first()
        c.is_select = 0 if c.is_select else 1
        c.save()
        carts = CartModel.objects.filter(user=user)
        cartnum = [cart.is_select for cart in carts]
        all = True if len(carts) == sum(cartnum) else False
        data ={
            'code': 200,
            'msg': '请求成功',
            'is_select': c.is_select,
            'all': all,
        }
        return JsonResponse(data)


def allselect(request):
    if request.method == 'GET':
        user = request.user
        carts = CartModel.objects.filter(user=user)
        goods_id = [cart['goods_id'] for cart in carts.values()]
        cartnum = [cart.is_select for cart in carts]
        all = True if len(carts) == sum(cartnum) else False
        if all:
            all = 0
            for c in carts:
                c.is_select = 0
                c.save()
        else:
            all = 1
            for c in carts:
                c.is_select = 1
                c.save()
        data = {
            'code': 200,
            'msg': '请求成功',
            'all': all,
            'goods_id':  goods_id,
        }
        return JsonResponse(data)


def money(request):
    if request.method == 'GET':
        user = request.user
        carts = CartModel.objects.filter(user=user, is_select=1)
        money = 0
        for catr in carts:
            money += catr.goods.price * catr.c_num
        money = round(money, 3)
        data = {
            'code': 200,
            'msg': '请求成功',
            'money': money,
        }
        print(data)
        return JsonResponse(data)

@csrf_exempt
def order(request):
    if request.method == 'POST':
        user = request.user
        o_num = get_order()
        #创建订单
        order = OrderModel.objects.create(user=user, o_num=o_num)
        #获取用户购物车信息
        carts = CartModel.objects.filter(user=user, is_select=1)
        #创建订单商品详情表
        for c in carts:
            OrderGoodsModel.objects.create(order=order,
                                           goods=c.goods,
                                           goods_num=c.c_num)
        carts.delete()
        return JsonResponse({'code': 200, 'msg': "请求成功", 'order_id': o_num})


def order_info(request):
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        print(order_id)
        order = OrderModel.objects.get(o_num=order_id)

        goods= OrderGoodsModel.objects.filter(order=order)
        money = 0
        for good in goods:
            money += good.goods.price*good.goods_num
        money = round(money, 3)

        data = {'goods': goods, 'order_id': order.o_num, 'money': money}
        return render(request, 'order/order_info.html', data)


@csrf_exempt
def order_pay(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = OrderModel.objects.get(o_num=order_id)
        order.o_status = 1
        order.save()
        data = {'code': 200, 'msg': '请求成功'}
        return JsonResponse(data)


def order_list_wait_pay(request):
    if request.method == 'GET':
        print("---------------")
        user = request.user
        print(user)
        orders = OrderModel.objects.filter(user=user, o_status=0)
        return render(request, 'order/order_list_wait_pay.html', {'orders': orders})


def order_list_payed(request):
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user, o_status=1)
        return render(request, 'order/order_list_payed.html', {'orders': orders})