from django.test import TestCase
from decimal import *
from .models import Order, OrderLineItem, PreOrder, PreOrderLineItem
from products.models import Product
from django.conf import settings


class TestProductModel(TestCase):

    def test_shipped_defaults_to_False(self):
        """
        test if new instance has default field to true
        """ 
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
        """
        test if grand total takes in consideration
        correct delivery fee
        and sums up lineitems correctly
        """ 
        # delivery to Ireland
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
                original_bag="test",
        )
        order.save()
        # check grand total calculation
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
        total = (product.price)*orderlineitem.quantity + (product2.price)*orderlineitem2.quantity
        ie_delivery_fee = total * settings.IRL_STANDARD_DELIVERY_PERCENTAGE / 100
        grand_total = (ie_delivery_fee + total)
        self.assertEqual(order.grand_total, grand_total)
        # same, order, delivery to EU
        order.country = "DE"
        order.save()
        orderlineitem.save()
        orderlineitem2.save()
        delivery_fee = total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        grand_total = (delivery_fee + total)
        self.assertEqual(order.grand_total, grand_total)

    def test_preorder_total(self):
        # delivery to Ireland
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
        self.assertEqual(order.grand_total, Decimal('31.35'))
        # same, order, delivery to EU
        order.country = "DE"
        order.save()
        orderlineitem.save()
        orderlineitem2.save()
        self.assertEqual(order.grand_total, Decimal('34.20'))


    def test_delivery_threshold(self):
        """
        test if grand total takes in consideration
        correct delivery threshold
        """ 
        # delivery to Ireland
        product = Product(name="product", price=51)
        product.save()
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
        )
        order.save()
        orderlineitem = OrderLineItem(
            order=order,
            product=product,
            quantity=1,
        )
        orderlineitem.save()
        self.assertEqual(order.grand_total, order.order_total)
        # same, order, delivery to EU
        order.country = "DE"
        product = Product(name="product", price=201)
        product.save()
        orderlineitem = OrderLineItem(
            order=order,
            product=product,
            quantity=1,
        )
        orderlineitem.save()
        order.save()
        self.assertEqual(order.grand_total, order.order_total)

    def test_paypal_discount(self):
        """
        test if paypal discount
        applies with preorders
        """ 
        product = Product(name="product", price=20)
        product.save()
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
            quantity=1,
        )
        orderlineitem.save()
        total = (product.price)*orderlineitem.quantity
        ie_delivery_fee = total * settings.IRL_STANDARD_DELIVERY_PERCENTAGE / 100
        grand_total = (ie_delivery_fee + total) * settings.PAY_PAL_DISCOUNT /100
        self.assertEqual(float(order.grand_total), grand_total)
        