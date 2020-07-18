from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    irl_delivery = False
    bag = request.session.get('bag', {})
    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
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
            n+=1

        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'remaining_qty': remaining_qty,
            'product': product,
            'total':subtotal,
            'available_quantity_list': available_quantity_list
        })



    def delivery_calculation (free_delivery_treshold, standard_delivery_percentage):
        if total < free_delivery_treshold:
            delivery = total * Decimal(standard_delivery_percentage/ 100)
            free_delivery_delta = free_delivery_treshold- total
        else:
            delivery = 0
            free_delivery_delta = 0
        results = {
            'delivery': delivery,
            'free_delivery_delta': free_delivery_delta,
            'free_delivery_threshold': free_delivery_treshold,
        }
        return results

    if irl_delivery == False:
        results = delivery_calculation(settings.FREE_DELIVERY_THRESHOLD, settings.STANDARD_DELIVERY_PERCENTAGE)
    
    else:
        results = delivery_calculation(settings.IRL_FREE_DELIVERY_THRESHOLD, settings.IRL_STANDARD_DELIVERY_PERCENTAGE)
    
    delivery = results['delivery']
    free_delivery_delta = results['free_delivery_delta']
    free_delivery_treshold = results['free_delivery_threshold']   
    grand_total = delivery + total
    
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': free_delivery_treshold,
        'grand_total': grand_total,
        'discount': settings.PAY_PAL_DISCOUNT
    }

    return context