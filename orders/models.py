from django.db import models

from authentication.models import CustomUser
from catalog.models import AutoParts


class Order(models.Model):
    PAYMENT_CHOICES = [
        (1, 'Наличными'),
        (2, 'Картой'),
        (3, 'Безналичный'),
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    customer_phone = models.CharField(max_length=20)
    customer_address = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=30, choices=PAYMENT_CHOICES)

    def __str__(self):
        return self.customer_phone


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(AutoParts, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name


