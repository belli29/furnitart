from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from checkout.models import Order, PreOrder
from django.utils import timezone


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    only_ie_delivery = False
    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        if product.euro_shipping is False:
            only_ie_delivery = True
        subtotal = quantity * product.price
        total += subtotal
        product_count += quantity
        remaining_qty = product.available_quantity - quantity
        """
        creates a list with number of avaialable items
        """
        available_quantity_list = []
        n = 1
        while n <= product.available_quantity:
            available_quantity_list.append(n)
            n += 1

        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'remaining_qty': remaining_qty,
            'product': product,
            'total': subtotal,
            'available_quantity_list': available_quantity_list
        })

    def delivery_calculation(request,):
        """ evaluates if discount for delivery to Ireland applies
        and calculates delivery cost and treshold """

        ie_delivery = False
        # user selected a delivery country in the checkout page
        if "chosen_country" in request.session:
            delivery_country = request.session["chosen_country"]
            if delivery_country == "IE":
                ie_delivery = True
        # user has not selected any country but he is already authenticated
        elif request.user.is_authenticated:
            if request.user.userprofile.default_country == "IE":
                ie_delivery = True
        # apply different delivery rates and treshold
        if ie_delivery:
            free_delivery_treshold = settings.IRL_FREE_DELIVERY_THRESHOLD
            delivery_percentage = settings.IRL_STANDARD_DELIVERY_PERCENTAGE
        else:
            free_delivery_treshold = settings.FREE_DELIVERY_THRESHOLD
            delivery_percentage = settings.STANDARD_DELIVERY_PERCENTAGE
        # calculate delivery percentage and free delivery delta
        if total < free_delivery_treshold:
            delivery = total * Decimal(delivery_percentage / 100)
            free_delivery_delta = free_delivery_treshold - total
        else:
            delivery = 0
            free_delivery_delta = 0
        # define if there is a delivery problem
        delivery_problem = False
        if only_ie_delivery is True and ie_delivery is False:
            delivery_problem = True
        results = {
            'delivery': delivery,
            'free_delivery_delta': free_delivery_delta,
            'free_delivery_threshold': free_delivery_treshold,
            'ie_delivery': ie_delivery,
            'delivery_problem': delivery_problem
        }

        return results
    results = delivery_calculation(request)
    delivery = results['delivery']
    free_delivery_delta = results['free_delivery_delta']
    free_delivery_treshold = results['free_delivery_threshold']
    ie_delivery = results['ie_delivery']
    delivery_problem = results['delivery_problem']
    grand_total = delivery + total

    # for seller banner

    today = timezone.now()
    today = timezone.now().date()
    today_orders = Order.objects.all().filter(
        date__gte=today)
    today_preorders = PreOrder.objects.all().filter(
        date__gte=today)
    today_orders_count = len(today_orders)
    today_preorders_count = len(today_preorders)

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': free_delivery_treshold,
        'grand_total': grand_total,
        'discount': settings.PAY_PAL_DISCOUNT,
        'ie_delivery': ie_delivery,
        'delivery_problem': delivery_problem,
        'today': today,
        'today_orders_count': today_orders_count,
        'today_preorders_count': today_preorders_count,
    }

    return context
