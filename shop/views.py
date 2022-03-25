from django.shortcuts import render,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import Category, Product
from .forms import CategoryAddForm,ProductAddForm,ProductPriceUpdateForm,ProductUpdateForm
from home.models import ShopProfile
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.views.generic.edit import UpdateView

@login_required(login_url='/register/')
def product_list(request, category_slug=None):
    shop = request.user.shopprofile.id
    x = ShopProfile.objects.get(user=request.user,id=shop)
    if x.paid == True:
        template = loader.get_template('shop/product/list.html')
        category = None
        categories = Category.objects.filter(creator=shop)
        if request.user.is_authenticated:
            shop = request.user.shopprofile.id
            products = Product.objects.filter(available=True,shop=shop)
            if category_slug:
                category = get_object_or_404(Category,slug=category_slug)
                products = products.filter(category=category,shop=shop)
            context = {'category':category,
                    'categories':categories,
                    'products':products,}
            return HttpResponse(template.render(context,request)) 
        else:
            return redirect('home')
    else:
        context={'x':x}
        template = loader.get_template('shop/notification.html')
        return HttpResponse(template.render(context,request)) 

@login_required(login_url='/register/')
def product_detail(request, id, slug):
    template = loader.get_template('shop/product/detail.html')
    shop = request.user.shopprofile.id
    product = get_object_or_404(Product,id=id,slug=slug,available=True,shop=shop)
    cart_product_form = CartAddProductForm()
    context = {'product': product,
                'cart_product_form':cart_product_form,}
    return HttpResponse(template.render(context,request)) 

@login_required(login_url='/register/')
def update_price(request,id,slug):
    shop = request.user.shopprofile.id
    product = Product.objects.get(id=id,slug=slug,available=True,shop=shop)
    if request.method == 'POST':
        form = ProductPriceUpdateForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop:product_list')
    else:
        form = ProductPriceUpdateForm(instance=product)
    context={'form': form,'product':product}
    template = loader.get_template('shop/update_price.html')
    return HttpResponse(template.render(context,request)) 

@login_required(login_url='/register/')
def update_product(request,id,slug):
    shop = request.user.shopprofile.id
    product = Product.objects.get(id=id,slug=slug,shop=shop)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop:shop_detail')
    else:
        form = ProductUpdateForm(instance=product)
        form.fields['category'].queryset = Category.objects.filter(creator=shop)
        #form = ProductUpdateForm(initial={'': 'Initial headline'}, instance=product)

    context={'form': form,'product':product}
    template = loader.get_template('shop/update_product.html')
    return HttpResponse(template.render(context,request)) 


class add_product(CreateView):
    model = Product
    form_class = ProductAddForm
    template_name = 'shop/add_product.html'
    success_url = reverse_lazy('shop:product_list')
    def get_form_kwargs(self):
        kwargs = super(add_product, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs 

class add_category(CreateView):
    model = Category
    form_class = CategoryAddForm
    template_name = 'shop/add_category.html'
    success_url = reverse_lazy('shop:product_list')
    def get_form_kwargs(self):
        kwargs = super(add_category, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

@login_required(login_url='/register/')
def shop_detail(request):
    shop = request.user.shopprofile.id
    product = Product.objects.filter(shop=shop).order_by('stock')
    categories = Category.objects.filter(creator=shop)
    context = {'product':product}
    template = loader.get_template('shop/shop_detail.html')
    return HttpResponse(template.render(context,request)) 