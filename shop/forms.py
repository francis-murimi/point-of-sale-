from django import forms
from .models import Category,Product
from home.models import ShopProfile

"""category_choice =  Category.objects.filter(creator=shop)
    PRODUCT_CATEGORY_CHOICES = [(i, str(i)) for i in category_choice]"""

class CategoryAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CategoryAddForm, self).__init__(*args, **kwargs)
        self.fields['creator'].queryset = ShopProfile.objects.filter(user = self.request.user,paid=True)
    class Meta:
        model = Category
        fields = ['creator','name']

class ProductAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProductAddForm, self).__init__(*args, **kwargs)
        shop = self.request.user.shopprofile
        self.fields['category'].queryset = Category.objects.filter(creator=shop)
        self.fields['shop'].queryset = ShopProfile.objects.filter(user = self.request.user,paid=True)
    class Meta:
        model = Product
        fields = ['shop','category','name','price','cost','stock','description']

class ProductPriceUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['price']

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category','name','description','price','cost','stock','available']