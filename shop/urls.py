from django.conf.urls import url
from django.urls import path
from . import views
from shop.views import add_product

app_name = 'shop'
urlpatterns = [
    path('price/<int:id>/<slug>/',views.update_price,name='update_price'),
    path('product/<int:id>/<slug>/',views.update_product,name='update_product'),
    path('shop/',views.shop_detail,name='shop_detail'),
    path('product/',views.add_product.as_view(),name='add_product'),
    path('category/',views.add_category.as_view(),name='add_category'),
    path('<category_slug>/',views.product_list,name='product_list_by_category'),
    path('<int:id>/<slug>/',views.product_detail,name='product_detail'),
    path('product_list',views.product_list,name='product_list'),
]