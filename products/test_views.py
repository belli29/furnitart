from django.test import TestCase
from bag.contexts import bag_contents
from .models import Product

def get_bag_context(self):
    response = self.client.get('/bag/')
    context = response.context
    return context

 
class TestView (TestCase):
 
    def test_products(self):
        """testing if the products page works and template used"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
    
    def test_quantity_of_product_selectable(self):
        """testing if the selectable product quantity is correct"""
        product = Product(name="Create a Test", price=0, available_quantity=10)
        product.save()
        quantity_already_in_bag = 5
        session = self.client.session
        session['bag'] = {product.id: quantity_already_in_bag }
        session.save()
        response = self.client.get('/bag/')
        bag_context = get_bag_context(self)
        remaining_qty_context = bag_context['bag_items'][0]['remaining_qty']
        remaining_quantity = product.available_quantity - quantity_already_in_bag
        self.assertEqual(remaining_quantity, remaining_qty_context)

    def test_search_by_q(self):
        """testing search questy functionality"""
        product = Product(name="test name", price=0, description="test description")
        product.save()
        response = self.client.get(f'/products/', {"q": "test name"}) #searching name by name
        self.assertIn(product, response.context["products"])
        response = self.client.get(f'/products/', {"q": "test description"}) #searching name by description
        self.assertIn(product, response.context["products"])
    
    def test_search_by_euro_filter(self):
        """testing EU shippable filter"""
        product = Product(name="test name", price=0, euro_shipping=False)
        product.save()
        response = self.client.get(f'/products/', {"euro_filter": True})
        self.assertNotIn(product, response.context["products"])
    
    def test_search_by_image_filter(self):
        """testing image filter"""
        product = Product(name="test name", price=0, image="")
        product.save()
        response = self.client.get(f'/products/', {"image_filter": True})
        self.assertNotIn(product, response.context["products"])