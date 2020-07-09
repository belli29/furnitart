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
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            'total':subtotal,
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
    }

    return context