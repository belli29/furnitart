from django.test import TestCase
from .models import Product
 
class TestView (TestCase):
 
    def test_products(self):
        """testing if the products page works and template used""""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
    
    def test_quantity_of_product_selectable(self):
        """testing if the selectable product quantity is correct""""
        product = Product(name="Create a Test", price=0, available_quantity=10)
        product.save()
        quantity_already_in_bag = 5
        session = self.client.session
        session['bag'] = {product.id: quantity_already_in_bag }
        session.save()
        response = self.client.get(f'/products/{product.id}')
        remaining_items = product.available_quantity - quantity_already_in_bag
        self.assertEqual(remaining_items, response.context['remaining_qty'])

    def test_search_by_q(self):
        """testing search questy functionality""""
        product = Product(name="test name", price=0, description="test description")
        product.save()
        response = self.client.get(f'/products/', {"q": "test name"}) #searching name by name
        self.assertIn(product, response.context["products"])
        response = self.client.get(f'/products/', {"q": "test description"}) #searching name by description
        self.assertIn(product, response.context["products"])
    
    def test_search_by_euro_filter(self):
        """testing EU shippable filter""""
        product = Product(name="test name", price=0, euro_shipping=False)
        product.save()
        response = self.client.get(f'/products/', {"euro_filter": True})
        self.assertNotIn(product, response.context["products"])
    
    def test_search_by_image_filter(self):
        """testing image filter""""
        product = Product(name="test name", price=0, image="")
        product.save()
        response = self.client.get(f'/products/', {"image_filter": True})
        self.assertNotIn(product, response.context["products"])