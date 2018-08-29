from datetime import datetime, timedelta
import random

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from home.models import UserTicketModel
from users.models import UserModel

# Create your views here.
from utils.function import random_titck


def mine(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            arrearage = 0
            receiving = 0
            apprais = 0
            ordermodel = user.ordermodel_set.all()
            for order in ordermodel:
                if order.o_status == 0:
                    arrearage += 1
                elif order.o_status == 1 or order.o_status == 2:
                    receiving += 1
                elif order.o_status == 3:
                    apprais += 1
            data ={
                'arrearage': arrearage,
                'receiving': receiving,
                'apprais': apprais
            }
            return render(request, 'mine/mine.html', data)
        else:
            return render(request, 'mine/mine.html')


def registe(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get("icon")
        if not all([username, password, email, icon]):
            error = '请填完所有信息'
            return render(request, 'user/user_register.html', {'error': error})
        user = UserModel.objects.filter(username=username).exists()
        if user:
            error = '用户名已存在'
            return render(request, 'user/user_register.html',{'error': error})
        else:
            UserModel.objects.create(username=username, password=make_password(password), email=email, icon=icon)
            return HttpResponseRedirect(reverse('users:login'))


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username, password]):
            error = '请填完所有信息'
            return render(request, 'user/user_login.html', {'error': error})
        user = UserModel.objects.filter(username=username).first()
        if not user:
            error = '用户名不存在'
            return render(request, 'user/user_login.html', {'error': error})
        else:
            userpassword = user.password
            if check_password(password, userpassword):
                res = HttpResponseRedirect(reverse('users:mine'))
                # 写随机数字符串生成cookie
                s = 'qazwsxedcrfvtgbyhnujmikolpQZWXEDCRFVTGBYHNUJMIKOLP1234567890'
                # 给cookie定名字
                session_id = ''
                # 循环写cookie
                session_id = random_titck()
                # 创建cookie过期时限默认（一天）
                out_time = datetime.now() + timedelta(days=1)
                # 为用户（服务器客户端添加）添加cookie,用来判断用户是否登录。没有登录的用户没有cookie值无法直接进
                res.set_cookie('session_id', session_id, expires=out_time)
                UserTicketModel.objects.create(ticket=session_id, out_time=out_time, user_id=user.id)
                # 执行跳转
                return res


def logout(request):
    if request.method == 'GET':
        user = request.user
        UserTicketModel.objects.filter(user_id=user.id).delete()
        res = HttpResponseRedirect(reverse('users:mine'))
        res.delete_cookie('session_id')
        return res


