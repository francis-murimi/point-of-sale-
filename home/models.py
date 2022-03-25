from django.db import models
from django.contrib.auth.models import User

class ShopProfile(models.Model):
    PACKAGE_TYPE = (
        ('standard', 'Standard'),
        ('advanced', 'Advanced'),
        ('premium','Premium'),
    )
    SUBSCRIPTION_TYPE = (
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=150,help_text='Business name')
    category = models.CharField(max_length=150,help_text='Type of shop')
    county = models.CharField(max_length=150,help_text='County of operation')
    town = models.CharField(max_length=150,help_text='Town of operation')
    shop_pin = models.CharField(max_length=10,help_text='Shop administration pin',default='12345')
    paid = models.BooleanField(default=False)
    subscription = models.CharField(max_length=8,choices=SUBSCRIPTION_TYPE,default='yearly',help_text='Pay monthly or yearly?')
    shop_package = models.CharField(max_length=9,choices=PACKAGE_TYPE,default='standard',help_text='Standard = 100 products, Advanced=200 products,Premium=Above 200 products')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    def __str__(self):
        return self.user.username

