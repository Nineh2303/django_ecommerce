from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.allProducts, name='all_products'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
    path('product/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name="product_detail")
]
