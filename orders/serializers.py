from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def validate(self, validated_data):
        product = validated_data['product']

        if validated_data['quantity'] <= product.quantity:
            order_item = OrderItem.objects.create(order=validated_data['order'], product=product,
                                                  quantity=validated_data['quantity'],
                                                  price=validated_data['price'])
            product.quantity -= order_item.quantity
            product.save()
            return validated_data
        else:
            raise serializers.ValidationError(f'Товар {product.name} доступен в количестве {product.quantity} шт., '
                                              f'но вы пытаетесь заказать {validated_data["quantity"]} шт.')

