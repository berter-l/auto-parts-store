from django.urls import path

from orders.views import OrderApiView

urlpatterns = [
    path('', OrderApiView.as_view())

]
