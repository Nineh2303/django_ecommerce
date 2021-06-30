from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase

from store.models import Category, Product
from store.views import product_all


#
# @skip("demonstrating skipping")
# class TestSkip(TestCase):
#     def test_skip_example(self):
#         pass


class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        category = Category.objects.create(name='django', slug='django')
        user = User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=category.id, title='django beginners', created_by_id=user.id,
                                            slug='django-beginners', price='20.20', image='django')

    def test_product_detail_url(self):
        response = self.c.get('/product/django/django-beginners/')
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        response = self.c.get('/shop/django/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>PhotoStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        request = self.factory.get('/item/canon/canon-eos-77d')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>PhotoStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_url_allowed_host(self):
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)
