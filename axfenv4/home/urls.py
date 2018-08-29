from django.conf.urls import url
from home import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^market_params/(?P<typeid>\d+)/(?P<cid>\d+)/(?P<did>\d+)/', views.marketparams, name='market_params'),
    url(r'^add_to_cart/', views.add_to_card, name='add_to_card'),
    url(r'^minus_to_cart/', views.minus_to_cart, name='minus_to_cart'),
    url(r'^refresh_goods/', views.refresh_goods, name='refresh_goods'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^delselect/', views.delselect, name='delselect'),
    url(r'^allselect/', views.allselect, name='allselect'),
    url(r'^money/', views.money, name='money'),
    url(r'^order_info/', views.order_info, name='order_info'),
    url(r'^order_pay/', views.order_pay, name='order_pay'),
    url(r'^order/', views.order, name='order'),
    url(r'^order_list_wait_pay/', views.order_list_wait_pay, name='order_list_wait_pay'),
    url(r'^order_list_payed/', views.order_list_payed, name='order_list_payed'),


]