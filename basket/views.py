from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from store.models import Product
from .basket import Basket


# Create your views here.
def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        product_quantity = int(request.POST.get('productQuantity'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, product_quantity=product_quantity)

        all_quantity = basket.__len__()
        response = JsonResponse({'quantity': all_quantity})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        basket.delete(product=product_id)
        response = JsonResponse({'Success': True})
        basket_quantity = basket.__len__()
        baskettotal = basket.get_total_price()

        response = JsonResponse({'quantity': basket_quantity, 'total': baskettotal})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        product_quantity = int(request.POST.get('productQuantity'))
        basket.update(product=product_id, product_quantity=product_quantity)

        basket_quantity = basket.__len__()
        baskettotal = basket.get_total_price()
        print(baskettotal)
        response = JsonResponse({'quantity': basket_quantity, 'subtotal': baskettotal})
        return response
