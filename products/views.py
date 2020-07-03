from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.contrib import messages
from django.db.models import Q, F
from django.db.models.functions import Lower

from .models import Product, Category

# Create your views here.

def all_products (request):
    """view showing all products, including sorting and search queried"""
    
    products = Product.objects.filter(is_active=True)
    query = None
    category = None

    if 'sort' in request.GET:
        sortkey = request.GET['sort']
        sort = sortkey
        if sortkey == 'name':
            sortkey = 'lower_name'
            products = products.annotate(lower_name=Lower('name'))
        if sortkey == 'size':
            products = products.annotate(size=F('l')*F('w')*F('h'))          
        if 'direction' in request.GET:
            direction = request.GET['direction']
            if direction == 'desc':
                sortkey = f'-{sortkey}'
        products = products.order_by(sortkey)

    if 'q' in request.GET:
        query = request.GET['q']
        if not query:
            messages.error(request, 'You have not entered any search criteria')
            return redirect(reverse('products'))

        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)
    
    if 'category' in request.GET:
        category = request.GET['category']
        products = products.filter(category__name=category)
        category = Category.objects.filter(name=category)

    context ={
        'products': products,
        'search_term': query, 
        'current_category':category
    }

    return render(request, 'products/products.html', context )

def product_details (request, product_id):
    """view showing details of the selected product"""
    
    product = get_object_or_404(Product, pk=product_id)
    context ={
        'product': product
    }

    return render(request, 'products/product_details.html', context )