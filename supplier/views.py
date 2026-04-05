import logging

from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import AutoParts
from catalog.paginations import StandardResultsSetPagination
from catalog.serializers import AutoPartsSerializer
from supplier.mixins import GetObjectMixin
from supplier.models import Supplier
from supplier.permissions import SupplierPermission
from supplier.serializers import SupplierSerializer

logger = logging.getLogger('django')


class SupplierCreateApiView(APIView):
    permission_classes = [SupplierPermission]
    serializer_class = SupplierSerializer

    @extend_schema(
        summary="Создать поставщика",
        description="Регистрация нового поставщика. Требуется авторизация. Пользователь автоматически связывается с "
                    "создаваемым поставщиком.",
        request=SupplierSerializer,
        responses=SupplierSerializer
    )
    def post(self, request):
        if not Supplier.objects.filter(user=request.user).exists():
            user = request.user
            serializer = SupplierSerializer(data=request.data)
            serializer.initial_data['user'] = user.id
            try:
                if serializer.is_valid(raise_exception=True):
                    try:
                        with transaction.atomic():
                            serializer.save()
                            return Response(serializer.data, status=201)
                    except Exception as e:
                        logger.error(f"Supplier creation error for user {user.id}: {str(e)}")
                        return Response({"error": "Ошибка при создании поставщика"}, status=500)
            except serializers.ValidationError as e:
                raise
        else:
            return Response({'message': 'вы уже создали поставщика'}, status=400)


class PartCreateAPIView(APIView):
    permission_classes = [SupplierPermission]
    serializer_class = AutoPartsSerializer

    @extend_schema(
        summary="Создать товары",
        description="Создает один или несколько товаров для текущего поставщика. Принимает как один объект, "
                    "так и массив объектов."
    )
    def post(self, request):
        data_req = request.data.copy()
        try:
            data = Supplier.objects.get(user=request.user)
        except Supplier.DoesNotExist:
            logger.error(f"Supplier not found for user {request.user.id} during product creation")
            return Response({"error": "Поставщик не найден"}, status=404)

        if len(data_req) == 1:
            try:
                data_req = request.data.copy()
                data_req = data_req[0]
                data_req['supplier'] = data.id

                serializer = AutoPartsSerializer(data=data_req)
                if serializer.is_valid(raise_exception=True):
                    try:
                        with transaction.atomic():
                            serializer.save()
                            return Response({'name': serializer.data['name'], 'id': serializer.data['id']}, status=201)
                    except Exception as e:
                        logger.error(f"Transaction error saving single product for supplier {data.id}: {str(e)}")
                        return Response({"error": 'При сохранении объекта произошла ошибка. Пожалуйста,'
                                                  ' повторите попытку '
                                                  'позже.', 'e': str(e)}, status=500)
                else:
                    logger.error(f"Product validation error for single product: {serializer.errors}")
                    return Response(serializer.errors, status=400)
            except serializers.ValidationError as e:
                logger.error(f"Error processing single product creation: {str(e)}")
                raise
        else:
            a = {}
            data_req = request.data
            for x in data_req:
                x['supplier'] = data.id

            serializer = AutoPartsSerializer(data=data_req, many=True)
            try:
                if serializer.is_valid(raise_exception=True):
                    try:
                        with transaction.atomic():
                            serializer.save()
                            for x in serializer.data:
                                a[x['id']] = x['name'],

                            return Response(a, status=200)
                    except Exception as e:
                        logger.error(f"Transaction error saving multiple products for supplier {data.id}: {str(e)}")
                        return Response({"error": 'При сохранении объекта произошла ошибка. Пожалуйста,'
                                                  ' повторите попытку '
                                                  'позже.'}, status=400)
                else:
                    logger.error(f"Product validation error for multiple products: {serializer.errors}")
                    return Response(serializer.errors, status=400)
            except serializers.ValidationError as e:
                logger.error(f"Error processing multiple products creation: {str(e)}")
                raise


class OneSupPart(GetObjectMixin, APIView):
    permission_classes = [SupplierPermission]
    serializer_class = AutoPartsSerializer
    pagination_class = StandardResultsSetPagination

    @extend_schema(
        summary="Информация о товаре",
        description="Получить детальную информацию о конкретном товаре по его уникальному идентификатору. Доступен "
                    "только для владельца товара.")
    def get(self, request, id):
        try:
            auto_part = self.get_object(id)
            serializer = AutoPartsSerializer(auto_part)
            return Response(serializer.data, status=200)

        except Exception as e:
            logger.error(f"Error retrieving AutoPart {id} for user {request.user.id}: {str(e)}")
            return Response({"error": 'такого объекта не существует'}, status=400)


class AllPartView(APIView):
    permission_classes = [SupplierPermission]
    serializer_class = AutoPartsSerializer
    pagination_class = StandardResultsSetPagination

    @extend_schema(
        summary="Список всех товаров",
        description="Возвращает полный список товаров, добавленных текущим поставщиком. Результаты автоматически "
                    "разбиваются на страницы для удобной навигации. Каждая страница содержит информацию о количестве "
                    "товаров и ссылки для перехода к другим страницам.")
    def get(self, request):
        try:
            data = Supplier.objects.get(user=request.user)

            data_auto = AutoParts.objects.filter(supplier=data)
            if data_auto.exists():

                paginator = self.pagination_class()
                page = paginator.paginate_queryset(data_auto, request, view=self)
                serializer = AutoPartsSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response({"message": 'У вас еще нет никаких продуктов'}, status=200)

        except Exception as e:
            logger.error(f"Error retrieving supplier products for user {request.user.id}: {str(e)}")
            return Response({"error": 'Произошла ошибка, повторите попытку позже'}, status=400)


class AutoPartUpdateApiView(GetObjectMixin, APIView):
    permission_classes = [SupplierPermission]
    serializer_class = AutoPartsSerializer

    @extend_schema(
        summary="Обновить товар",
        description="Частичное обновление данных товара поставщика."
    )
    def patch(self, request, pk):
        if pk is not None:
            try:
                auto_part = self.get_object(pk)

                serializer = AutoPartsSerializer(data=request.data, instance=auto_part)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=200)
            except serializers.ValidationError as e:
                logger.error(f"Update validation error for product {pk}: {serializer.errors}")
                raise

            except Exception as e:
                logger.error(f"Error updating product {pk}: {str(e)}", exc_info=True)
                return Response({"error": "Ошибка при обновлении товара"}, status=500)
        else:
            logger.error(f"Update attempt without product id by user {request.user.id}")
            return Response({
                "error": "вы не передали идентификатор обновляемого объекта"
            }, status=400)


class DeletePartApiView(GetObjectMixin, APIView):
    permission_classes = [SupplierPermission]

    @extend_schema(
        summary="Удалить товар",
        description="Удаляет товар поставщика по его ID. Операция необратима."
    )
    def delete(self, request, pk):
        try:
            auto_part = self.get_object(pk)

            auto_part.delete()
            return Response({'message': "товар был удален"}, status=200)
        except Exception as e:
            logger.error(f"Error deleting product {pk}: {str(e)}")
            return Response({"error": 'такого товара не существует или вы не являетесь автором объекта'}, status=400)
