from django.urls import path,reverse_lazy
from . import views
from django.conf.urls import url
app_name = 'info'
urlpatterns = [
    path('sales/',views.all_sales,name='all_sales'),
    path('time/',views.my_time,name='my_time'),
    path('display/',views.show_time,name='show_time'),
    path('detail/<int:id>',views.order_item,name='order_item'),
    path('access/',views.access_grant,name='access_grant'),
    ]