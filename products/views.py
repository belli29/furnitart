from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect

from .models import Product, Category
from .forms import ProductForm
from checkout.models import Order

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
        products = products.exclude(image ="")
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
    bag_qty = 0
    if 'bag' in list(request.session.keys()):
        if product_id in list(request.session.get("bag").keys()):
            bag_qty = request.session.get("bag")[product_id]
    remaining_qty = product.available_quantity - bag_qty
    context ={
        'product': product,
        'remaining_qty': remaining_qty
    }

    return render(request, 'products/product_details.html', context )

# products management

@login_required
def management (request):
    """view allowing super users to manage inventory """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    all_orders = Order.objects.all()
    context = {
        'orders': all_orders,
    }
    template = 'products/management.html'
    return render(request, template, context )



@login_required
def add_product (request):
    """view adding a new product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'You succesfully added a product!')
            return redirect (reverse("product_details", args=[product.id]))
        else:
           messages.error(request, 'Something went wrong. We could not add the product.') 
        
    else:
        form = ProductForm()
        context = {
            "form": form
        }
        template = 'products/add_product.html'
        return render (request, template, context)

@login_required
def list_products (request):
    """view listing all products """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    all_products = Product.objects.all()
    context = {
            "products": all_products
        }
    template = 'products/list_products.html'
    return render (request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            # identify if the user was coming from management dashboard
            from_management = request.POST['from_management']
            if from_management == True:  
                return redirect(reverse('list_products'))
            else:
                return redirect(reverse('product_details', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')
    template = 'products/edit_product.html'
    # define if the user is coming from management dashboard
    from_management = request.GET.get("from_management", False)
    context = {
        'form': form,
        'product': product,
        'from_management': from_management,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f'Product {product.name} deleted!')
    return redirect(reverse('products'))

@login_required
def toggle_active(request, product_id):
    """ Toggle a product is_active field """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    if product.is_active:
        product.is_active = False
        product.save()
    else:
        product.is_active = True
        product.save()
    template = 'products/list_products.html'
    return redirect(reverse('list_products'))