from django.shortcuts import render,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import ExtendedUserCreationForm,ShopProfileForm,LoginForm, UserUpdateForm,ShopUpdateForm
from django.contrib import messages
from . models import ShopProfile
from datetime import datetime,timedelta,date
from shop.models import Product

def check_payment(request):
    y_shops = ShopProfile.objects.filter(subscription='yearly',paid=True)
    m_shops = ShopProfile.objects.filter(subscription='monthly',paid=True)
    tarehe = date.today()
    for shop in y_shops:
        ref_date = shop.updated  + timedelta(days=365)
        if tarehe == ref_date:
            shop.paid = False
            shop.save()
    
    for shop in m_shops:
        ref_date = shop.updated  + timedelta(days=30)
        if tarehe == ref_date:
            shop.paid = False
            shop.save()
    return redirect('home')


def home(request):
    shop = ''
    if request.user.is_authenticated:
        username = request.user.username
        shop = request.user.shopprofile
    else:
        username = 'not logged in'
    context = {'username':username,'shop':shop}
    template = loader.get_template('home/home.html')
    return HttpResponse(template.render(context,request))

def log_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect ('home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm()
    form = LoginForm()
    template = loader.get_template('home/login.html')
    context = {'form':form}
    return HttpResponse(template.render(context,request))

def register(request):
    template = loader.get_template('home/register.html')
    if request.method == 'POST':
        form =ExtendedUserCreationForm(request.POST)
        profile_form = ShopProfileForm(request.POST)
        
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1') 
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home')
    else:
        form = ExtendedUserCreationForm()
        profile_form = ShopProfileForm()
    
    context = {'form':form,'profile_form':profile_form}
    return HttpResponse(template.render(context,request))

def log_out(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/register/')
def profile(request):
    if request.method == 'POST':
        p_form = ShopUpdateForm(request.POST,request.FILES,instance=request.user.shopprofile)
        u_form = UserUpdateForm(request.POST,instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your Profile has been updated!')
            return redirect('home')
    else:
        p_form = ShopUpdateForm(instance=request.user.shopprofile)
        u_form = UserUpdateForm(instance=request.user)

    context={'p_form': p_form, 'u_form': u_form}
    template = loader.get_template('home/update.html')
    return HttpResponse(template.render(context,request))

def documentation(request):
    context={}
    template = loader.get_template('home/documentation.html')
    return HttpResponse(template.render(context,request))

@login_required(login_url='/register/')
def check_package(request):
    shop_id = request.user.shopprofile.id
    x = Product.objects.filter(shop=shop_id).count()
    shop = request.user.shopprofile
    
    if shop.shop_package == 'standard':
        if x > 101:
            context={'shop_id':shop_id,'shop':shop,'x':x,}
            template = loader.get_template('home/package.html')
            return HttpResponse(template.render(context,request))
        else:
            return redirect ('shop:add_product')
    elif shop.shop_package == 'advanced':
        if x > 201:
            context={'shop_id':shop_id,'shop':shop,'x':x}
            template = loader.get_template('home/package.html')
            return HttpResponse(template.render(context,request))
        else:
            return redirect ('shop:add_product')
    
    elif shop.shop_package == 'premium':
        if x > 401:
            context={'shop_id':shop_id,'shop':shop,'x':x,}
            template = loader.get_template('home/package.html')
            return HttpResponse(template.render(context,request))
        else:
            return redirect ('shop:add_product')
    else:
        context={'shop_id':shop_id,'shop':shop,}
        template = loader.get_template('home/package.html')
        return HttpResponse(template.render(context,request))
    