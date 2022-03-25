from django.db import models
from shop.models import Product
from django.contrib.auth.models import User
from home.models import ShopProfile
from django.urls import reverse
import datetime


class Order(models.Model):
    orderer = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    mine = models.ForeignKey(ShopProfile,related_name='mwene',on_delete=models.CASCADE)
    made = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ('-created',) 
    def __str__(self):
        return 'Order {}'.format(self.id)
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    def get_order_detail(self):
        return reverse('info:order_item',args=[self.id])
    def get_total_profit(self):
        return sum(item.get_profit() for item in self.items.all())
    def get_total_sales(self):
        return sum(item.get_sales() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=True)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    old_cost = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    quantity = models.PositiveIntegerField(default=1)
    shop = models.ForeignKey(ShopProfile,related_name='duka',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    stock = models.BooleanField(default=False)
    class Meta:
        ordering = ('-created',)
    
    """def __str__(self):
        return '{}'.format(self.id)"""
    def save(self, *args, **kwargs):
        self.name = self.product.name
        super(OrderItem, self).save(*args, **kwargs)
    def __str__(self):
        return self.product.name
    def get_cost(self):
        return self.price * self.quantity
    def one_profit(self):
        return self.price - self.cost
    def get_profit(self):
        return (self.price - self.cost) * self.quantity
    def get_name(self):
        return self.product.name
    def get_quantity(self):
        return int(self.quantity)
    def get_sales(self):
        return self.price * self.quantity