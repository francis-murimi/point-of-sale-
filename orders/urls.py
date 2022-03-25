from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/',views.order_create,name='order_create'),
    path('try/',views.stock_check2,name='stock_check2'),
]