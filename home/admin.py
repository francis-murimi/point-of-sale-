from django.contrib import admin
from . models import ShopProfile

class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ['user','shop_name','county','category','created','updated','paid','subscription']
    list_filter = ['county','paid','subscription']
    search_fields = ['shop_name']
admin.site.register(ShopProfile,ShopProfileAdmin)