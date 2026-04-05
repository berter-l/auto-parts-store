from django.contrib import admin

from orders.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_filter = ['payment_type']
    list_display = ['payment_type', 'customer_phone']


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_filter = ['product']
    list_display = ['order', 'product', 'quantity', 'price']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
