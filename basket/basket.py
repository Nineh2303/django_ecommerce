from decimal import Decimal

from store.models import Product


class Basket():

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('session_key')
        if 'session_key' not in request.session:
            basket = self.session['session_key'] = {}
        self.basket = basket

    def add(self, product, product_quantity):
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['quantity'] = product_quantity
        else:
            self.basket[product_id] = {'price': str(product.price), 'quantity': int(product_quantity)}
        self.save()

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
            Get the basket data and  count the quantity of item
        """
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    def delete(self, product):
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product, product_quantity):
        product_id = str(product)

        if product_id in self.basket:
            self.basket[product_id]['quantity'] = product_quantity

        self.save()

    def save(self):
        self.session.modified = True
