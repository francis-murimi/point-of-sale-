from django import forms
from .models import Order
from urllib import request


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['mine','orderer']