from django.test import TestCase
from checkout.models import Order
from django.contrib.auth.models import User


def get_bag_context(self):
    response = self.client.get('/bag/')
    context = response.context
    return context


class TestView (TestCase):
    def test_profiles(self):
        """testing if the bag page works and template used"""
        # when user is not logged in
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, 302)
        # when user is logged in
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        logged_in = self.client.login(
            username='testuser',
            password='12345'
            )
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_show_correct_orders(self):
        """testing if orders shown are correctly associated to profile"""
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        userprofile = user.userprofile
        logged_in = self.client.login(username='testuser', password='12345')
        order = Order(
            user_profile=userprofile,
            full_name='test',
            email="test",
            phone_number="1",
            country="test",
            town_or_city="test",
            street_address1="test",
            delivery_cost=1,
            order_total=1,
            grand_total=1
            )
        order.save()
        order2 = Order(user_profile=userprofile,
                       full_name='test',
                       email="test",
                       phone_number="1",
                       country="test",
                       town_or_city="test",
                       street_address1="test",
                       delivery_cost=1,
                       order_total=1,
                       grand_total=1
                       )
        order2.save()
        user_orders = user.userprofile.orders.all()
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, 200)
        context_orders = response.context['orders']
        self.assertEqual(str(context_orders), str(user_orders))
