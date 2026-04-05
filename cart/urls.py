from django.urls import path
from .views import CreateCartApiView, ViewCartApi, DeleteCartApi, AllDeleteApiView

urlpatterns = [
    path('', ViewCartApi.as_view()),
    path('add/<int:id>/', CreateCartApiView.as_view()),
    path('delete/<int:id>/', DeleteCartApi.as_view()),
    path('all/delete/', AllDeleteApiView.as_view())

]
