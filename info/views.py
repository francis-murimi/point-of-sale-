from django.shortcuts import render,get_object_or_404,redirect
from orders.models import OrderItem,Order
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from .forms import DateForm,Tryform,ShopAdminForm
import itertools
from datetime import datetime,timedelta,date
import pytz
from django.db.models import Count,Sum,Avg

@login_required(login_url='/register/')
def all_sales(request):
    shop = request.user.shopprofile
    orders = Order.objects.filter(mine=shop)
    template = loader.get_template('info/all.html')
    context = {'orders':orders,}
    return HttpResponse(template.render(context,request))

@login_required(login_url='/register/')
def my_time(request):
    shop = request.user.shopprofile
    
    s_pin = ''
    form_class = ShopAdminForm
    form = form_class(request.POST or None)
    if request.method == "POST":
        form = ShopAdminForm(request.POST)
        if form.is_valid():
            s_pin = form.cleaned_data.get("admin_pin")
            if s_pin == shop.shop_pin:
                leo = date.today()
                orders = Order.objects.filter(mine=shop)
                aa = OrderItem.objects.filter(shop=shop).values('name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')
                sales = sum(order.get_total_sales() for order in orders)
                profit = sum(order.get_total_profit() for order in orders)
                cost = sales - profit
                rate = (profit/cost)*100
                template = loader.get_template('info/my_time.html')
                context = {'sales':sales,'profit':profit,'cost':cost,'rate':rate,'aa':aa,'shop':shop}
                return HttpResponse(template.render(context,request))
        else:
            form = ShopAdminForm()
    context = {'form':form,}
    template = loader.get_template('info/my_time.html')
    return HttpResponse(template.render(context,request))

@login_required(login_url='/register/')
def access_grant(request):
    shop = request.user.shopprofile
    s_pin = ''
    form_class = ShopAdminForm
    form = form_class(request.POST or None)
    if request.method == "POST":
        form = ShopAdminForm(request.POST)
        if form.is_valid():
            s_pin = form.cleaned_data.get("admin_pin")
            if s_pin == shop.shop_pin:
                return redirect('info:show_time')
        else:
            form = ShopAdminForm()
    context = {'form':form,}
    template = loader.get_template('info/myform.html')
    return HttpResponse(template.render(context,request))

@login_required(login_url='/register/')
def show_time(request):
    tarehe = date.today()
    form_class = DateForm
    form = form_class(request.POST or None)
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            tarehe = form.cleaned_data.get("tarehe")
        else:
            form = DateForm()
    # analysis
    shop = request.user.shopprofile
    weekday = tarehe - timedelta(days=6)
    orders = Order.objects.filter(mine=shop,made__year=tarehe.year,made__month=tarehe.month,made__day=tarehe.day)
    #dd = OrderItem.objects.filter(shop=shop,created__year=tarehe.year).values('name').annotate(total_quantity=Sum('quantity')).order_by('name')
    sales = sum(order.get_total_sales() for order in orders)
    profit = sum(order.get_total_profit() for order in orders)
    cost = sales - profit
    if profit == 0:
        rate = 0
    else:
        rate = (profit/cost)*100
    weekly_orders = Order.objects.filter(mine=shop,made__range=[weekday,tarehe])
    ww = OrderItem.objects.filter(shop=shop,created__range=[weekday,tarehe]).values('name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')
    w_sales = sum(order.get_total_sales() for order in weekly_orders)
    w_profit = sum(order.get_total_profit() for order in weekly_orders)
    w_cost = w_sales - w_profit
    if profit == 0:
        w_rate = 0
    else:
        w_rate = (w_profit/w_cost)*100
    monthly_orders = Order.objects.filter(mine=shop,made__year=tarehe.year,made__month=tarehe.month)
    #mm = OrderItem.objects.filter(shop=shop,created__year=tarehe.year).values('name').annotate(total_quantity=Sum('quantity')).order_by('name')
    m_sales = sum(order.get_total_sales() for order in monthly_orders)
    m_profit = sum(order.get_total_profit() for order in monthly_orders)
    m_cost = m_sales - m_profit
    if m_profit == 0:
        m_rate = 0
    else:
        m_rate = (m_profit/m_cost)*100
    yearly_orders = Order.objects.filter(mine=shop,made__year=tarehe.year)
    yy = OrderItem.objects.filter(shop=shop,created__year=tarehe.year).values('name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')
    y_sales = sum(order.get_total_sales() for order in yearly_orders)
    y_profit = sum(order.get_total_profit() for order in yearly_orders)
    y_cost = y_sales - y_profit
    if y_cost == 0:
        y_rate = 0
    else:
        y_rate = (y_profit/y_cost)*100
    context = {'form':form,'tarehe':tarehe,
                'orders':orders,
                'weekday':weekday,
                'weekly_orders':weekly_orders,
                'monthly_orders':monthly_orders,
                'yearly_orders':yearly_orders,
                'sales':sales,'profit':profit,'cost':cost,'rate':rate,
                'w_sales':w_sales,'w_profit':w_profit,'w_cost':w_cost,'w_rate':w_rate,
                'm_sales':m_sales,'m_profit':m_profit,'m_cost':m_cost,'m_rate':m_rate,
                'y_sales':y_sales,'y_profit':y_profit,'y_cost':y_cost,'y_rate':y_rate,
                'yy':yy,'ww':ww}
    template = loader.get_template('info/show.html')
    return HttpResponse(template.render(context,request))

@login_required(login_url='/register/')
def order_item(request,id):
    shop = request.user.shopprofile.id
    order = Order.objects.get(id=id,mine=shop)
    product = OrderItem.objects.filter(order=order)
    template = loader.get_template('info/order_item.html')
    context = {'product':product,'order':order}
    return HttpResponse(template.render(context,request))


