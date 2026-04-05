import logging

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from elasticsearch_dsl.query import MultiMatch
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.documents import PartDocument
from catalog.models import AutoParts, GlobalCategory, Subcategories
from catalog.paginations import StandardResultsSetPagination
from catalog.serializers import AutoPartsSerializer, GlobalCategorySerializer, SubcategoriesSerializer, \
    AutoPartsPaginationSerializer, AutoPartImageSerializer

logger = logging.getLogger('django')


class PartApiView(APIView):
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination
    serializer_class = AutoPartsPaginationSerializer

    @extend_schema(
        summary="Список всех товаров",
        description="Возвращает пагинированный список всех доступных товаров с кэшированием на 24 часа."
    )
    @method_decorator(cache_page(60 * 60 * 24, key_prefix='product'))
    def get(self, request):
        try:
            data = AutoParts.objects.all()
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(data, request, view=self)
            serializer = AutoPartsPaginationSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving all parts for user {request.user.id}: {str(e)}")
            return Response({'error': 'Ошибка при получении списка товаров'}, status=500)


class CategoryApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GlobalCategorySerializer

    @extend_schema(
        summary="Список категорий",
        description="Возвращает список всех активных глобальных категорий. Кэшируется на 72 часа."
    )
    @method_decorator(cache_page(60 * 60 * 72, key_prefix='Category'))
    def get(self, request):
        try:
            category = GlobalCategory.objects.filter(is_active=True)
            serializer = GlobalCategorySerializer(category, many=True)
            return Response({'Category': serializer.data}, status=200)
        except Exception as e:
            logger.error(f"Error retrieving categories for user {request.user.id}: {str(e)}")
            return Response({'error': 'Ошибка при получении категорий'}, status=500)


class SubcategoriesApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubcategoriesSerializer

    @extend_schema(
        summary="Список подкатегорий",
        description="Возвращает список активных подкатегорий для указанной категории. Кэшируется на 72 часа."
    )
    @method_decorator(cache_page(60 * 60 * 72, key_prefix='Subcategories'))
    def get(self, request, pk):
        try:
            subcategory = Subcategories.objects.filter(global_category=pk, is_active=True)
            serializer = SubcategoriesSerializer(subcategory, many=True)
            return Response({'Subcategory': serializer.data}, status=200)
        except Exception as e:
            logger.error(f"Error retrieving subcategories for user {request.user.id}, category {pk}: {str(e)}")
            return Response({'error': 'Ошибка при получении подкатегорий'}, status=500)


class PartCategoryApiView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = AutoPartsPaginationSerializer

    @extend_schema(
        summary="Товары по подкатегории",
        description="Возвращает пагинированный список доступных товаров для указанной подкатегории. Кэшируется на 48 "
                    "часов."
    )
    @method_decorator(cache_page(60 * 60 * 48, key_prefix='product'))
    def get(self, request, pk):
        try:
            parts = AutoParts.objects.filter(subcategory=pk, is_available=True)

            if parts.exists():
                paginator = self.pagination_class()
                page = paginator.paginate_queryset(parts, request, view=self)
                serializer = AutoPartsPaginationSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response({'Message': 'пока нет товаров в этой подкатегории'}, status=200)
        except Exception as e:
            logger.error(f"Error retrieving parts for category {pk}, user {request.user.id}: {str(e)}")
            return Response({'error': 'Ошибка при получении товаров категории'}, status=500)


class SearchApiView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = AutoPartsPaginationSerializer

    @extend_schema(
        summary="Поиск товаров",
        description="Выполняет полнотекстовый поиск по названию, бренду, описанию и характеристикам товара. Параметр "
                    "q обязателен."
    )
    def get(self, request):
        q = request.GET.get('q')
        if q:
            try:
                query = MultiMatch(query=q, fields=['name', 'brand', 'short_description', 'features'], fuzziness='AUTO')
                part = PartDocument.search().query(query)
                qs = part.to_queryset()
                paginator = self.pagination_class()
                page = paginator.paginate_queryset(qs, request, view=self)
                serializer = AutoPartsPaginationSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            except Exception as e:
                logger.error(f"Search error for query '{q}', user {request.user.id}: {str(e)}")
                return Response({'error': 'Ошибка при выполнении поиска'}, status=500)
        else:
            return Response({'error': 'вы не указали параметры поиска.'})


class OnePartApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AutoPartsSerializer

    @extend_schema(
        summary="Детальная информация о товаре",
        description="Возвращает полную информацию о товаре по его ID, включая изображения. Кэшируется на 120 часов."
    )
    @method_decorator(cache_page(60 * 60 * 120, key_prefix='product'))
    def get(self, request, pk):
        try:
            data = AutoParts.objects.prefetch_related('cars').get(pk=pk)

            serializer = AutoPartsSerializer(data)
            images = data.images.all()
            if images.exists():
                serializer = AutoPartImageSerializer(data=images)

                return Response({'data': serializer.data}, status=200)
            else:
                return Response({'data': serializer.data, 'images': 'у товара нет изображений'},
                                status=200)

        except AutoParts.DoesNotExist:
            logger.error(f"Part with id {pk} not found for user {request.user.id}")
            return Response({'error': 'такого id нету'})
        except Exception as e:
            logger.error(f"Error retrieving part {pk} for user {request.user.id}: {str(e)}")
            return Response({'error': 'Ошибка при получении товара'}, status=500)
