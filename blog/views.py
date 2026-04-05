from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from elasticsearch_dsl.query import MultiMatch
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.documents import ArticleDocument
from blog.models import Article
from blog.paginations import BlogResultsSetPagination
from blog.serializers import BlogSerializer


class ArticleView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = BlogResultsSetPagination
    serializer_class = BlogSerializer

    @extend_schema(
        summary="Список статей",
        description="Возвращает пагинированный список всех статей блога. Кэшируется на 24 часа."
    )
    @method_decorator(cache_page(60 * 60 * 24, key_prefix='Article_list'))
    def get(self, request):
        articles = Article.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(articles, request, view=self)
        serializer = BlogSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data, status=200)


class SearchView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer
    pagination_class = BlogResultsSetPagination

    @extend_schema(
        summary="Поиск статей",
        description="Выполняет полнотекстовый поиск по заголовку и содержанию статей. Параметр q обязателен."
    )
    def get(self, request):
        q = request.GET.get('q')
        if q:
            query = MultiMatch(query=q, fields=['title', 'content'])
            article = ArticleDocument.search().query(query)
            article = article.to_queryset()
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(article, request, view=self)
            serializer = BlogSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data, status=200)
        else:
            return Response({'error': 'вы не указали параметры поиска.'})
