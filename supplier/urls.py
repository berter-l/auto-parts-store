from django.urls import path
from .views import SupplierCreateApiView, PartCreateAPIView, AutoPartUpdateApiView, OneSupPart, \
    AllPartView, DeletePartApiView

urlpatterns = [
    path('suppliers/', SupplierCreateApiView.as_view(), name='supplier-create'),
    path('parts/', PartCreateAPIView.as_view(), name='part-list-create'),
    path('parts/<int:pk>/', OneSupPart.as_view(), name='part-view-detail'),
    path('parts/all/', AllPartView.as_view(), name='part-detail-update-delete'),
    path('parts/delete/<int:pk>/', DeletePartApiView.as_view(), name='part-delete-detail'),
    path('parts/update/<int:pk>/', AutoPartUpdateApiView.as_view(), name='part-update-detail')
]
