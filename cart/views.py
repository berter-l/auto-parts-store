import logging
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer
from catalog.models import AutoParts

logger = logging.getLogger('django')


class CreateCartApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Добавить товар в корзину",
        description="Добавляет товар по ID в корзину текущего пользователя. Если корзины нет, создается новая."
    )
    def post(self, request, id):

        if not Cart.objects.filter(user=request.user).exists():

            try:
                with transaction.atomic():
                    cart = Cart.objects.create(user=request.user)
                    data_part = AutoParts.objects.get(id=id)
                    cart_item = CartItem.objects.create(cart=cart, product=data_part)
                    Cart().total_price(cart)
                    serializer = CartItemSerializer(cart_item)
                    return Response(serializer.data)
            except Exception as e:
                logger.error(f"Cart creation error for user {request.user.id}: {str(e)}")
                return Response({'error': 'Что-то пошло не так'})
        else:
            Cart_a = Cart.objects.get(user=request.user)
            data_part = AutoParts.objects.get(id=id)
            cart_item = CartItem.objects.create(cart=Cart_a, product=data_part)
            Cart_a.total_price(Cart_a)
            return Response({'message': 'товар добавлен в корзину'}, status=200)


class ViewCartApi(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    @extend_schema(
        summary="Просмотр корзины",
        description="Возвращает список всех товаров в корзине текущего пользователя и общую сумму."
    )
    def get(self, request):
        try:
            data_cart = Cart.objects.get(user=request.user)
            cart_item = data_cart.items.all()

            total_price = data_cart.total_price(data_cart)
            data = CartItem.objects.select_related('product').filter(cart=data_cart)
            data = data_cart.combining_goods(id=Cart.objects.get(user=request.user.id))
            return Response({'cart': data, 'total_price': total_price})


        except Exception as e:
            logger.error(f"Cart retrieval error for user {request.user.id}: {str(e)}")
            return Response({"message": 'в вашей корзине еще нет товаров'})


class DeleteCartApi(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Удалить товар из корзины",
        description="Удаляет конкретный товар из корзины текущего пользователя по ID товара."
    )
    def delete(self, request, id):
        try:
            data_cart = Cart.objects.get(user=request.user.id)
            cart_item = data_cart.items.all()
            cart_item = cart_item.filter(product=id).first()
            cart_item.delete()
            return Response({'message': 'okey'}, status=200)
        except Exception as e:
            logger.error(f"Cart item deletion error for user {request.user.id}, product {id}: {str(e)}")
            return Response({'error': 'invalid product id'}, status=400)


class AllDeleteApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Очистить корзину",
        description="Полностью удаляет всю корзину текущего пользователя со всеми товарами."
    )
    def delete(self, request):
        try:
            data_cart = Cart.objects.get(user=request.user)
            data_cart.delete()
            return Response({'message': 'корзина покупок была успешно очищена'}, status=200)
        except Exception as e:
            logger.error(f"Cart deletion error for user {request.user.id}: {str(e)}")
            return Response({'error': 'у вас нету корзины, либо она пуста'}, status=400)
