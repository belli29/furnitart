from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.contrib import messages
from django.db.models import Q, F
from django.db.models.functions import Lower

from .models import Product, Category

# Create your views here.

def all_products (request):
    """view showing all products, including sorting and search queried"""
    
    current_url = request.get_full_path()
    if '?' in current_url :
        current_param = current_url.split('?')[1]
    else:
        current_param = ""
    
    products = Product.objects.filter(is_active=True)
    query = None
    category = None
    sort = None
    direction = None
    euro_filter = False
    image_filter = False

    if 'euro_filter' in request.GET:
        products = products.filter(euro_shipping=True)
        euro_filter = True
    
    if 'image_filter' in request.GET:
        products = products.exclude(image = "")
        image_filter = True


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
        category = Category.objects.filter(name=category)[0]

    current_sorting = f'{sort}_{direction}'

    context ={
        'products': products,
        'search_term': query, 
        'current_category':category,
        'current_sorting': current_sorting,
        'euro_filter_active': euro_filter,
        'image_filter_active': image_filter,
        'current_param': current_param
    }

    return render(request, 'products/products.html', context )

def product_details (request, product_id):
    """view showing details of the selected product"""
    
    product = get_object_or_404(Product, pk=product_id)
    context ={
        'product': product
    }

    return render(request, 'products/product_details.html', context )