from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


class TestBasketView(TestCase):
    def setUp(self):
        category = Category.objects.create(name='django', slug='django')
        user = User.objects.create(username='admin')
        Product.objects.create(category_id=category.id, title='django lv1', created_by_id=user.id,
                                            slug='django-lv1', price='20', image='django')
        Product.objects.create(category_id=1, title='django lv2', created_by_id=1,
                                            slug='django-lv2', price='15', image='django')
        Product.objects.create(category_id=1, title='django lv3', created_by_id=1,
                                            slug='django-lv3', price='10', image='django')

        response = self.client.post(reverse('basket:basket_add'),
                                    {"productId":1, "productQuantity": 2, "action": "post"},
                                    xhr=True)
        response = self.client.post(reverse('basket:basket_add'),
                                    {"productId": 2, "productQuantity": 2, "action": "post"},
                                    xhr=True)

    def test_basket_url(self):
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        response = self.client.post(reverse('basket:basket_add'),
                                    {"productId": 3, "productQuantity": 3, "action": "post"},
                                    xhr=True)
        self.assertEqual(response.json(), {'quantity': 7})
        response = self.client.post(reverse('basket:basket_add'),
                                    {"productId": 2, "productQuantity": 2, "action": "post"},
                                    xhr=True)
        self.assertEqual(response.json(), {'quantity': 7})

    def test_basket_delete(self):
        response = self.client.post(reverse('basket:basket_delete'), {"productId": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'quantity': 2, 'total': '40.00'})

    def test_basket_update(self):
        response = self.client.post(reverse('basket:basket_update'),
                                    {"productId": 2, "productQuantity": 1, "action": "post"},
                                    xhr=True)
        self.assertEqual(response.json(), {'quantity': 3, 'total': '55.00'})
