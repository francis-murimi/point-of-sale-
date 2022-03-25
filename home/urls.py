from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
app_name = 'home'
urlpatterns = [
    path('',views.home,name = 'home'),
    path('register/',views.register,name='register'),
    path('login/',views.log_in,name='log_in'),
    path('logout/',views.log_out,name='log_out'),
    path('check/',views.check_payment,name='check_payment'),
    path('documentation/',views.documentation,name='documentation'),
    path('package/',views.check_package,name='check_package'),
    #password reset views
    #password.html contains form for email,email_template is template shown in email
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='home/password.html',email_template_name='home/email.html',success_url=reverse_lazy('home:password_reset_done')),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('home:password_reset_complete')),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'),name='password_reset_complete'),
    ]
