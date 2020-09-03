from django.urls import path
from . import views
from .webhooks import webhook
urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('wh/', webhook, name='webhook'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('invoice_confirmation/<pre_order_number>', views.invoice_confirmation, name='invoice_confirmation'),
    path('toggle_shipped/<int:order_id>', views.toggle_shipped, name='toggle_shipped'),
    path('change_country/<country>', views.change_country, name='change_country'),
]