from django.contrib import admin
from .models import Order, OrderItem
from django.urls import reverse

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product'] 
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','created','mine']
    list_filter = ['created']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

