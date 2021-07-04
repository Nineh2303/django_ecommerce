from django.contrib import admin

from .models import Order, OrderItem


# Register your models here.
class OrderShow(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'order_key', 'total_paid')




admin.site.register(Order, OrderShow)
admin.site.register(OrderItem)
