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

    def test_search_by_image_filter(self):
        """testing image filter"""
        product = Product(name="test name", price=0, image="")
        product.save()
        response = self.client.get('/products/', {"image_filter": True})
        self.assertNotIn(product, response.context["products"])

    """management tests"""

    def test_delete_preorder(self):
        """testing delete preorder option """

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
                  f'/products/delete_pre_order/{preorder.order_number}'
                  )
        try:
            preorder = PreOrder.objects.get(pk=preorder.id)
        except PreOrder.DoesNotExist:
            preorder = None
        self.assertEqual(None, preorder)

    def test_order_shipped(self):
        """testing if order is maked as shipped correctly"""
        product = Product(
            name="test name",
            price=0, image="",
            available_quantity=10,
            reserved=2
            )
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
        user = User.objects.create_superuser(
            'testuser', 'test@test.com', '12345'
            )
        user.save()
        self.client.login(username=user.username, password='12345')
        response = self.client.post(f'/checkout/toggle_shipped/{order.id}')
        order = Order.objects.get(pk=order.id)
        self.assertTrue(order.shipped)
