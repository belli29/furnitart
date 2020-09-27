from django.test import TestCase
from bag.contexts import bag_contents
from django.contrib import messages
from .models import Product
from checkout.models import Order, PreOrder
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
        session['bag'] = {product.id: quantity_already_in_bag}
        session.save()
        response = self.client.get('/bag/')
        bag_context = get_bag_context(self)
        remaining_qty_context = bag_context['bag_items'][0]['remaining_qty']
        remaining_quantity = (
            product.available_quantity - quantity_already_in_bag
        )
        self.assertEqual(remaining_quantity, remaining_qty_context)

    def test_search_by_q(self):
        """testing search questy functionality"""
        product = Product(
            name="test name", price=0, description="test description"
            )
        product.save()
        # searching name by name
        response = self.client.get('/products/', {"q": "test name"})
        self.assertIn(product, response.context["products"])
        # searching name by description
        response = self.client.get('/products/', {"q": "test description"})
        self.assertIn(product, response.context["products"])

    def test_search_by_euro_filter(self):
        """testing EU shippable filter"""
        product = Product(name="test name", price=0, euro_shipping=False)
        product.save()
        response = self.client.get('/products/', {"euro_filter": True})
        self.assertNotIn(product, response.context["products"])

    def test_search_by_avaialable_filter(self):
        """testing avaialable filter"""
        product = Product(name="test name", price=0, available_quantity=0)
        product.save()
        response = self.client.get('/products/', {"available_filter": True})
        self.assertNotIn(product, response.context["products"])

    """management tests"""

    def test_confirm_preorder(self):
        """testing confirm preorder option """

        preorder = PreOrder(
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
        )
        preorder.save()
        user = User.objects.create_superuser(
            'testuser', 'test@test.com', '12345'
            )
        user.save()
        self.client.login(username=user.username, password='12345')
        response = self.client.post(
                  f'/products/confirm_pre_order/{preorder.order_number}',
                  {'pp_transaction_id': 'test_transaction_id'}
                  )
        confirmed_preorder = PreOrder.objects.get(pk=preorder.id)
        self.assertEqual("UPG", confirmed_preorder.status)

    def test_order_shipped(self):
        """testing if order is marked as shipped correctly"""
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
        user = User.objects.create_superuser(
            'testuser', 'test@test.com', '12345'
            )
        user.save()
        self.client.login(username=user.username, password='12345')
        delivery_info = {
            'tracking_number': '12345',
            'provider': 'test provider',
            'expected_wait': 22,
            'order':order,
        }

        response = self.client.post(f'/products/toggle_shipped/{order.id}', delivery_info)
        order = Order.objects.get(pk=order.id)
        self.assertTrue(order.shipped)
        #check if associated delivery was generated
        delivery_generated = False
        delivery = order.delivery.all()[0]
        if (delivery_info['tracking_number'] == delivery.tracking_number and
                delivery_info['provider'] == delivery.provider and
                delivery_info['expected_wait'] == delivery.expected_wait):
            delivery_generated = True
        self.assertTrue(delivery_generated)
        #request to unship the order
        response = self.client.post(f'/products/toggle_shipped/{order.id}')
        order = Order.objects.get(pk=order.id)
        self.assertFalse(order.shipped)

    def test_product_active(self):
        """testing if order is marked active correctly"""
        product = Product(
            name="test name",
            price=0, image="",
            available_quantity=10,
            )
        product.save()
        user = User.objects.create_superuser(
            'testuser', 'test@test.com', '12345'
            )
        user.save()
        self.client.login(username=user.username, password='12345')
        #request to make product inactive
        response = self.client.post(f'/products/toggle_active/{product.id}')
        product = Product.objects.get(pk=product.id)
        self.assertFalse(product.is_active)
        #request to make product active
        response = self.client.post(f'/products/toggle_active/{product.id}')
        product = Product.objects.get(pk=product.id)
        self.assertTrue(product.is_active)

    def test_preorder_invalid(self):
        """testing if preorder is marked invalid correctly"""
        preorder = PreOrder(
            full_name="test",
            email="test",
            phone_number="12",
            country="test",
            postcode="test",
            town_or_city="test",
            street_address1="test",
            street_address2="test",
            county="test",
        )
        preorder.save()
        user = User.objects.create_superuser(
            'testuser', 'test@test.com', '12345'
            )
        user.save()
        self.client.login(username=user.username, password='12345')
        #request to make preorder invalid
        response = self.client.post(f'/products/invalid_pre_order/{preorder.order_number}')
        preorder = PreOrder.objects.get(pk=preorder.id)
        self.assertEqual("INV", preorder.status)
