import re
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from home.models import UserTicketModel
from users.models import UserModel


class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        path = request.path
        paths = ['/users/register/','/home/home/', '/users/login/','/home/market/']

        for check_path in paths:
            if re.match(check_path, path):
                return None

        session_id = request.COOKIES.get('session_id')
        if not session_id:
            if path == '/users/mine/':
                return None
            if re.match(re.compile(r'/home/market_params/(\d+)/(\d+)/(\d+)/'), path):
                return None
            return HttpResponseRedirect(reverse('users:login'))


        userticket = UserTicketModel.objects.filter(ticket=session_id).first()
        if userticket:
            if userticket.out_time.replace(tzinfo=None) < datetime.now():
                userticket.delete()
                return HttpResponseRedirect(reverse('users:login'))
            request.user = userticket.user
        else:
            if path == '/users/mine/' :
                return None
            return HttpResponseRedirect(reverse('users:login'))





