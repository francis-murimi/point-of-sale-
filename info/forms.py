from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    tarehe = forms.DateField(widget=DateInput()) 
    #name = forms.CharField()

class Tryform(forms.Form):
    name = forms.CharField()

class ShopAdminForm(forms.Form):
    admin_pin = forms.CharField(widget=forms.PasswordInput()) 
    