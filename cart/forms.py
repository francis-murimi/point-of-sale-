from django import forms
from shop.models import Product
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
#form = CartAddProductForm(initial={'cost':str(Product.cost),'old_cost':str(Product.old_cost),})
"""cost = models.DecimalField(max_digits=10, decimal_places=2)
old_cost = models.DecimalField(max_digits=10, decimal_places=2,blank=True)"""