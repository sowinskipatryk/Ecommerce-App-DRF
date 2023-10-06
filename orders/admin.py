from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'date_ordered', 'due_date', 'summary_price')
    list_filter = ('client', 'date_ordered', 'due_date')
    search_fields = ('client__username', 'delivery_address')
    date_hierarchy = 'date_ordered'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order__client', 'product')
    search_fields = ('order__client__username', 'product__name')
