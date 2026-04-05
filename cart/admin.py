from django.contrib import admin

from cart.models import CartItem, Cart


class CartAdmin(admin.ModelAdmin):
    model = Cart
    search_fields = ['customer_name']
    list_display = ('user', 'total', 'created_at')
    list_filter = ('user', 'created_at')


class CartItemAdmin(admin.ModelAdmin):
    model = CartItem
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart', 'product')


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)
