from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
    path('pre_order_history/<order_number>', views.pre_order_history, name='pre_order_history'),
]