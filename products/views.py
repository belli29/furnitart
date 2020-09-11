from django.shortcuts import render, get_object_or_404, redirect,reverse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Product, Category
from .forms import ProductForm
from checkout.models import Order, OrderLineItem, PreOrder, PreOrderLineItem

# Create your views here.

def all_products (request):
    """view showing all products, including sorting and search queried"""
    # save current parameters in a variable 
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
    # orders section
    orders = Order.objects.all()
    pay_pal_filter = False
    shipped_filter = False
    view_preorders = False
    if 'view_preorders' in request.GET:    
        view_preorders = True
    if 'pay_pal_filter' in request.GET:
        orders = orders.filter(pay_pal_order=True)
        pay_pal_filter = True
    if 'shipped_filter' in request.GET:
        orders = orders.filter(shipped=True)
        shipped_filter = True
    # save current parameters in a variable 
    current_url = request.get_full_path()
    if '?' in current_url :
        current_param = current_url.split('?')[1]
    else:
        current_param = ""

    preorders = PreOrder.objects.all()
    context = {
        'view_preorders': view_preorders,
        'orders': orders,
        'preorders': preorders,
        'pay_pal_filter_active': pay_pal_filter,
        'shipped_filter_active': shipped_filter,
        'current_param': current_param,
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
            # identify if the user was coming from management dashboard
            from_management = request.POST['from_management']
            print(from_management)
            if from_management:  
                return redirect(reverse('list_products'))
            else:
                return redirect (reverse("product_details", args=[product.id]))
        else:
           messages.error(request, 'Something went wrong. We could not add the product.') 
        
    else:
        form = ProductForm()
        # define if the user is coming from management dashboard
        from_management = request.GET.get("from_management", False)
        context = {
            "form": form,
            "from_management": from_management,
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
            "products": all_products,
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
            if from_management:
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
    # identify if the user was coming from management dashboard
    from_management = request.GET.get('from_management', False)
    if from_management:
        return redirect(reverse('list_products'))
    else:
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
    return redirect(reverse('list_products'))
 
@login_required
def order_history(request, order_number):
    """ show speficic order """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can see that.')
        return redirect(reverse('home'))
    order = get_object_or_404(Order, order_number=order_number)
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_management': True,
    }

    return render(request, template, context)

@login_required
def pre_order_history(request, order_number):
    """ show speficic pre order """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can see that.')
        return redirect(reverse('home'))
    order = get_object_or_404(PreOrder, order_number=order_number)
    messages.info(request, (
        f'This is a past confirmation for pre order number {order_number}. '
        'Payment instructions  were sent on the order date.'
    ))

    template = 'checkout/invoice_confirmation.html'
    context = {
        'order': order,
        'from_management': True,
        }

    return render(request, template, context)

@login_required
def confirm_pre_order(request, order_number):
    """ view deleting preorder and creating a corresponding order """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can see that.')
        return redirect(reverse('home'))
    pre_order = get_object_or_404(PreOrder, order_number=order_number)
    order = Order(
        user_profile=pre_order.user_profile,
        full_name=pre_order.full_name,
        email=pre_order.email,
        phone_number=pre_order.phone_number,
        country=pre_order.country,
        postcode=pre_order.postcode,
        town_or_city=pre_order.town_or_city,
        street_address1=pre_order.street_address1,
        street_address2=pre_order.street_address2,
        county=pre_order.county,
        delivery_cost=pre_order.delivery_cost,
        order_total=pre_order.order_total,
        grand_total=pre_order.grand_total,
        pay_pal_order=True
        
    )
    # save order
    order.save()
    # copy line items from preorder to order 
    for li in pre_order.lineitems.all():
        order_line_item = OrderLineItem(
            order=order,
            product=li.product,
            quantity=li.quantity,
        )
        order_line_item.save()
        # update product reserved, sold
        product=li.product
        quantity=li.quantity
        product.sold =  product.sold + quantity
        product.reserved = product.reserved - quantity
        product.save()
    # delete preorder
    pre_order.delete()
    # success message
    messages.success(request, f'pre_order {pre_order.order_number} deleted. New order {order.order_number} confirmed')
    return redirect(reverse('products_management'))

@login_required
def delete_pre_order(request, order_number):
    """ view deleting preorder and creating a corresponding order """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can see that.')
        return redirect(reverse('home'))
    pre_order = get_object_or_404(PreOrder, order_number=order_number)
    order = Order(
        user_profile=pre_order.user_profile,
        full_name=pre_order.full_name,
        email=pre_order.email,
        phone_number=pre_order.phone_number,
        country=pre_order.country,
        postcode=pre_order.postcode,
        town_or_city=pre_order.town_or_city,
        street_address1=pre_order.street_address1,
        street_address2=pre_order.street_address2,
        county=pre_order.county,
        delivery_cost=pre_order.delivery_cost,
        order_total=pre_order.order_total,
        grand_total=pre_order.grand_total,
        pay_pal_order=True
        
    )
    # update product avaiable, reserved
    for li in pre_order.lineitems.all():
        product=li.product
        quantity=li.quantity
        product.available_quantity =  product.available_quantity + quantity
        product.reserved = product.reserved - quantity
        product.save()
    
    # email user
    cust_email = order.email
    subject = render_to_string(
        'checkout/confirmation_emails/delete_preorder_subject.txt',
        {'preorder': order})
    body = render_to_string(
        'checkout/confirmation_emails/delete_preorder_body.txt',
        {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
            
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
    # delete preorder
    pre_order.delete()
    # success message
    messages.success(request, f'pre_order {pre_order.order_number} deleted.')
    return redirect(reverse('products_management'))