from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def all_products (request):
    """view showing all products, including sorting and search queried"""
    
    products = Product.objects.filter(is_active=True)
    context ={
        'products': products, 
    }

    return render(request, 'products/products.html', context )

def product_details (request, product_id):
    """view showing details of the selected product"""
    
    product = get_object_or_404(Product, pk=product_id)
    context ={
        'product': product
    }

    return render(request, 'products/product_details.html', context )