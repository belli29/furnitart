from django.test import TestCase


class TestView (TestCase):

    def test_index(self):
        """testing if the index page works and template used"""
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_contact(self):
        """testing if the contact page works and template used"""
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact.html')

    def test_about(self):
        """testing if the index page works and template used"""
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/about.html')
