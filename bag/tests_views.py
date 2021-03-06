from django.test import TestCase
from products.models import Product
from django.contrib.auth.models import User


class TestView (TestCase):
    def test_bag(self):
        """testing if the bag page works and template used"""
        response = self.client.get('/bag/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_deliverable(self):
        """testing if the bag page does display the info
        that product is not deliverable in case necessary"""
        # create a test product only deliverable to Ireland
        # and add it to the bag
        product = Product(name="Create a Test", price=1, euro_shipping=False)
        product.save()
        session = self.client.session
        session['bag'] = {product.id: 1}
        session.save()
        # user is registed with a default delivery not in Ireland
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.userprofile.default_country = "DE"
        user.save()
        logged_in = self.client.login(
            username='testuser',
            password='12345')
        response = self.client.get('/bag/')
        self.assertTrue(response.context["delivery_problem"])
        # user is registed with a default delivery in Ireland
        user.userprofile.default_country = "IE"
        user.save()
        response = self.client.get('/bag/')
        self.assertFalse(response.context["delivery_problem"])
        # create a product  deliverable to all EU  and add it to the bag
        product = Product(name="Create a Test", price=1, euro_shipping=True)
        product.save()
        session = self.client.session
        session['bag'] = {product.id: 1}
        session.save()
        # user is registed with a default delivery in Ireland
        response = self.client.get('/bag/')
        self.assertFalse(response.context["delivery_problem"])
        # user is registed with a default delivery not in Ireland
        user.userprofile.default_country = "DE"
        user.save()
        response = self.client.get('/bag/')
        self.assertFalse(response.context["delivery_problem"])

    def test_add_to_bag(self):
        """testing the view that adds items id and quantity to the bag"""
        product = Product(name="Create a Test", price=1, euro_shipping=False)
        product.save()
        product = Product.objects.get(
            name="Create a Test",
            price=1,
            euro_shipping=False
            )
        quantity = 2
        response = self.client.post(f'/bag/add/1',
                                    {'quantity': quantity,
                                     'redirect_url': 'home'})
        session = self.client.session
        bag = session['bag']
        self.assertEqual(bag, {str(product.id): quantity})

    def test_update_bag(self):
        """testing the view that updates items id and quantity to the bag"""
        product = Product(name="Create a Test", price=1, euro_shipping=False)
        product.save()
        product = Product.objects.get(
            name="Create a Test",
            price=1,
            euro_shipping=False)
        quantity = 2
        response = self.client.post(f'/bag/add/{product.id}',
                                    {'quantity': quantity,
                                     "redirect_url": 'home'})
        new_quantity = 5
        response = self.client.post(
            f'/bag/update/{product.id}',
            {'quantity': new_quantity}
        )
        session = self.client.session
        bag = session['bag']
        self.assertEqual(bag, {str(product.id): new_quantity})

    def test_remove_from_bag(self):
        """testing the view that remove items from the bag"""
        product = Product(name="Create a Test", price=1, euro_shipping=False)
        product.save()
        product = Product.objects.get(
            name="Create a Test",
            price=1,
            euro_shipping=False
            )
        quantity = 2
        response = self.client.post(f'/bag/add/{product.id}',
                                    {'quantity': quantity,
                                     "redirect_url": 'home'}
                                    )
        session = self.client.session
        bag = session['bag']
        response = self.client.post(
            f'/bag/remove/{product.id}')
        session = self.client.session
        bag = session['bag']
        self.assertEqual(bag, {})
