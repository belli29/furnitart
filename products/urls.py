from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_details, name='product_details'),
    path('management/', views.management, name='products_management'),
    path('add/', views.add_product, name='add_product'),
    path('list_products/', views.list_products, name='list_products'),
    path('edit/<int:product_id>', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>', views.delete_product, name='delete_product'),
    path('toggle_active/<int:product_id>', views.toggle_active, name='toggle_active'),
]   