from django.urls import path

from authentication.views import RegistrationView, UpdateJWTView, LogoutAPIView, LoginAPIView
urlpatterns = [
    path('', RegistrationView.as_view()),
    path('update_token/', UpdateJWTView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('login/', LoginAPIView.as_view())

]
