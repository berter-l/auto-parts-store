from django.urls import path
from .views import PartApiView, CategoryApiView, SubcategoriesApiView, PartCategoryApiView, SearchApiView, \
    OnePartApiView

urlpatterns = [
    path('', PartApiView.as_view()),
    path('category/', CategoryApiView.as_view()),
    path('category/<int:pk>/', SubcategoriesApiView.as_view()),
    path('parts/subcategory/<int:pk>/', PartCategoryApiView.as_view()),
    path('parts/search/', SearchApiView.as_view()),
    path('one_part/<int:pk>/', OnePartApiView.as_view()),

]
