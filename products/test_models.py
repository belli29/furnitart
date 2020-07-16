from django.test import TestCase
from .models import Product

class TestProductModel(TestCase):

    def test_is_active_defaults_to_True(self):
        product = Product(name="Create a Test", price=0)
        product.save()
        self.assertEqual(product.name, "Create a Test")
        self.assertTrue(product.is_active)
    
    def test_euro_shipping_defaults_to_True(self):
        product = Product(name="Create a Test", price=0)
        product.save()
        self.assertEqual(product.name, "Create a Test")
        self.assertTrue(product.euro_shipping)
    
  
