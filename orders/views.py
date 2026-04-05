import logging
from rest_framework.exceptions import APIException
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from cart.models import Cart
from orders.serializers import OrderSerializer, OrderItemSerializer
from rest_framework import serializers

logger = logging.getLogger('django')


class OrderApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    @extend_schema(
        summary="Оформить заказ",
        description="Создает заказ на основе товаров в корзине текущего пользователя. Корзина автоматически очищается "
                    "после успешного оформления."
    )
    def post(self, request):
        orders_item = []
        try:
            cart = Cart.objects.get(user=request.user)
            data = request.data
            data['customer'] = request.user.id
            data['total_amount'] = cart.total
            serializer = OrderSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                try:
                    with transaction.atomic():
                        order = serializer.save()
                        itemi = cart.combining_goods(id=cart.id)

                        for item in itemi:
                            orders_item.append({
                                'order': order.id,
                                'product': item['product__id'],
                                'quantity': item['quantity'],
                                'price': item['total']
                            })

                        order_serializer = OrderItemSerializer(data=orders_item, many=True)
                        if order_serializer.is_valid(raise_exception=True):
                            order_serializer.save()
                            cart.delete()
                            return Response({'message': 'заказ был оформлен'}, status=201)


                except serializers.ValidationError as e:
                    logger.error(f"Order creation transaction error for user {request.user.id}: {str(e)}")
                    raise

                except Exception as e:
                    logger.error(
                        f"Transaction error for user {request.user.id}: {str(e)}",

                    )
                    raise APIException("Произошла ошибка при оформлении заказа. Попробуйте позже.")
            else:
                logger.error(f"Order validation error for user {request.user.id}: {serializer.errors}")
                return Response({'data': serializer.errors}, status=400)

        except ObjectDoesNotExist:
            logger.error(f"Unexpected error during order creation for user {request.user.id}")
            return Response({'message': 'Вы еще не выбрали товары, которые хотите купить'})
