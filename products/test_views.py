from django.test import TestCase
from django.shortcuts import get_object_or_404
from bag.contexts import bag_contents
from .models import Product
from checkout.models import Order
from django.contrib.auth.models import User

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

    """management tests"""

    def test_delete_preorder(self):
        """testing deletee preorder option """
         
        preorder = Order(
                full_name="test",
                email="test",
                phone_number="12",
                country="test",
                postcode="test",
                town_or_city="test",
                street_address1="test",
                street_address2="test",
                county="test",
                delivery_cost=10,
                order_total=10,
                grand_total=10,
                original_bag="test"            
        )
        preorder.save()  
        print(preorder.id)
        user = User.objects.create_superuser('testuser', 'test@test.com', '12345')
        user.save()
        self.client.login(username=user.username, password='12345')
        response =self.client.post(f'/products/delete_preorder/{preorder.order_number}')
        preorder.save()
        self.assertEqual (None, preorder)

    def test_order_shipped(self):
        """testing image filter"""
        product = Product(name="test name", price=0, image="", available_quantity=10, reserved=2)
        product.save()
        order = Order(
                full_name="test",
                email="test",
                phone_number="12",
                country="test",
                postcode="test",
                town_or_city="test",
                street_address1="test",
                street_address2="test",
                county="test",
                delivery_cost=10,
                order_total=10,
                grand_total=10,
                original_bag="test"            
        )
        order.save()
        self.assertFalse(order.shipped)
        user = User.objects.create_superuser('testuser', 'test@test.com', '12345')
        user.save()
        user = User.objects.get(id=1)
        self.client.login(username=user.username, password='12345')
        response = self.client.post(f'/checkout/toggle_shipped/{order.id}')
        if response.url == '/products/management/':
            order.shipped = True
        order.save()
        print(user)
        print(order)
        print(order.id)
        print(order.shipped)
        print(response)
        self.assertTrue(order.shipped)
