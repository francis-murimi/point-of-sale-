from django.shortcuts import render,get_object_or_404,redirect
from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from shop.models import Product as kindu
import itertools
from home.models import ShopProfile

@login_required(login_url='/register/')
def order_create(request):
    cart = Cart(request)
    kitu = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.orderer = request.user
            order.mine = ShopProfile.objects.get(user = request.user)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'],cost=item['cost'],old_cost=item['old_cost'],shop= request.user.shopprofile,)
            cart.clear()
            return redirect('orders:stock_check2')
            #return render(request,'orders/order/created.html',{'order': order,'kitu':kitu,'cart':cart})
    else:
        form = OrderCreateForm()
    return render(request,'orders/order/create.html',{'cart': cart, 'form': form})

@login_required(login_url='/register/')
def stock_check(request):
    shop = request.user.shopprofile
    order_item = OrderItem.objects.filter(shop=shop,stock=False)
    shop_item = kindu.objects.filter(shop=shop)
    for a,b in zip(order_item,shop_item):
        if a.get_name() == b.name:
            c = int(b.stock)
            d = a.get_quantity()
            b.stock = c - d
            b.save()
            a.stock = True
            a.save()
        if b.stock < 1:
            b.available = False
            b.save()
    return render(request,'orders/try.html',{})

#genre_list = Song.objects.values_list('genre',flat=True).order_by('genre').distinct()
@login_required(login_url='/register/')
def stock_check2(request):
    shop = request.user.shopprofile
    order_item = OrderItem.objects.filter(shop=shop,stock=False)
    shop_item = kindu.objects.filter(shop=shop)
    for a,b in [(a,b) for a in order_item for b in shop_item ]:
        if a.get_name() == b.name:
            c = int(b.stock)
            d = a.get_quantity()
            b.stock = c - d
            b.save()
            a.stock = True
            a.save()
        if b.stock < 1:
            b.available = False
            b.save()
    return redirect('shop:product_list')

