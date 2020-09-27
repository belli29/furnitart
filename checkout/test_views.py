from django.test import TestCase
from products.models import Product
from django.contrib.auth.models import User


def get_bag_context(self):
    response = self.client.get('/bag/')
    context = response.context
    return context


class TestView (TestCase):

    def test_checkout(self):
        """testing if the products page works and template used"""
        # with no items in bag
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 302)
        # with items in bag
        product = Product(name="Create a Test", price=1, available_quantity=10)
        product.save()
        session = self.client.session
        session['bag'] = {product.id: 1}
        session.save()
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_detect_delivery_problem(self):
        """detecting if there is an item that cannot be delivered"""
        # create a product only deliverable to Irebale and move it to bag
        product = Product(name="Create a Test", price=1, available_quantity=10,
                          euro_shipping=False)
        product.save()
        session = self.client.session
        session['bag'] = {product.id: 1}
        session.save()
        # user is not logged in
        # (has not specified a delivery address in  Ireland)
        response = self.client.get('/checkout/')
        message = list(response.context['messages'])[0]
        self.assertEqual(40, message.level)
        # user is logged in with delivery adress not Ireland
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.userprofile.default_country = "DE"
        user.save()
        logged_in = self.client.login(username='testuser', password='12345')
        response = self.client.get('/checkout/')
        message = list(response.context['messages'])[0]
        self.assertEqual(40, message.level)
        # user is logged in with delivery adress in Ireland
        user.userprofile.default_country = "IE"
        user.save()
        response = self.client.get('/checkout/')
        message = list(response.context['messages'])
        self.assertEqual([], message)
        # user is logged in with delivery addess in Ireland
        # but selects a delivery to a EU country
        session = self.client.session
        session['chosen_country'] = "DE"
        session.save()
        response = self.client.get('/checkout/')
        message = list(response.context['messages'])[0]
        self.assertEqual(40, message.level)

