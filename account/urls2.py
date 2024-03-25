from django.urls import path, include
from .views import custom_activation_view,password_rest_view,reset_password_confirm_view
import account.views as views
urlpatterns = [
    path('activate/', custom_activation_view, name='custom_activation'),
    path('password-reset/', password_rest_view, name='custom_pasword_reset'),
    path('reset_password_confirm/', reset_password_confirm_view, name='reset_password_confirm'),

   ]
