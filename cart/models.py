from functools import total_ordering

from django.db import models
from django.db.models import Count, Sum, Avg, Max

from authentication.models import CustomUser
from catalog.models import AutoParts


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart_user')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self, cart):
        total = sum([x.product.selling_price for x in cart.items.all()])
        cart.total = total
        cart.save()
        return total

    def combining_goods(self, id):
        cart = CartItem.objects.filter(cart=id).values('product__name', 'product__id').annotate(
            quantity=Count('product__id')).annotate(total=Sum('product__selling_price'))

        return cart

    def __str__(self):
        return f'{self.user.email} '


class CartItem(models.Model):
    objects = models.Manager()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(AutoParts, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
