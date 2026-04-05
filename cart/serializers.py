from rest_framework import serializers

from cart.models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'price', 'product_name', 'quantity']

    def get_product_name(self, obj):
        return obj.product.name

    def get_price(self, obj):
        return obj.product.selling_price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
