from django.test import TestCase
from .models import Order, OrderLineItem

class TestProductModel(TestCase):

    def test_shipped_defaults_to_True(self):
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
                order_total=10,
                original_bag="test"            
        )
        order.save()
        self.assertFalse(order.shipped)  