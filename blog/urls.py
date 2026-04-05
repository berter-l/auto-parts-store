from django.urls import path
from .views import SearchView, ArticleView
urlpatterns = [
    path('blog/search/', SearchView.as_view()),
    path('blog/', ArticleView.as_view())

]
