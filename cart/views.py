from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='/register/')
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = form.cleaned_data.get('quantity')
        cart.add(product=product,quantity=quantity,update_quantity=cd['update'])
    return redirect('cart:cart_detail')

@login_required(login_url='/register/')
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@login_required(login_url='/register/')
def cart_detail(request):
    template = loader.get_template('cart/detail.html')
    cart = Cart(request)
    context = {'cart': cart}
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity':item['quantity'],'update':True})
    return HttpResponse(template.render(context,request))


