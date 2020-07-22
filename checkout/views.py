from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents

import stripe
import json

def checkout(request):
    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        } 
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_quantity in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_quantity,
                            )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Contact us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))    
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
        request.session['save_info'] = 'save-info' in request.POST
        return redirect(reverse('checkout_success', args=[order.order_number]))
    else:
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        grand_total = current_bag['grand_total']
        # Stripe intent
        stripe_total = round(grand_total*100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()
        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

    return render(request, template, context)

def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')
    
    bag = request.session['bag'] # saves session bag info to a bag variable 
    bag_with_item_name = []
    for key , value in bag.items():
        product = get_object_or_404(Product, pk=key)
        bag_with_item_name.append({
            'name':product.name,
            'quantity': value

        })
    if 'bag' in request.session: # deletes session bag 
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'bag': bag_with_item_name 
    }

    return render(request, template, context)

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except  Exception as e:
        messages.error(request, "There was something wrong with your payment.\
            Please try later")
        return HttpResponse(status=400)