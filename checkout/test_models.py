from django.test import TestCase
from decimal import *
from .models import Order, OrderLineItem, PreOrder, PreOrderLineItem
from products.models import Product

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
                original_bag="test"            
        )
        order.save()
        self.assertFalse(order.shipped)  

    def test_order_total(self):
        #delivery to Ireland
        product = Product(name="product", price=10)
        product2 = Product(name="product2", price=5) 
        product.save()
        product2.save()
        order = Order(
                full_name="test",
                email="test",
                phone_number="12",
                country="IE",
                postcode="test",
                town_or_city="test",
                street_address1="test",
                street_address2="test",
                county="test",
                original_bag="test"            
        )
        order.save()
        orderlineitem = OrderLineItem(
            order=order,
            product=product,
            quantity=2,
        )
        orderlineitem2 = OrderLineItem(
            order=order,
            product=product2,
            quantity=2,
        )
        orderlineitem.save()
        orderlineitem2.save()
        self.assertEqual(order.grand_total, 33)
        #same, order, delivery to EU
        order.country = "DE"
        order.save()
        orderlineitem.save()
        orderlineitem2.save()
        self.assertEqual(order.grand_total, 36)

    def test_preorder_total(self):
        #delivery to Ireland
        product = Product(name="product", price=10)
        product2 = Product(name="product2", price=5) 
        product.save()
        product2.save()
        order = PreOrder(
                full_name="test",
                email="test",
                phone_number="12",
                country="IE",
                postcode="test",
                town_or_city="test",
                street_address1="test",
                street_address2="test",
                county="test",           
        )
        order.save()
        orderlineitem = PreOrderLineItem(
            order=order,
            product=product,
            quantity=2,
        )
        orderlineitem2 = PreOrderLineItem(
            order=order,
            product=product2,
            quantity=2,
        )
        orderlineitem.save()
        orderlineitem2.save()
        self.assertEqual(order.grand_total, Decimal('31.35') )
        #same, order, delivery to EU
        order.country = "DE"
        order.save()
        orderlineitem.save()
        orderlineitem2.save()
        self.assertEqual(order.grand_total, Decimal('34.20')) 