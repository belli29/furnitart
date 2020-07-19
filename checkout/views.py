from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51GuP4JD5esY7sUmQZeBl1o1kZA44XS06hdOZdEBkRn1lw0YDuZOfWomPklTHuOzqrX5LEORM5wrElTIlfAjyKAyD00bQr5nHwM'
    }

    return render(request, template, context)