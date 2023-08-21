from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'cart', 'total_price', 'total_quantity', 'is_paid', 'is_active']
