import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from basket.basket import Basket


# Create your views here.

@login_required
def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    print(total)

    stripe.api_key = 'sk_test_51IzN5FBE7MCF29mgRrFxHOdAw8B5Ap1Lc1mzhRF85p8u3rdRnI8gYFLLtLHEROieyPLdYOlPHWqWzK91DT2jjVNX00sY7khTgA'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id, }
    )
    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})
